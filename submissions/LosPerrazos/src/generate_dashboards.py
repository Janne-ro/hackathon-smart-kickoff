#!/usr/bin/env python3
"""
generate_dashboards.py

Reads a voice-session report JSON (produced by the AI onboarding call) and
calls OpenAI to generate structured data for both dashboards:

  - data/dashboard-data.json         → tutor dashboard  (dashboard.html)
  - data/student-dashboard-data.json → student dashboard (student-dashboard.html)

Usage:
    python generate_dashboards.py report.json
    cat report.json | python generate_dashboards.py
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Literal, Optional

import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).parent.parent / ".env")


# ─────────────────────────────────────────────────────────────────────────────
# Shared primitives
# ─────────────────────────────────────────────────────────────────────────────

class Badge(BaseModel):
    icon: str = Field(description="Single emoji representing the badge")
    label: str


class MotivationTag(BaseModel):
    icon: str
    label: str


class IconText(BaseModel):
    icon: str
    text: str


# ─────────────────────────────────────────────────────────────────────────────
# Tutor dashboard  (dashboard-data.json)
# ─────────────────────────────────────────────────────────────────────────────

class TutorSkill(BaseModel):
    name: Literal["Speaking", "Listening", "Vocabulary", "Grammar"]
    score: int = Field(ge=0, le=100, description="0–100 proficiency score")
    cefr: Literal["A1", "A2", "B1", "B2", "C1", "C2"]
    icon: str = Field(description="Single emoji for the skill")
    color: str = Field(description="Hex colour string, e.g. #ff5ba4")


class TutorStudent(BaseModel):
    name: str
    initials: str = Field(description="Two-letter uppercase initials derived from name")
    nativeLanguage: str
    targetLanguage: str
    onboardedAt: str = Field(description="Human-readable date, e.g. Mar 19, 2026")
    badges: list[Badge]
    skills: list[TutorSkill] = Field(min_length=4, max_length=4)


class RetentionTimelineItem(BaseModel):
    label: str = Field(description="Milestone label, e.g. 'After 1st Class'")
    score: int = Field(ge=0, le=100)
    color: str = Field(description="Hex colour")


class Retention(BaseModel):
    label: Literal["High", "Medium", "Low"]
    timeline: list[RetentionTimelineItem] = Field(
        min_length=3, max_length=3,
        description="Predicted retention at 3 milestones: 1st class, 1 week, 1 month"
    )
    signals: list[IconText] = Field(
        min_length=2, max_length=6,
        description="Key signals that drove the retention prediction"
    )


class TutorMotivation(BaseModel):
    goals: str = Field(description="One concise sentence summarising the student's goals")
    type: str = Field(description="e.g. Career, Personal, Academic")
    timeline: str = Field(description="e.g. 3–6 months")
    urgency: Literal["High", "Medium", "Low"]
    tags: list[MotivationTag] = Field(min_length=2, max_length=5)


class SentimentSignal(BaseModel):
    label: str
    value: int = Field(ge=0, le=100, description="Signal intensity, 0–100")
    icon: str


class Sentiment(BaseModel):
    overall: Literal["Positive", "Neutral", "Negative", "Mixed"]
    engagement: Literal["High", "Medium", "Low"]
    signals: list[SentimentSignal] = Field(
        min_length=3, max_length=6,
        description="Named signals with intensity scores, e.g. Enthusiasm 85"
    )
    notes: str = Field(description="2–3 sentence narrative for the tutor")


class TutorBrief(BaseModel):
    suggestedFocus: list[IconText] = Field(min_length=2, max_length=4)
    icebreaker: str = Field(description="One concrete icebreaker suggestion for lesson 1")
    watchOut: str = Field(description="One potential friction point the tutor should know")
    aiSummary: str = Field(description="3–4 sentence AI summary paragraph for the tutor")


class Onboarding(BaseModel):
    retention: Retention
    motivation: TutorMotivation
    sentiment: Sentiment
    tutorBrief: TutorBrief


class TutorDashboardData(BaseModel):
    student: TutorStudent
    onboarding: Onboarding


# ─────────────────────────────────────────────────────────────────────────────
# Student dashboard  (student-dashboard-data.json)
# ─────────────────────────────────────────────────────────────────────────────

class StudentInfo(BaseModel):
    name: str
    nativeLanguage: str
    targetLanguage: str
    onboardedAt: str
    badges: list[Badge]


class LearningGoals(BaseModel):
    goal: str = Field(description="e.g. Career & Business")
    inspiration: str = Field(description="e.g. Personal Challenge")
    topicFocus: str = Field(description="e.g. Business English")
    timeline: str = Field(description="e.g. 3–6 months")


class TutorPrefs(BaseModel):
    country: str = Field(description="Preferred tutor country, e.g. United States")
    otherLanguages: list[str] = Field(description="Languages the tutor should speak")
    teachingStyle: list[str] = Field(
        min_length=1, max_length=5,
        description="e.g. Encouraging, Goal-Focused, Structured"
    )


class WeeklyAvailability(BaseModel):
    Mon: list[Literal["Morning", "Afternoon", "Evening"]]
    Tue: list[Literal["Morning", "Afternoon", "Evening"]]
    Wed: list[Literal["Morning", "Afternoon", "Evening"]]
    Thu: list[Literal["Morning", "Afternoon", "Evening"]]
    Fri: list[Literal["Morning", "Afternoon", "Evening"]]
    Sat: list[Literal["Morning", "Afternoon", "Evening"]]
    Sun: list[Literal["Morning", "Afternoon", "Evening"]]


class Scheduling(BaseModel):
    availability: WeeklyAvailability
    budget: str = Field(description="e.g. $15–25 / lesson")
    lessonsPerWeek: int = Field(ge=1, le=7)
    sessionDuration: str = Field(description="e.g. 60 min")


class Preferences(BaseModel):
    goals: LearningGoals
    tutor: TutorPrefs
    scheduling: Scheduling


class AssessmentSkill(BaseModel):
    name: Literal["Speaking", "Listening", "Vocabulary", "Grammar"]
    icon: str
    level: Literal["Beginner", "Intermediate", "Advanced"]
    score: int = Field(ge=0, le=100)
    color: str = Field(description="Hex colour string")


class Assessment(BaseModel):
    overallLevel: Literal["Beginner", "Intermediate", "Advanced"]
    skills: list[AssessmentSkill] = Field(min_length=4, max_length=4)
    strengths: list[IconText] = Field(min_length=1, max_length=4)
    improvements: list[IconText] = Field(min_length=1, max_length=4)


class StudentMotivation(BaseModel):
    quote: str = Field(description="First-person motivational quote attributed to the student")
    tags: list[MotivationTag] = Field(min_length=2, max_length=5)
    timeline: str
    urgency: Literal["High", "Medium", "Low"]
    type: str


class TutorCard(BaseModel):
    name: str = Field(description="e.g. Sarah K.")
    country: str = Field(description="Flag + country name, e.g. '🇺🇸 United States'")
    rating: float = Field(ge=4.0, le=5.0)
    reviews: int = Field(ge=1)
    price: str = Field(description="e.g. $22")
    specialty: str = Field(description="e.g. Business English")
    speaksLanguage: Optional[str] = Field(
        default=None,
        description="Student's native language if the tutor speaks it, else null"
    )


class TutorMatch(BaseModel):
    count: int = Field(ge=1, description="Total number of matching tutors on the platform")
    tutors: list[TutorCard] = Field(
        min_length=3, max_length=3,
        description="Top 3 recommended tutors"
    )


class StudentDashboardData(BaseModel):
    student: StudentInfo
    preferences: Preferences
    assessment: Assessment
    motivation: StudentMotivation
    tutorMatch: TutorMatch


# ─────────────────────────────────────────────────────────────────────────────
# Combined LLM output envelope
# ─────────────────────────────────────────────────────────────────────────────

class DashboardOutput(BaseModel):
    tutorDashboard: TutorDashboardData
    studentDashboard: StudentDashboardData


# ─────────────────────────────────────────────────────────────────────────────
# Generation
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are an AI data analyst for Preply, a language-learning platform.

You receive a JSON report from a student's AI onboarding voice conversation.
The report contains:
  - transcript: the conversation between the AI and the student
  - biomarkers: Thymia voice-based wellness/psychological analysis
    (distress, stress, engagement, sentiment, etc.)

Your job is to produce two JSON objects — one for the tutor dashboard and one
for the student dashboard — exactly matching the required schema.

Guidelines:
- Infer the student's name, native language, and target language from the transcript.
  If the name is unclear use "Daniel".
- Use biomarkers to inform sentiment, stress, and engagement scores.
  Map distress (0–1) → a 0–100 inverse engagement score, stress (0–1) → urgency, etc.
- Skill scores should reflect actual conversation quality (vocabulary range,
  grammar, fluency, listening comprehension observed in the transcript).
- Retention probabilities should be calibrated: high motivation + clear goals = high retention.
- For preferences not stated explicitly (scheduling, budget) use sensible defaults
  consistent with the student's profile and language goal.
- Generate 3 realistic tutor cards that match the student's stated preferences.
- Keep all text concise, warm, and professional.
- Use this date for onboardedAt: {date.today().strftime("%b %d, %Y")}
- Skill icon mapping: Speaking=🎙️, Listening=👂, Vocabulary=💬, Grammar=🔤
- Skill colour mapping: Speaking=#ff5ba4, Listening=#d63d85, Vocabulary=#3b82f6, Grammar=#f59e0b
- Retention timeline colours: After 1st Class=#10b981, After 1 Week=#ff5ba4, After 1 Month=#f59e0b

Return ONLY valid JSON matching the schema. No markdown fences, no extra keys."""


