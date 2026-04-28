from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum

class Seniority(str, Enum):
    INTERN = "INTERN"
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    LEAD = "LEAD"
    DIRECTOR = "DIRECTOR"


class WorkMode(str, Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ON_SITE = "ON_SITE"


class Tone(str, Enum):
    FORMAL = "FORMAL"
    PROFESSIONAL = "PROFESSIONAL"
    PROFESSIONAL_FRIENDLY = "PROFESSIONAL_FRIENDLY"
    CONVERSATIONAL = "CONVERSATIONAL"
    CONFIDENT = "CONFIDENT"
    INCLUSIVE = "INCLUSIVE"
    STARTUP_BOLD = "STARTUP_BOLD"


class TargetLength(str, Enum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


class EducationRequirement(str, Enum):
    NONE = "NONE"
    BACHELOR_OR_EQUIV = "BACHELOR_OR_EQUIV"
    MASTERS_PREFERRED = "MASTERS_PREFERRED"
    PHD_PREFERRED = "PHD_PREFERRED"

class JDRequest(BaseModel):
    jobTitle: str = Field(..., min_length=1, max_length=150)
    seniority: Seniority
    location: str = Field(..., min_length=1)
    workMode: WorkMode
    mustHaveSkills: List[str]
    tone: Tone
    targetLength: TargetLength

    # Optional fields
    department: Optional[str] = None
    companyName: Optional[str] = None
    industry: Optional[str] = None
    templateId: Optional[str] = None
    cultureKeywords: Optional[List[str]] = None
    niceToHaveSkills: Optional[List[str]] = None
    yearsExperience: Optional[str] = None
    educationRequirement: Optional[EducationRequirement] = None
    salaryMin: Optional[int] = None
    salaryMax: Optional[int] = None
    salaryCurrency: Optional[str] = None
    benefits: Optional[List[str]] = None
    growthOpportunity: Optional[str] = None
    targetPersona: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("mustHaveSkills")
    @classmethod
    def validate_must_have_skills(cls, v):
        if not (1 <= len(v) <= 15):
            raise ValueError("mustHaveSkills must have between 1 and 15 items")
        return v

    @field_validator("niceToHaveSkills")
    @classmethod
    def validate_nice_to_have(cls, v):
        if v and len(v) > 10:
            raise ValueError("niceToHaveSkills cannot exceed 10 items")
        return v

    @field_validator("salaryMin", "salaryMax")
    @classmethod
    def validate_salary_range(cls, v):
        if v is not None:
            if v < 0 or v > 10_000_000:
                raise ValueError("Salary must be between 0 and 10,000,000")
        return v

    @field_validator("salaryCurrency")
    @classmethod
    def validate_currency(cls, v):
        if v and len(v) != 3:
            raise ValueError("salaryCurrency must be a 3-letter code")
        return v