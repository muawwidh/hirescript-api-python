# HireScript AI Python Service

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Endpoints

POST /api/ai/jd/generate
GET /api/health

Headers

x-internal-secret: <your-secret>

Environment Variables

See .env.example

---

# 🚀 4. Deploy (Railway — fastest)

Steps:

1. Go to Railway
2. New Project → Deploy from GitHub
3. Select your Python repo
4. Add environment variables from `.env`
5. Deploy

