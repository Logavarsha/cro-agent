

## 🛠️ Technology

| Layer                | Technology              |
| -------------------- | ----------------------- |
| 🐍 Backend           | Python, Flask           |
| 🔍 Web Extraction    | Requests, BeautifulSoup |
| 🤖 AI Integration    | OpenAI-compatible API   |
| 🎨 Frontend          | HTML, CSS, JavaScript   |
| 🚀 Production Server | Gunicorn                |
| ☁️ Deployment        | Render                  |

---

## 📁 Project Structure

```text
cro-agent/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── image.png
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
```

---

# 💻 Local Development

## 📋 Prerequisites

* 🐍 Python 3.10+
* 🌐 Internet connection
* 🔑 An API key for the configured OpenAI-compatible provider

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Logavarsha/cro-agent.git
cd cro-agent
```

---

## 2️⃣ Create a Virtual Environment

### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 🍎 macOS / 🐧 Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create:

```text
backend/.env
```

Add:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=openai/gpt-oss-120b
```

> 🔐 **Security:** Never commit `.env` files, API keys, or other secrets to GitHub.

---

## 5️⃣ Start the Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

##  Health Check

```http
GET /api/health
```

### Response

```json
{
  "status": "ok",
  "ai_configured": true,
  "model": "openai/gpt-oss-120b"
}
```

---

## 🔍 Analyze a Page

```http
POST /api/analyze
Content-Type: application/json
```

### Request

```json
{
  "url": "https://example.com"
}
```

The API returns the analyzed page information and structured CRO recommendations.

---

# ☁️ Production Deployment

The application can be deployed as a **Python Web Service on Render**.

### 📂 Root Directory

```text
backend
```

### 🔨 Build Command

```bash
pip install -r requirements.txt
```

### ▶️ Start Command

```bash
gunicorn app:app
```

### 🔐 Environment Variables

Configure the following environment variables in the hosting platform:

```text
OPENAI_API_KEY
OPENAI_MODEL
```

---

# 🌐 Live Demo

### 🚀 CRO Agent

[https://cro-agent-vcmx.onrender.com/](https://cro-agent-vcmx.onrender.com/)

---

```

