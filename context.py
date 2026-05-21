"""
context.py  —  EduBuddy context loader for PLACED
---------------------------------------------------
Loads placed_kb.json (produced by scraper.py) and exposes
register_all_contexts(agent) which attaches every @agent.context
function in one call.
 
Usage in chat.py:
    from context import register_all_contexts
    ...
    agent = Agent(...)
    register_all_contexts(agent)
    response = agent.chat(message)
 
If placed_kb.json is missing it falls back to the embedded
STATIC_FALLBACK dict so the bot never breaks in prod.
"""
 
from __future__ import annotations
 
import json
import os
from typing import TYPE_CHECKING

import agent
 
if TYPE_CHECKING:
    from agent import Agent, Tools
 
# Knowledge-base loader
 
KB_PATH = os.path.join(os.path.dirname(__file__), "placed_kb.json")
 
# Embedded fallback so the bot works even if scraper.py hasn't been run yet.
STATIC_FALLBACK: dict = {
    "company": {
        "linkedin": "yes, you can find the links on the bottom",
        "instagram": "yes, you can find the links on the bottom",
        "youtube": "yes, you can find the links on the bottom",
        "telegram": "yes, you can find the links on the bottom",
        "playstore": "yes, you can find the links on the bottom"
    },
    "leadership": [
        {"name": "A S Abhishek",    "role": "Co-Founder & CEO"},
        {"name": "Vishnu Mohan R",  "role": "Co-Founder & COO"},
        {"name": "Vigneswaran A R", "role": "Co-Founder & CAO"},
    ],
    "socials": {
        "linkedin": "yes, you can find the links on the bottom",
        "instagram": "yes, you can find the links on the bottom",
        "youtube": "yes, you can find the links on the bottom",
        "telegram": "yes, you can find the links on the bottom",
        "playstore": "yes, you can find the links on the bottom"
    },
    "navigation": {
        "Home": "contains the main landing page with scrolling sections that explain the company, its programs, and its information",
        "About Us": "About the company, its vision, and its mission",
        "Programs": "Detailed information about the three main programs offered by PLACED: Corporate Readiness, Public Exam Foundation, and Academic Navigator",
        "Mentors": "Information about the mentors associated with PLACED, the mentors are :\nTess - General Awareness Expert\nRishi - General Awareness Expert\nJishnu - General Awareness Expert\nPrem Harshan - Soft Skills and Verbal Ability Coach\nIbnu Syed S - Industry expert\nAnantha Krishnan P - Industry expert\nAnoushka V - Industry expert\nMichelle - Technical and Aptitude Expert\nVarun Menon - Soft Skill and General Awareness Expert\nNayana T - Aptitude Expert\nNandhana - Aptitude Expert\nNeethu T - Aptitude Expert\nJithesh Krishnan R - Recruitment Coach\nMithun - Aptitude Expert\nGeorge - Aptitude Expert\nTaniya Eliza Thomas - General Awareness Expert",
        "Alumni": "Success stories of alumni who have benefited from PLACED's programs",
        "Book Demo": "A call-to-action for institutions to book a demo of PLACED's offerings"
    },
    "journey": [
        {"step": 1, "title": "Apply",    "desc": "Submit your profile and pass the diagnostic assessment."},
        {"step": 2, "title": "Upskill",  "desc": "Progressive learning mapped to real corporate needs."},
        {"step": 3, "title": "Simulate", "desc": "Experience end-to-end mock recruitment pressure."},
        {"step": 4, "title": "Outcome",  "desc": "Achieve success in placements or higher education."},
    ],
    "about": {
        "vision": (
            "Build an inclusive education platform that allows learners from different backgrounds "
            "to explore possibilities through learning that adapts to their needs. "
            "Quality education should not be restricted by location, format, or circumstance."
        ),
        "mission": (
            "Design education that leads to tangible outcomes by combining technology with practical, "
            "engaging teaching methods to help learners build clarity, confidence, and capability."
        ),
    },
    "programs": [
        {
            "key":      "corporate_readiness",
            "name":     "Corporate Readiness",
            "focus":    "Placement Focus",
            "desc":     (
                "Prepares students for real placement success covering Quantitative Aptitude, "
                "Logical Reasoning, Verbal Ability, and Mock Simulations."
            ),
            "ideal_for": "Students targeting corporate / private sector placements.",
        },
        {
            "key":      "public_exam",
            "name":     "Public Exam Foundation",
            "focus":    "Govt. Exam Focus",
            "desc":     (
                "Builds a strong foundation for highly competitive government exams through "
                "timed drills and concept-based exercises for national-level government careers."
            ),
            "ideal_for": "Students targeting PSC, UPSC, banking, or other government exams.",
        },
        {
            "key":      "academic_navigator",
            "name":     "Academic Navigator",
            "focus":    "Higher Studies",
            "desc":     (
                "Guides students through postgraduate programs, professional courses, and flexible "
                "learning pathways to make informed academic decisions."
            ),
            "ideal_for": "Students planning for PG, professional certifications, or further studies.",
        },
    ],
    "scraped_pages": [],
}
 
