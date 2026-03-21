"""
1_extract.py
------------
Extrai texto das 3 fontes PDF e da página Wikipedia,
guarda em ficheiros .txt na pasta texts/
"""

import pdfplumber
import requests
from bs4 import BeautifulSoup
import os
import re

TEXTS_DIR = os.path.join(os.path.dirname(__file__), "texts")
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "pdfsources")

SOURCES = [
    {
        "id": "kajanova",
        "type": "pdf",
        "file": os.path.join(UPLOADS_DIR, "Kajanova_Onthe_history_of_rock_Music_selection.pdf"),
        "title": "On the History of Rock Music",
        "author": "Yvetta Kajanová",
        "year": "2014",
        "publisher": "Peter Lang GmbH, Frankfurt am Main",
        "url": None
    },
    {
        "id": "larson",
        "type": "pdf",
        "file": os.path.join(UPLOADS_DIR, "the-roots-of-rock.pdf"),
        "title": "The Roots of Rock and Roll",
        "author": "Thomas Larson",
        "year": "2020",
        "publisher": "Kendall Hunt Publishing",
        "url": None
    },
    {
        "id": "short_history",
        "type": "pdf",
        "file": os.path.join(UPLOADS_DIR, "A-SHORT-HISTORY-OF-ROCK-N-ROLL.pdf"),
        "title": "A Short History of Rock 'n' Roll",
        "author": "Ken Best",
        "year": "2023",
        "publisher": "Self-published",
        "url": None
    },
    {
        "id": "wikipedia",
        "type": "web",
        "file": None,
        "title": "Rock and Roll",
        "author": "Wikipedia contributors",
        "year": "2025",
        "publisher": "Wikipedia, The Free Encyclopedia",
        "url": "https://en.wikipedia.org/wiki/Rock_and_roll"
    }
]


def extract_pdf(filepath):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_web(url):
    """Extract main text content from a Wikipedia page."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NLP-project/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove navigation, references, tables, infoboxes
    for tag in soup.find_all(["table", "sup", "span", "div"], class_=True):
        classes = tag.get("class", [])
        if any(c in ["navbox", "reflist", "hatnote", "infobox", "toc",
                     "mw-editsection", "reference", "noprint"] for c in classes):
            tag.decompose()

    # Get main content div
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        content = soup.find("div", class_="mw-parser-output")
    if not content:
        content = soup.body

    paragraphs = []
    for p in content.find_all("p"):
        text = p.get_text(separator=" ", strip=True)
        if len(text) > 60:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def clean_text(text):
    """Basic text cleaning."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    # Remove page numbers (standalone digits on a line)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    # Remove footnote markers like [1], [2]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove lines that are just headers/copyright notices
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 10 or l.strip() == '']
    text = '\n'.join(lines)
    return text.strip()


def main():
    os.makedirs(TEXTS_DIR, exist_ok=True)

    for source in SOURCES:
        print(f"Extracting: {source['id']} ...")
        try:
            if source["type"] == "pdf":
                raw = extract_pdf(source["file"])
            else:
                raw = extract_web(source["url"])

            cleaned = clean_text(raw)
            out_path = os.path.join(TEXTS_DIR, f"{source['id']}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"  -> Saved {len(cleaned)} chars to {out_path}")

        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nExtraction complete.")


if __name__ == "__main__":
    main()