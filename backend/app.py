import os
import json
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "backend", ".env"), override=True)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.groq.com/openai/v1")
else:
    client = None

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36 "
    "CRO-Agent/1.0"
)


def validate_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def scrape_page(url):
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type.lower():
        raise ValueError("The URL did not return an HTML webpage.")

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = clean_text(soup.title.get_text()) if soup.title else ""
    meta_description = ""
    meta = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    if meta:
        meta_description = clean_text(meta.get("content", ""))

    headings = {
        "h1": [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all("h1")],
        "h2": [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all("h2")],
        "h3": [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all("h3")],
    }

    buttons = []
    for element in soup.find_all(["button", "a", "input"]):
        text = clean_text(
            element.get("value", "")
            or element.get_text(" ", strip=True)
            or element.get("aria-label", "")
        )
        if text and len(text) <= 100:
            buttons.append(text)

    images = []
    for img in soup.find_all("img"):
        images.append({
            "alt": clean_text(img.get("alt", "")),
            "src": img.get("src", "")
        })

    # Keep the page text small enough for the LLM.
    body_text = clean_text(soup.get_text(" ", strip=True))
    body_text = body_text[:18000]

    # Useful signals often found on ecommerce pages.
    lower = body_text.lower()
    keywords = {
        "reviews_or_ratings": any(k in lower for k in ["review", "rating", "stars", "customer reviews"]),
        "shipping": any(k in lower for k in ["shipping", "delivery", "deliver"]),
        "returns": any(k in lower for k in ["return", "refund", "money back"]),
        "guarantee": any(k in lower for k in ["guarantee", "warranty"]),
        "secure_payment": any(k in lower for k in ["secure payment", "secure checkout", "ssl"]),
        "size_guide": any(k in lower for k in ["size guide", "size chart"]),
        "faq": "faq" in lower or "frequently asked questions" in lower,
        "discount": any(k in lower for k in ["discount", "sale", "off"]),
    }

    return {
        "requested_url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "buttons_and_links": buttons[:80],
        "image_count": len(images),
        "image_alt_examples": [x["alt"] for x in images[:20] if x["alt"]],
        "signals": keywords,
        "page_text": body_text,
    }


def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.I)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if match:
            return json.loads(match.group(0))
        raise


def analyze_with_ai(page_data):
    if not client:
        raise RuntimeError("OPENAI_API_KEY is missing in the .env file.")

    system_prompt = """
You are an expert Conversion Rate Optimization (CRO) analyst.

Your job is to audit a product page or landing page for conversion improvement.

Analyze these areas:
1. hero_analysis
2. cta_quality
3. trust_signals
4. product_page_issues
5. mobile_ux
6. copy_clarity
7. friction_points
8. recommendations
9. cro_score

Important rules:
- Do NOT invent facts.
- Separate what is observed from what is recommended.
- If information cannot be verified from the extracted page data, say that it could not be verified.
- Mobile UX is being inferred from page structure/text unless explicit mobile evidence is provided.
- Give practical recommendations that a website owner can actually implement.
- cro_score must be an integer from 0 to 100.
- Return ONLY valid JSON. No markdown and no extra explanation.

Use this JSON shape:
{
  "hero_analysis": "string",
  "cta_quality": "string",
  "trust_signals": "string",
  "product_page_issues": ["string"],
  "mobile_ux": "string",
  "copy_clarity": "string",
  "friction_points": ["string"],
  "recommendations": [
    {"priority": "High|Medium|Low", "recommendation": "string", "reason": "string"}
  ],
  "cro_score": 0
}
"""

    user_prompt = "Analyze this webpage data:\n" + json.dumps(page_data, ensure_ascii=False)

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=system_prompt,
        input=user_prompt,
    )

    return extract_json(response.output_text)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    url = clean_text(data.get("url", ""))

    if not url:
        return jsonify({"error": "Please enter a website URL."}), 400

    if not validate_url(url):
        return jsonify({"error": "Please enter a valid URL starting with http:// or https://"}), 400

    try:
        page_data = scrape_page(url)
        report = analyze_with_ai(page_data)

        return jsonify({
            "success": True,
            "url": page_data["final_url"],
            "page": {
                "title": page_data["title"],
                "meta_description": page_data["meta_description"],
                "h1": page_data["headings"]["h1"],
            },
            "report": report,
        })

    except requests.RequestException as exc:
        return jsonify({
            "error": "Could not fetch the webpage. The site may block automated requests or require JavaScript.",
            "details": str(exc),
        }), 502

    except json.JSONDecodeError:
        return jsonify({
            "error": "The AI returned an invalid report format. Please try again."
        }), 502

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "ai_configured": bool(OPENAI_API_KEY),
        "model": OPENAI_MODEL,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
