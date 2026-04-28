from openai import OpenAI, APITimeoutError, RateLimitError, APIError
from app.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=settings.REQUEST_TIMEOUT_SECONDS
)


def generate_job_description(prompt: str):
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert recruiter and HR job description writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content

        tokens_used = None
        if response.usage:
            tokens_used = response.usage.total_tokens

        return {
            "content": content,
            "modelUsed": settings.OPENAI_MODEL,
            "tokensUsed": tokens_used
        }

    except APITimeoutError:
        raise Exception("OPENAI_TIMEOUT")

    except RateLimitError:
        raise Exception("OPENAI_RATE_LIMIT")

    except APIError:
        raise Exception("OPENAI_API_ERROR")

    except Exception:
        raise Exception("INTERNAL_SERVER_ERROR")