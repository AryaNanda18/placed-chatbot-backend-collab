"""
scraper.py  —  PLACED website scraper for EduBuddy
----------------------------------------------------
Fetches every public page of placededu.com, strips noise,
and writes a structured knowledge base to placed_kb.json.
 
Run:  python scraper.py
Output: placed_kb.json   (consumed by context.py)
 
Dependencies:  pip install requests beautifulsoup4
"""
 
import json
import time
import requests
from bs4 import BeautifulSoup
 
# Config
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}
 
PAGES: dict[str, str] = {
    "home":                "https://www.placededu.com/",
    "about":               "https://www.placededu.com/about",
    "programs":            "https://www.placededu.com/programs",
    "corporate_readiness": "https://www.placededu.com/programs/corporate-readiness",
    "public_exam":         "https://www.placededu.com/programs/public-exam",
    "academic_navigator":  "https://www.placededu.com/programs/academic-navigator",
    "mentors":             "https://www.placededu.com/mentors",
    "alumni":              "https://www.placededu.com/alumni",
}
 
OUTPUT_FILE = "placed_kb.json"
 
# Tags that never contain useful body text
NOISE_TAGS = ["script", "style", "noscript", "svg", "img",
               "meta", "link", "head"]
 
# Helpers
 
def clean_text(soup: BeautifulSoup) -> str:
    """Strip noise tags and return collapsed plain text."""
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    lines = [
        line.strip()
        for line in soup.get_text(separator="\n").splitlines()
        if line.strip()
    ]
    # Deduplicate consecutive identical lines (nav links repeat)
    deduped: list[str] = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped)
 
 
def extract_links(soup: BeautifulSoup, base: str = "https://www.placededu.com") -> list[str]:
    """Return internal hrefs found on the page."""
    links: list[str] = []
    for a in soup.find_all("a", href=True):
        href: str = a["href"].strip()
        if href.startswith("/"):
            href = base + href
        if href.startswith(base) and href not in links:
            links.append(href)
    return links
 
 
def scrape_page(key: str, url: str) -> dict:
    """Fetch one page and return a structured record."""
    print(f"  Scraping [{key}] {url} …", end=" ", flush=True)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"FAILED — {exc}")
        return {"key": key, "url": url, "status": "error", "error": str(exc), "text": ""}
 
    soup = BeautifulSoup(resp.text, "html.parser")
 
    # Page title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
 
    # Meta description
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag.get("content", "").strip() if meta_desc_tag else ""
 
    text = clean_text(BeautifulSoup(resp.text, "html.parser"))
    links = extract_links(soup)
 
    print(f"OK  ({len(text)} chars)")
    return {
        "key":         key,
        "url":         url,
        "status":      "ok",
        "title":       title,
        "description": meta_desc,
        "text":        text,
        "links":       links,
    }
 
# Static fallback knowledge
# (used when live scraping fails or as guaranteed base layer)
 