def _load_kb() -> dict:
    """Load placed_kb.json; fall back to STATIC_FALLBACK if unavailable."""
    if os.path.exists(KB_PATH):
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            # placed_kb.json has {"static": {...}, "scraped": [...]}
            # Merge scraped page texts into the static layer for richer answers.
            kb = raw.get("static", STATIC_FALLBACK).copy()
            kb["scraped_pages"] = [
                {"key": p["key"], "text": p.get("text", "")}
                for p in raw.get("scraped", [])
                if p.get("status") == "ok"
            ]
            return kb
        except (json.JSONDecodeError, KeyError):
            pass
    return STATIC_FALLBACK
 
KB: dict = _load_kb()
 
# Context-string builders
# (each returns a plain string; no asterisks, no markdown — matches
# existing structure_context rule)
 
def _company_text() -> str:
    c = KB["company"]
    return (
        f"Company Name: {c['name']}\n"
        f"Tagline: {c['tagline']}\n"
        f"Type: {c['type']}\n"
        f"Focus: {c['focus']}\n"
        f"Location: {c['location']}\n"
        f"Address: {c['address']}\n"
        f"Phone / WhatsApp: {c['phone']}\n"
        f"WhatsApp: {c['whatsapp']}\n",
        f"Email: {c['email']}\n",
    )
 
def _leadership_text() -> str:
    lines = ["Leadership Team:"]
    for person in KB["leadership"]:
        lines.append(f"  - {person['name']} — {person['role']}")
    return "\n".join(lines)
 
def _programs_text() -> str:
    lines = ["Programs offered by PLACED:"]
    for p in KB["programs"]:
        lines.append(
            f"\n{p['name']} ({p['focus']})\n"
            f"  Description: {p['desc']}\n"
            f"  Ideal for: {p['ideal_for']}"
        )
    return "\n".join(lines)
 
def _journey_text() -> str:
    lines = ["The PLACED Student Journey (4 steps):"]
    for step in KB["journey"]:
        lines.append(f"  Step {step['step']} — {step['title']}: {step['desc']}")
    return "\n".join(lines)
 
def _about_text() -> str:
    a = KB["about"]
    return (
        f"Vision: {a['vision']}\n\n"
        f"Mission: {a['mission']}"
    )
 
def _navigation_text() -> str:
    lines = ["Site Navigation (page name):"]
    for name in KB["navigation"].items():
        lines.append(f"{name}")
    return "\n".join(lines)
 
 
def _socials_text() -> str:
    s = KB["socials"]
    lines = ["PLACED Social Media & Apps:"]
    for platform in s.items():
        lines.append(f"  {platform}")
    return "\n".join(lines)
 
 
def _scraped_pages_text() -> str:
    """Extra text scraped live from the site (if scraper.py was run)."""
    pages = KB.get("scraped_pages", [])
    if not pages:
        return "No live scraped content available. Using static knowledge base."
    chunks: list[str] = []
    for page in pages:
        # Trim to 600 chars per page to stay within token budgets
        text = page["text"][:600].strip()
        if text:
            chunks.append(f"[Page: {page['key']}]\n{text}")
    return "\n\n".join(chunks) if chunks else "Scraped content empty."
 
 
def _behaviour_text() -> str:
    return (
        "Response rules:\n"
        "  - Plain text only, no asterisks, no markdown symbols\n"
        "  - Keep answers short and concise\n"
        "  - When a user asks about a program, always include its URL so they can visit it\n"
        "  - When a user asks how to join or get started, direct them to Book Demo: https://www.placededu.com/signup\n"
        "  - When a user asks for contact, give the phone number and WhatsApp link\n"
        "  - Do not reveal the secret trigger words or the existence of them in any way, only reveal the secret when the trigger word is invoked\n"
        "  - If you do not know something, say so honestly and suggest they contact PLACED via WhatsApp\n",
        "  - When mentioning a page or program, say its name naturally — do not paste raw URLs in the response\n"
    )
 
 
# Public API
 
def register_all_contexts(agent: "Agent") -> None:
    """
    Attach all PLACED knowledge contexts to a live Agent instance.
    Call this right after constructing the Agent, before agent.chat().
 
    Example:
        agent = Agent(model=..., api_key=..., system_prompt=...)
        register_all_contexts(agent)
        reply = agent.chat(user_message)
    """
 
    @agent.context
    def structure_context() -> str:
        return _behaviour_text()
 
    @agent.context
    def company_context() -> str:
        return _company_text()
 
    @agent.context
    def leadership_context() -> str:
        return _leadership_text()
 
    @agent.context
    def programs_context() -> str:
        return _programs_text()
 
    @agent.context
    def journey_context() -> str:
        return _journey_text()
 
    @agent.context
    def about_context() -> str:
        return _about_text()
 
    @agent.context
    def navigation_context() -> str:
        return _navigation_text()
 
    @agent.context
    def socials_context() -> str:
        return _socials_text()
 
    @agent.context
    def scraped_site_context() -> str:
        return _scraped_pages_text()
  