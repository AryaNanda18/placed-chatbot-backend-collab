# EduBuddy Chatbot

## Overview

EduBuddy is an AI-powered chatbot for PLACED EdTech services. Backend powered by FastAPI + Groq API. Minimal static frontend.

## Prerequisites

- Python 3.8+
- Git (to clone repo)
- Groq API key (sign up at [console.groq.com](https://console.groq.com))

## Quick Start

### 1. Clone & Setup

```
git clone <repo-url>
cd EduBuddy-Chatbot
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Setup Environment

Create `.env` file in root:

```
API_KEY=your_groq_api_key_here
```

### 4. Activate Backend (app_fastapi.py)

```
python app_fastapi.py
```

- Starts FastAPI server at http://localhost:5000
- `/predict` endpoint ready for POST requests.

### 5. Access Frontend (standalone-frontend/base.html)

**Option A: Direct Open (Simplest)**

- Open `standalone-frontend/base.html` in browser (Chrome/Firefox).
- Chatbox appears; type & send (connects to localhost:5000 automatically via JS).

**Option B: Local Server**

```
cd standalone-frontend
python -m http.server 8000
```

- Visit http://localhost:8000/base.html

### 6. Test Chatbot

- Toggle chatbox.
- Ask: "What services does PLACED offer?"
- Backend uses Groq GPT model with EduBuddy context.

## Troubleshooting

- Backend errors? Check terminal, ensure GROQ_API_KEY set.
- CORS issues? check if the endpoint is defined in origins list.
- Frontend not connecting? Verify backend running on port 5000.
- Missing images/JS? All assets in `standalone-frontend/`.
