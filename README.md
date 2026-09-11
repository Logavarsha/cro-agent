🚀 AI Landing Page CRO Agent

AI-powered Conversion Rate Optimization for modern landing pages.

AI Landing Page CRO Agent analyzes a public webpage, extracts key conversion signals, and generates a structured CRO audit with practical recommendations.

🔎 Overview

A lightweight CRO auditing platform designed to help founders, marketers, designers, and developers quickly identify conversion opportunities on landing and product pages.

📊 Analysis Areas

🎯 Hero section and value proposition

🖱️ CTA quality and clarity

🛡️ Trust signals

🛍️ Product-page issues

📱 Mobile UX signals

✍️ Copy clarity

⚡ Conversion friction

💡 Prioritized recommendations

📈 Overall CRO score from 0–100

🔄 How It Works

┌─────────────────────┐
│   🌐 Website URL    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│    ⚙️ Flask API     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   🔍 Web Scraping   │
│ Requests + BeautifulSoup │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 📦 Structured Data  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  🤖 AI CRO Analysis │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   📋 JSON Report    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 🖥️ Dashboard        │
└─────────────────────┘

🛠️ Technology

Layer

Technology

🐍 Backend

Python, Flask

🔍 Web Extraction

Requests, BeautifulSoup

🤖 AI Integration

OpenAI-compatible API

🎨 Frontend

HTML, CSS, JavaScript

🚀 Production Server

Gunicorn

☁️ Deployment

Render

📁 Project Structure

cro-agent/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── image.png
├── frontend/
│   └── index.html
├── .gitignore
└── README.md

💻 Local Development

📋 Prerequisites

🐍 Python 3.10+

🌐 Internet connection

🔑 An API key for the configured OpenAI-compatible provider

1️⃣ Clone the Repository

git clone https://github.com/Logavarsha/cro-agent.git
cd cro-agent

2️⃣ Create a Virtual Environment

🪟 Windows

python -m venv venv
venv\Scripts\activate

🍎 macOS / 🐧 Linux

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies

cd backend
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create:

backend/.env

Add:

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=openai/gpt-oss-120b

🔐 Security: Never commit .env files, API keys, or other secrets to GitHub.

5️⃣ Start the Application

python app.py

Open:

http://localhost:5000

🔌 API

❤️ Health Check

GET /api/health

Response

{
  "status": "ok",
  "ai_configured": true,
  "model": "openai/gpt-oss-120b"
}

🔍 Analyze a Page

POST /api/analyze
Content-Type: application/json

Request

{
  "url": "https://example.com"
}

The API returns the analyzed page information and structured CRO recommendations.

☁️ Production Deployment

The application can be deployed as a Python Web Service on Render.

📂 Root Directory

backend

🔨 Build Command

pip install -r requirements.txt

▶️ Start Command

gunicorn app:app

🔐 Environment Variables

Configure the following environment variables in the hosting platform:

OPENAI_API_KEY
OPENAI_MODEL

🌐 Live Demo

🚀 CRO Agent

https://cro-agent-vcmx.onrender.com/
