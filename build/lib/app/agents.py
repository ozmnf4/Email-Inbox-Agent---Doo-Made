from __future__ import annotations

from typing import Literal

from agents import Agent
from pydantic import BaseModel, Field

from app.config import load_config
from app.tools import (
    save_reply_draft_tool,
    archive_email_tool,
    mark_email_read_tool,
    move_to_label_tool,
)


class TriageDecision(BaseModel):
    action: Literal["IGNORE", "REPLY", "SUSPICIOUS", "ARCHIVE", "MOVE_TO_FOLDER"]
    category: Literal[
        "PERSONAL_DIRECT",
        "FINANCE",
        "SALES_OUTREACH",
        "EVENTS_CALENDAR",
        "NEWSLETTERS",
        "SECURITY_ADMIN",
        "PROFESSIONAL_NETWORK",
        "RECEIPTS_BILLING",
        "SAAS_TOOLS",
    ]
    target_folder: str = Field(
        default="",
        description="Target folder/label for MOVE_TO_FOLDER action. Use: Personal & Direct, Finance, Sales & Outreach, Events & Calendar, Newsletters, Security & Admin, Professional Network, Receipts & Billing, SaaS & Tools, Archive, or keep empty for inbox.",
    )
    confidence: float = Field(
        description="Confidence score from 0.0 to 1.0 for the chosen action.",
        ge=0.0,
        le=1.0,
    )
    suspicious_signals: list[str] = Field(
        default_factory=list,
        description="Concrete risk indicators found when action is SUSPICIOUS.",
    )
    reason: str = Field(description="Short explanation for the decision.")
    summary: str = Field(
        default="",
        description="One-sentence summary of the email content for quick review.",
    )


def build_triage_agent() -> Agent[TriageDecision]:
    config = load_config()
    return Agent[TriageDecision](
        name="EmailTriageAgent",
        model=config.openai_model_triage,
        instructions=(
            "You are an email triage specialist for productivity workflows.\n\n"
            "You will receive exactly one email.\n\n"
            "Assign exactly one action:\n"
            "- IGNORE: no response needed, leave in inbox.\n"
            "- REPLY: user should respond and we will draft a reply.\n"
            "- SUSPICIOUS: possible phishing/risky message; user must manually verify.\n"
            "- ARCHIVE: move email out of inbox (for newsletters, promotions, low priority).\n"
            "- MOVE_TO_FOLDER: organize email into specific folder/label and remove from inbox.\n\n"
            "Assign exactly one category:\n"
            "- PERSONAL_DIRECT\n"
            "- FINANCE\n"
            "- SALES_OUTREACH\n"
            "- EVENTS_CALENDAR\n"
            "- NEWSLETTERS\n"
            "- SECURITY_ADMIN\n"
            "- PROFESSIONAL_NETWORK\n"
            "- RECEIPTS_BILLING\n"
            "- SAAS_TOOLS\n\n"
            "For MOVE_TO_FOLDER action, specify target_folder:\n"
            "- Newsletters -> 'Newsletters'\n"
            "- Receipts -> 'Receipts & Billing'\n"
            "- Finance -> 'Finance'\n"
            "- Sales -> 'Sales & Outreach'\n"
            "- etc.\n\n"
            "Rules:\n"
            "- If action is SUSPICIOUS, category should usually be SECURITY_ADMIN.\n"
            "- If action is REPLY, category should typically be ACTION_REQUIRED, EVENTS_CALENDAR, "
            "PERSONAL_DIRECT, PROFESSIONAL_NETWORK, or SALES_OUTREACH.\n"
            "- ARCHIVE is for: newsletters, promotions, notifications, automated emails.\n"
            "- MOVE_TO_FOLDER is for: emails you want to keep but organize (receipts, invoices, etc.).\n"
            "- Include confidence in [0.0, 1.0].\n"
            "- Always provide a brief summary (1 sentence max).\n"
            "- If action is SUSPICIOUS, provide suspicious_signals with concrete evidence (prefer >=2 items).\n\n"
            "Output JSON exactly with:\n"
            "{ \"action\": \"...\", \"category\": \"...\", \"target_folder\": \"...\", \"confidence\": 0.0-1.0, "
            "\"suspicious_signals\": [\"...\"], \"reason\": \"...\", \"summary\": \"...\" }\n"
            "Keep reason concise (one sentence max)."
        ),
        tools=[archive_email_tool, mark_email_read_tool, move_to_label_tool],
        output_type=TriageDecision,
    )


def build_draft_agent() -> Agent[str]:
    config = load_config()
    return Agent[str](
        name="EmailDraftAgent",
        model=config.openai_model_draft,
        instructions=(
            "You are a professional email assistant.\n\n"
            "Given the original email details, write a short, clear, polite reply in plain text.\n"
            "Return only the reply body text.\n"
            "Do not include quoted original message.\n"
            "Do not include markdown.\n"
            "Do not call tools unless the user explicitly asks you to save a draft."
        ),
        tools=[save_reply_draft_tool],
        output_type=str,
    )
