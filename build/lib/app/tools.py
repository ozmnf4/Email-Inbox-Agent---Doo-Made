from __future__ import annotations

import json
import logging

from agents import function_tool

from app.gmail_client import fetch_unread_emails, save_draft_reply, archive_email, mark_email_read, move_to_label


LOGGER = logging.getLogger(__name__)


@function_tool
def list_unread_emails_tool(max_results: int = 10) -> str:
    """
    Fetch unread Gmail inbox messages and return a JSON array string.

    Returns objects with keys: id, threadId, from, subject, snippet, body.
    """

    emails = fetch_unread_emails(max_results=max_results)
    return json.dumps(emails, ensure_ascii=False)


@function_tool
def save_reply_draft_tool(message_id: str, reply_text: str) -> str:
    """
    Save a Gmail draft reply for message_id and return a JSON result string.
    """

    draft_id = save_draft_reply(message_id=message_id, reply_text=reply_text)
    result = {"status": "ok", "draft_id": draft_id}
    LOGGER.info("Draft tool created draft_id=%s for message_id=%s.", draft_id, message_id)
    return json.dumps(result, ensure_ascii=False)


@function_tool
def archive_email_tool(message_id: str) -> str:
    """
    Archive an email by removing it from the inbox.
    Use this for emails that don't need immediate attention (newsletters, promotions, etc.).
    Returns JSON result with status.
    """

    result = archive_email(message_id=message_id)
    LOGGER.info("Archive tool processed message_id=%s, status=%s.", message_id, result.get("status"))
    return json.dumps(result, ensure_ascii=False)


@function_tool
def mark_email_read_tool(message_id: str) -> str:
    """
    Mark an email as read (remove UNREAD label).
    Use this after processing an email.
    Returns JSON result with status.
    """

    result = mark_email_read(message_id=message_id)
    LOGGER.info("Mark read tool processed message_id=%s, status=%s.", message_id, result.get("status"))
    return json.dumps(result, ensure_ascii=False)


@function_tool
def move_to_label_tool(message_id: str, label_name: str) -> str:
    """
    Move an email to a specific label and remove from inbox.
    Use this to organize emails into folders.
    Available labels: Personal & Direct, Finance, Sales & Outreach, Events & Calendar,
    Newsletters, Security & Admin, Professional Network, Receipts & Billing, SaaS & Tools.
    Returns JSON result with status.
    """

    result = move_to_label(message_id=message_id, label_name=label_name)
    LOGGER.info("Move to label tool processed message_id=%s to label=%s, status=%s.", 
                message_id, label_name, result.get("status"))
    return json.dumps(result, ensure_ascii=False)
