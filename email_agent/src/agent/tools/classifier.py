# agent/tools/email_classifier.py

from typing import Dict, Any
import re


def classify_email(state: Dict[str, Any]) -> Dict[str, Any]:
    """Classify email type: job, promotions, or other."""
    subject = state.get("subject", "").lower()
    body = state.get("body", "").lower()
    sender = state.get("sender", "").lower()

    # Promotion heuristic
    promo_keywords = [
    "sale", "discount", "deal", "offer", "unsubscribe", "promo", "promotion",
    "buy now", "limited time", "clearance", "coupon", "bargain", "special offer",
    "lowest price", "best price", "exclusive", "act now", "hot deal", "flash sale",
    "guaranteed", "save big", "bonus", "gift", "win", "reward", "click here",
    "free trial", "subscribe", "shop now", "don't miss", "weekly offer",
    "get it now", "limited stock", "massive savings", "early access"
    ]
    if any(kw in body or kw in subject for kw in promo_keywords):
        return {**state, "label": "promotions"}

    # Job-related heuristic
    job_keywords = [
    "job", "jobs", "opening", "hiring", "opportunity", "position", "vacancy",
    "recruiter", "career", "apply now", "resume", "CV", "interview", "walk-in",
    "shortlisted", "role", "application", "job description", "JD", "company is hiring",
    "technical round", "HR round", "hiring update", "offer letter", "placement",
    "campus hiring", "urgent requirement", "talent acquisition"
    ]
    if any(kw in body or kw in subject for kw in job_keywords):
        return {**state, "label": "job"}

    return {**state, "label": "other"}
