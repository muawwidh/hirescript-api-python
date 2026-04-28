from app.models import JDRequest


def build_prompt(request: JDRequest) -> str:
    # --- Length mapping ---
    length_map = {
        "SHORT": "300-500 words",
        "MEDIUM": "600-900 words",
        "LONG": "1000-1300 words"
    }

    # --- Tone mapping ---
    tone_map = {
        "FORMAL": "very professional and corporate",
        "PROFESSIONAL": "clear and business professional",
        "PROFESSIONAL_FRIENDLY": "professional but warm and approachable",
        "CONVERSATIONAL": "natural and easy to read",
        "CONFIDENT": "strong and persuasive",
        "INCLUSIVE": "welcoming and inclusive language",
        "STARTUP_BOLD": "energetic and modern startup tone"
    }

    prompt = f"""
You are an expert recruiter and HR professional.

Generate a high-quality, ATS-friendly job description based on the following details.

STRICT RULES:
- Do NOT invent salary, benefits, or company info if not provided
- Use must-have skills as primary requirements
- Use nice-to-have skills as optional
- Follow the requested tone strictly
- Respect the requested length
- Avoid fluff and generic phrases

JOB DETAILS:
Job Title: {request.jobTitle}
Seniority: {request.seniority}
Location: {request.location}
Work Mode: {request.workMode}
Tone: {tone_map.get(request.tone, request.tone)}
Target Length: {length_map.get(request.targetLength, request.targetLength)}

"""

    # Optional fields
    if request.companyName:
        prompt += f"Company Name: {request.companyName}\n"

    if request.industry:
        prompt += f"Industry: {request.industry}\n"

    if request.department:
        prompt += f"Department: {request.department}\n"

    if request.mustHaveSkills:
        prompt += f"Must Have Skills: {', '.join(request.mustHaveSkills)}\n"

    if request.niceToHaveSkills:
        prompt += f"Nice To Have Skills: {', '.join(request.niceToHaveSkills)}\n"

    if request.yearsExperience:
        prompt += f"Years of Experience: {request.yearsExperience}\n"

    if request.educationRequirement:
        prompt += f"Education: {request.educationRequirement}\n"

    if request.salaryMin and request.salaryMax:
        prompt += f"Salary Range: {request.salaryMin} - {request.salaryMax} {request.salaryCurrency or ''}\n"

    if request.benefits:
        prompt += f"Benefits: {', '.join(request.benefits)}\n"

    if request.growthOpportunity:
        prompt += f"Growth Opportunity: {request.growthOpportunity}\n"

    if request.targetPersona:
        prompt += f"Target Candidate: {request.targetPersona}\n"

    if request.notes:
        prompt += f"Additional Notes: {request.notes}\n"

    prompt += """
OUTPUT FORMAT:
Write a structured job description with sections:

- Job Title
- Company Overview (only if company info provided)
- Role Overview
- Key Responsibilities
- Required Skills
- Nice-to-Have Skills (only if provided)
- Experience / Education
- Salary (only if provided)
- Benefits (only if provided)
- Location & Work Mode
- Growth Opportunities (only if provided)

Make it professional, clean, and recruiter-friendly.
"""

    return prompt