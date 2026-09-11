# AI Landing Page CRO Agent

A simple AI-powered Conversion Rate Optimization (CRO) auditor.

## Flow

User URL → Flask → Web scraper → OpenAI → CRO JSON → HTML/CSS/JS dashboard

## Requirements

- Python 3.10+
- OpenAI API key
- Internet connection

## Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Create `.env`

Copy `.env.example` to `.env`:

```env
OPENAI_API_KEY=your_real_api_key
OPENAI_MODEL=gpt-5.6-luna
```

Never upload `.env` to GitHub.

### 4. Run

From the `backend` folder:

```bash
python app.py
```

Open:

https://cro-agent-vcmx.onrender.com/
## Notes

The first version uses requests + BeautifulSoup. Some Shopify/modern JavaScript websites may block simple HTTP fetching or render important content only in the browser. For those sites, add Playwright as a next step.

Mobile UX in this version is inferred from extracted page structure/text. A Playwright mobile screenshot + vision analysis can be added later for stronger mobile analysis.
