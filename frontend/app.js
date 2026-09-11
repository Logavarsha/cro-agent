const form = document.getElementById("analyzeForm");
const urlInput = document.getElementById("urlInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const report = document.getElementById("report");

function setList(elementId, items) {
  const el = document.getElementById(elementId);
  el.innerHTML = "";

  if (!Array.isArray(items) || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No major issues identified from the available page data.";
    el.appendChild(li);
    return;
  }

  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    el.appendChild(li);
  });
}

function renderRecommendations(items) {
  const el = document.getElementById("recommendations");
  el.innerHTML = "";

  if (!Array.isArray(items) || items.length === 0) {
    el.textContent = "No recommendations returned.";
    return;
  }

  items.forEach(item => {
    const box = document.createElement("div");
    box.className = "recommendation";

    const priority = document.createElement("span");
    priority.className = "priority";
    priority.textContent = item.priority || "MEDIUM";

    const title = document.createElement("strong");
    title.textContent = item.recommendation || "";

    const reason = document.createElement("p");
    reason.textContent = item.reason || "";

    box.append(priority, title, reason);
    el.appendChild(box);
  });
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
  report.classList.add("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const url = urlInput.value.trim();
  if (!url) return;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  loading.classList.remove("hidden");
  errorBox.classList.add("hidden");
  report.classList.add("hidden");

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Analysis failed.");
    }

    const r = data.report;

    document.getElementById("pageTitle").textContent =
      data.page?.title || "Page Analysis";

    const pageUrl = document.getElementById("pageUrl");
    pageUrl.textContent = data.url;
    pageUrl.href = data.url;

    document.getElementById("score").textContent = r.cro_score ?? "--";
    document.getElementById("heroAnalysis").textContent = r.hero_analysis || "Not available.";
    document.getElementById("ctaQuality").textContent = r.cta_quality || "Not available.";
    document.getElementById("trustSignals").textContent = r.trust_signals || "Not available.";
    document.getElementById("mobileUx").textContent = r.mobile_ux || "Not available.";
    document.getElementById("copyClarity").textContent = r.copy_clarity || "Not available.";

    setList("productIssues", r.product_page_issues);
    setList("frictionPoints", r.friction_points);
    renderRecommendations(r.recommendations);

    report.classList.remove("hidden");
    report.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (error) {
    showError(error.message);
  } finally {
    loading.classList.add("hidden");
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Page →";
  }
});