def generate_dashboards(
    session_report: dict,
    api_key: str | None = None,
    model: str = "gpt-4o",
) -> DashboardOutput:
    """
    Call OpenAI with the session report and return validated dashboard data.

    Args:
        session_report: Full session report dict (transcript + biomarkers).
        api_key: OpenAI API key. Defaults to the OPENAI_API_KEY env var.
        model: OpenAI model to use. Defaults to gpt-4o.

    Returns:
        DashboardOutput — both dashboard datasets, validated by Pydantic.
    """
    client = openai.OpenAI(api_key=api_key)

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(session_report, indent=2)},
        ],
        response_format=DashboardOutput,
        temperature=0.3,
    )

    result = response.choices[0].message.parsed
    if result is None:
        raise ValueError(
            "OpenAI returned no parsed output. "
            "Raw response: " + repr(response.choices[0].message.content)
        )
    return result


def save_dashboards(output: DashboardOutput, data_dir: Path) -> None:
    """Write the two dashboard JSON files into data_dir."""
    data_dir.mkdir(parents=True, exist_ok=True)

    tutor_path = data_dir / "dashboard-data.json"
    student_path = data_dir / "student-dashboard-data.json"

    tutor_path.write_text(
        output.tutorDashboard.model_dump_json(indent=2),
        encoding="utf-8",
    )
    student_path.write_text(
        output.studentDashboard.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print(f"Tutor dashboard   -> {tutor_path}")
    print(f"Student dashboard -> {student_path}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) > 1:
        report_path = Path(sys.argv[1])
        if not report_path.exists():
            print(f"Error: file not found: {report_path}", file=sys.stderr)
            sys.exit(1)
        session_report = json.loads(report_path.read_text(encoding="utf-8"))
    else:
        print("Reading session report from stdin…", file=sys.stderr)
        session_report = json.load(sys.stdin)

    print("Calling OpenAI to generate dashboard data…", file=sys.stderr)
    output = generate_dashboards(session_report)

    # Save alongside this script: src/data/
    data_dir = Path(__file__).parent / "data"
    save_dashboards(output, data_dir)


if __name__ == "__main__":
    main()
