# HireScript AI Python Service

HireScript AI Python Service is a FastAPI microservice that generates polished, ATS-friendly job descriptions from structured hiring inputs. It validates request data with Pydantic, builds a recruiter-focused prompt, calls the OpenAI API, and returns a clean API response that can be consumed by another backend, admin panel, or hiring workflow.

## Features

- Generate job descriptions from structured role data
- Support seniority, work mode, tone, target length, salary, benefits, skills, and optional hiring context
- Protect the generation endpoint with an internal API secret header
- Return consistent success and error response shapes
- Validate request payloads with Pydantic models and enums
- Rate-limit generation requests with SlowAPI
- Expose a simple health-check endpoint for deployments

## Tech Stack

- Python
- FastAPI
- Pydantic
- OpenAI Python SDK
- SlowAPI
- Uvicorn

## Project Structure

```text
.
├── app
│   ├── config.py           # Environment-based application settings
│   ├── errors.py           # Reserved for shared error helpers
│   ├── main.py             # FastAPI app, routes, handlers, and rate limiting
│   ├── models.py           # Pydantic request model and enums
│   ├── openai_service.py   # OpenAI client and generation call
│   ├── prompt_builder.py   # Prompt construction logic
│   └── security.py         # Internal secret header validation
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/muawwidh/hirescript-api-python.git
cd hirescript-api-python
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key
INTERNAL_API_SECRET=replace-this-secret
OPENAI_MODEL=gpt-4o-mini
PROMPT_VERSION=jd-generator-v1
REQUEST_TIMEOUT_SECONDS=30
ENVIRONMENT=development
LOG_LEVEL=INFO
```

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Empty string | API key used by the OpenAI SDK |
| `INTERNAL_API_SECRET` | Yes | `dev-secret-123` | Secret expected in the `x-internal-secret` request header |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI model used for generation |
| `PROMPT_VERSION` | No | `jd-generator-v1` | Version label returned in API responses |
| `REQUEST_TIMEOUT_SECONDS` | No | `30` | OpenAI client timeout |
| `ENVIRONMENT` | No | `development` | Runtime environment label |
| `LOG_LEVEL` | No | `INFO` | Logging level |

> Note: set a strong `INTERNAL_API_SECRET` before deploying. The default value is only suitable for local development.

### 5. Run the API locally

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs are available at:

```text
http://127.0.0.1:8000/docs
```