STATIC_KB: dict = {
    "company": {
        "name":     "PLACED",
        "tagline":  "Infinite Possibilities. Definite Outcome.",
        "type":     "EdTech (Education Technology)",
        "focus":    "Placement Assistance for schools and colleges; career readiness, government exam prep, higher studies guidance.",
        "location": "Kowdiar, Trivandrum, Kerala, India",
        "address":  "BNRA 162 A, Bhagavathi Nagar, Golf Links Road, Kowdiar P.O. Trivandrum — 695 003",
        "phone":    "+91 79075 97197",
        "whatsapp": "https://wa.me/917907597197",
        "email":    None,
    },
    "leadership": [
        {"name": "A S Abhishek",    "role": "Co-Founder & CEO"},
        {"name": "Vishnu Mohan R",  "role": "Co-Founder & COO"},
        {"name": "Vigneswaran A R", "role": "Co-Founder & CAO"},
    ],
    "socials": {
        "linkedin":  "https://www.linkedin.com/company/placedtech/",
        "instagram": "https://www.instagram.com/placed.official",
        "youtube":   "https://www.youtube.com/@placed.official",
        "telegram":  "https://t.me/placed_community",
        "playstore": "https://lynde.page.link/ofUJ",
    },
    "navigation": {
        "Home":       "https://www.placededu.com/",
        "About Us":   "https://www.placededu.com/about",
        "Programs":   "https://www.placededu.com/programs",
        "Mentors":    "https://www.placededu.com/mentors",
        "Alumni":     "https://www.placededu.com/alumni",
        "Book Demo":  "https://www.placededu.com/signup",
    },
    "journey": [
        {"step": 1, "title": "Apply",    "desc": "Submit your profile and pass the diagnostic assessment."},
        {"step": 2, "title": "Upskill",  "desc": "Progressive learning mapped to real corporate needs."},
        {"step": 3, "title": "Simulate", "desc": "Experience end-to-end mock recruitment pressure."},
        {"step": 4, "title": "Outcome",  "desc": "Achieve success in placements or higher education."},
    ],
    "architecture": {
        "phases": 7,
        "phase_1": "Diagnostic Analysis",
        "note": "A highly structured, interactive learning framework designed to build problem-solving ability and real-world readiness from day one.",
    },
    "about": {
        "vision": (
            "Build an inclusive education platform that allows learners from different backgrounds "
            "to explore possibilities through learning that adapts to their needs and the world around them. "
            "Quality education should not be restricted by location, format, or circumstance."
        ),
        "mission": (
            "Design education that leads to tangible outcomes. By combining technology with practical, "
            "engaging teaching methods, help learners build clarity, confidence, and capability. "
            "Focus on understanding and application so learning translates into real progress — "
            "academically, professionally, and personally."
        ),
    },
    "programs": [
        {
            "key":   "corporate_readiness",
            "name":  "Corporate Readiness",
            "focus": "Placement Focus",
            "url":   "https://www.placededu.com/programs/corporate-readiness",
            "desc": (
                "Prepares students for real placement success. Covers Quantitative Aptitude, "
                "Logical Reasoning, Verbal Ability, and Mock Simulations. "
                "Brings aptitude, communication, and interview preparation into one structured learning process."
            ),
            "ideal_for": "Students targeting private sector / corporate placements.",
        },
        {
            "key":   "public_exam",
            "name":  "Public Exam Foundation",
            "focus": "Govt. Exam Focus",
            "url":   "https://www.placededu.com/programs/public-exam",
            "desc": (
                "Designed to help students build a strong foundation for highly competitive government exams. "
                "Introduces students early to the structure and demands of national-level government careers "
                "through timed drills and concept-based exercises."
            ),
            "ideal_for": "Students targeting PSC, UPSC, banking, and other national government exams.",
        },
        {
            "key":   "academic_navigator",
            "name":  "Academic Navigator",
            "focus": "Higher Studies",
            "url":   "https://www.placededu.com/programs/academic-navigator",
            "desc": (
                "Guides students through postgraduate programs, professional courses, and flexible "
                "learning pathways so they can make informed academic decisions without confusion."
            ),
            "ideal_for": "Students planning for PG, professional certifications, or further academic qualifications.",
        },
    ],
}

# Main
 
def run() -> None:
    print("=" * 60)
    print("  PLACED Web Scraper — EduBuddy Knowledge Base Builder")
    print("=" * 60)
 
    scraped_pages: list[dict] = []
 
    for key, url in PAGES.items():
        record = scrape_page(key, url)
        scraped_pages.append(record)
        time.sleep(0.8)   # polite crawl delay
 
    successful = [p for p in scraped_pages if p["status"] == "ok"]
    failed     = [p for p in scraped_pages if p["status"] != "ok"]
 
    print(f"\nScraped: {len(successful)} OK / {len(failed)} failed")
    if failed:
        print(f"  Failed pages: {[p['key'] for p in failed]}")
        print("  Static fallback KB will cover missing pages.")
 
    kb = {
        "meta": {
            "source":       "placededu.com",
            "pages_scraped": len(successful),
            "pages_failed":  len(failed),
        },
        "static":  STATIC_KB,
        "scraped": scraped_pages,
    }
 
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
 
    print(f"\nKnowledge base saved → {OUTPUT_FILE}")
    print("Run context.py to load it into EduBuddy.\n")
 
 
if __name__ == "__main__":
    run()