## API Reference

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "UP",
  "service": "hirescript-ai-service"
}
```

### Generate Job Description

```http
POST /api/ai/jd/generate
```

Required header:

```http
x-internal-secret: replace-this-secret
```

The generation endpoint is currently rate-limited to `4/minute` per client IP.

#### Request Body

```json
{
  "jobTitle": "Backend Engineer",
  "seniority": "SENIOR",
  "location": "Vilnius, Lithuania",
  "workMode": "HYBRID",
  "mustHaveSkills": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
  "tone": "PROFESSIONAL_FRIENDLY",
  "targetLength": "MEDIUM",
  "companyName": "HireScript",
  "industry": "HR Technology",
  "department": "Engineering",
  "niceToHaveSkills": ["Docker", "AWS", "OpenAI APIs"],
  "yearsExperience": "5+ years",
  "educationRequirement": "BACHELOR_OR_EQUIV",
  "salaryMin": 5000,
  "salaryMax": 7500,
  "salaryCurrency": "EUR",
  "benefits": ["Flexible schedule", "Learning budget", "Health insurance"],
  "growthOpportunity": "Opportunity to grow into a technical lead role",
  "targetPersona": "Experienced backend engineer who enjoys product-focused teams",
  "notes": "Emphasize ownership, clean APIs, and collaboration."
}
```

#### Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `jobTitle` | string | Job title, 1-150 characters |
| `seniority` | enum | One of `INTERN`, `JUNIOR`, `MID`, `SENIOR`, `LEAD`, `DIRECTOR` |
| `location` | string | Role location |
| `workMode` | enum | One of `REMOTE`, `HYBRID`, `ON_SITE` |
| `mustHaveSkills` | string array | 1-15 required skills |
| `tone` | enum | Desired writing tone |
| `targetLength` | enum | One of `SHORT`, `MEDIUM`, `LONG` |

#### Optional Fields

| Field | Type | Description |
| --- | --- | --- |
| `department` | string | Department or team name |
| `companyName` | string | Company name |
| `industry` | string | Company or role industry |
| `templateId` | string | Optional template identifier for future use |
| `cultureKeywords` | string array | Optional culture keywords for future use |
| `niceToHaveSkills` | string array | Up to 10 optional skills |
| `yearsExperience` | string | Experience requirement |
| `educationRequirement` | enum | One of `NONE`, `BACHELOR_OR_EQUIV`, `MASTERS_PREFERRED`, `PHD_PREFERRED` |
| `salaryMin` | integer | Minimum salary, from 0 to 10,000,000 |
| `salaryMax` | integer | Maximum salary, from 0 to 10,000,000 |
| `salaryCurrency` | string | 3-letter currency code, for example `USD` or `EUR` |
| `benefits` | string array | Benefits to include in the job description |
| `growthOpportunity` | string | Growth or career path information |
| `targetPersona` | string | Description of the ideal candidate |
| `notes` | string | Additional instructions, up to 1000 characters |

#### Supported Tones

```text
FORMAL
PROFESSIONAL
PROFESSIONAL_FRIENDLY
CONVERSATIONAL
CONFIDENT
INCLUSIVE
STARTUP_BOLD
```

#### Target Lengths

| Value | Generated Length |
| --- | --- |
| `SHORT` | 300-500 words |
| `MEDIUM` | 600-900 words |
| `LONG` | 1000-1300 words |

#### Example cURL Request

```bash
curl -X POST "http://127.0.0.1:8000/api/ai/jd/generate" \
  -H "Content-Type: application/json" \
  -H "x-internal-secret: replace-this-secret" \
  -d '{
    "jobTitle": "Backend Engineer",
    "seniority": "SENIOR",
    "location": "Vilnius, Lithuania",
    "workMode": "HYBRID",
    "mustHaveSkills": ["Python", "FastAPI", "PostgreSQL"],
    "tone": "PROFESSIONAL_FRIENDLY",
    "targetLength": "MEDIUM",
    "companyName": "HireScript",
    "niceToHaveSkills": ["Docker", "AWS"],
    "yearsExperience": "5+ years",
    "salaryMin": 5000,
    "salaryMax": 7500,
    "salaryCurrency": "EUR"
  }'
```

#### Success Response

```json
{
  "status": "SUCCESS",
  "content": "Generated job description content...",
  "modelUsed": "gpt-4o-mini",
  "promptVersion": "jd-generator-v1",
  "tokensUsed": 1234
}
```

#### Error Responses

Missing or invalid internal secret:

```json
{
  "detail": {
    "status": "ERROR",
    "errorCode": "UNAUTHORIZED",
    "message": "Invalid internal API secret"
  }
}
```

Validation error:

```json
{
  "status": "ERROR",
  "errorCode": "VALIDATION_ERROR",
  "message": "Value error, mustHaveSkills must have between 1 and 15 items"
}
```

Rate limit error:

```json
{
  "status": "ERROR",
  "errorCode": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again later."
}
```

OpenAI or internal error:

```json
{
  "status": "ERROR",
  "errorCode": "OPENAI_API_ERROR",
  "message": "Failed to generate job description"
}
```

## How It Works

1. A client sends structured job information to `/api/ai/jd/generate`.
2. `verify_internal_secret` checks the `x-internal-secret` header.
3. `JDRequest` validates required fields, enum values, skill counts, salary range, and currency format.
4. `build_prompt` converts the request into a detailed recruiter-focused prompt.
5. `generate_job_description` sends the prompt to OpenAI using the configured model.
6. The API returns generated content, model name, prompt version, and token usage.

## Deployment

This service can be deployed to platforms that support Python web apps, including Railway, Render, Fly.io, and container-based hosting.

For Railway:

1. Create a new Railway project.
2. Deploy from this GitHub repository.
3. Add the required environment variables.
4. Set the start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Deploy and test `/api/health`.

## Production Notes

- Replace the default `INTERNAL_API_SECRET`.
- Keep `OPENAI_API_KEY` out of source control.
- Consider moving the hardcoded route limit in `app/main.py` to the `RATE_LIMIT_PER_MINUTE` setting if you want environment-based rate limits.
- Add automated tests for validation, authorization, prompt generation, and OpenAI error handling before production use.
- Add request logging and observability around generation latency, token usage, and failure rates.

## License

No license file is currently included. Add a license before distributing or accepting external contributions.
