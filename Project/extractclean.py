"""
extractnclean.py
----------------
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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    # Recolhe primeiro, só depois remove
    to_remove = []
    for tag in soup.find_all(["table", "sup", "span", "div"]):
        classes = tag.get("class") or []
        if any(c in ["navbox", "reflist", "hatnote", "infobox", "toc",
                     "mw-editsection", "reference", "noprint"] for c in classes):
            to_remove.append(tag)
    for tag in to_remove:
        tag.decompose()

    content = (soup.find("div", {"id": "mw-content-text"})
               or soup.find("div", class_="mw-parser-output")
               or soup.body)

    if content is None:
        return ""

    paragraphs = []
    for p in content.find_all("p"):
        text = p.get_text(separator=" ", strip=True)
        if len(text) > 60:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def clean_text(text):
    """General text cleaning applied to all sources."""
    # Remove page numbers (standalone digits on a line)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    # Remove footnote markers like [1], [2]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove excessive whitespace
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove lines shorter than 10 chars (noise)
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 10 or l.strip() == '']
    return '\n'.join(lines).strip()


def clean_kajanova(text):
    """
    Specific cleaning for Kajanova PDF.
    
    Seguindo a abordagem do aula4.py: marcamos primeiro os blocos
    de footnotes com um símbolo especial (@) e depois removemo-los,
    tal como se faz com os conceitos do dicionário médico.
    """
    # 1. Remove tudo antes da Introduction (TOC, copyright, ISBN)
    match = re.search(r'\nIntroduction\n', text)
    if match:
        text = text[match.start():]

    # 2. Remove Discography, Bibliography e Notes from author
    for section in ['Discography', 'Bibliography', 'Notes from the author']:
        match = re.search(rf'\n{section}\n', text)
        if match:
            text = text[:match.start()]

    # 3. Remove tabela de conteúdos (linhas com ... seguidas de número)
    text = re.sub(r'^.+\.{3,}\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # 4. Marca blocos de footnotes com @ (igual ao aula4.py que marca conceitos)
    # Footnotes começam com número isolado seguido de texto bibliográfico
    # Ex: "65 A complementary rhythm pattern..."
    # Ex: "71 Using 823 various musical examples..."
    text = re.sub(r'(?m)^(\d{1,2})\s+([A-Z])', r'@\1 \2', text)

    # 5. Remove tudo o que foi marcado como footnote (linhas que começam com @)
    # Remove o bloco inteiro até à próxima linha não-footnote
    text = re.sub(r'@\d+[^\n]*\n?', '', text)

    # 6. Remove inline footnote numbers colados a palavras
    # Ex: "rhythm65," -> "rhythm," | "organisation62," -> "organisation,"
    text = re.sub(r'(?<=[a-zA-Z])\d{1,2}(?=[,\.\s])', '', text)

    # 7. Remove linhas com padrões claros de referências bibliográficas
    # (contêm palavras alemãs/eslovacas ou padrões de citação)
    text = re.sub(r'^.*?(Verlag|Supraphon|Bratislava\s*\d|Praha:|Warszava:|Graz,\s*\d|VEB,|SAV\s).*$',
                  '', text, flags=re.MULTILINE)
    text = re.sub(r'^.*?\bp\.\s*\d+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^.*?pp\.\s*\d+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^.*?No\.\s*\d+,\s*\d{4}.*$', '', text, flags=re.MULTILINE)

    # 8. Remove linhas com texto alemão/eslovaco (palavras características)
    text = re.sub(r'^.*?(räumliche|Rhythmik und|Musikgestaltung|Musikkulturen|Jazzforschung|Jazzbuch|Kapitoly).*$',
                  '', text, flags=re.MULTILINE)

    # 9. Remove tabelas de percentagens
    text = re.sub(r'^.+\d+\s*%\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^(Jazz|Rock)\s+(Genre|Occurrence|\d).*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^(Probability|The Total|researched patterns|archetypes).*$', '', text, flags=re.MULTILINE)

    return clean_text(text)


def clean_larson(text):
    """Specific cleaning for Larson PDF."""
    # Remove repeated header/copyright lines
    text = re.sub(r'Chapter 1: The Roots of Rock and Roll from The History.*?\n', '', text)
    text = re.sub(r'by Thomas Larson \| 5th Edition \|.*?\n', '', text)
    text = re.sub(r'Property of Kendall Hunt Publishing\s*\n', '', text)

    # Remove KEY TERMS / KEY FIGURES / CHAPTER headings
    text = re.sub(r'^(KEY\s+(TERMS|FIGURES)|CHAPTER \d+.*|TRIVIA NOTE|MUSIC CUT \d+)\s*$',
                  '', text, flags=re.MULTILINE)

    # Remove all-caps section titles
    text = re.sub(r'^[A-Z][A-Z\s\'\&\-]{10,}$', '', text, flags=re.MULTILINE)

    # Remove lines with "CHAPTER 1" in the middle (header remnants)
    text = re.sub(r'^.*CHAPTER \d+.*The Roots of Rock.*$', '', text, flags=re.MULTILINE)

    # Remove Personnel/Music Cut lines
    text = re.sub(r'^.*Personnel:.*$', '', text, flags=re.MULTILINE)

    # Remove study questions
    match = re.search(r'\nSTUDY\s*\nQUESTIONS', text)
    if match:
        text = text[:match.start()]

    # Remove study question lines starting with number + Describe/What/Why
    text = re.sub(r'^\d+\s+(Describe|What|Why|How)\b.*$', '', text, flags=re.MULTILINE)

    return clean_text(text)


def clean_short_history(text):
    # Remove linhas que começam com número isolado (fragmentos de frase)
    text = re.sub(r'^\d+\s+on\b', '', text, flags=re.MULTILINE)
    return clean_text(text)


def clean_wikipedia(text):
    """Specific cleaning for Wikipedia web content."""
    # Remove spaces before punctuation (artifact from link extraction)
    text = re.sub(r' ([,;:\.\!\?])', r'\1', text)
    text = re.sub(r'\[\d+\]', '', text)
    return clean_text(text)


CLEANERS = {
    "kajanova":      clean_kajanova,
    "larson":        clean_larson,
    "short_history": clean_short_history,
    "wikipedia":     clean_wikipedia,
}


def main():
    os.makedirs(TEXTS_DIR, exist_ok=True)

    for source in SOURCES:
        sid = source["id"]
        print(f"Extracting: {sid} ...")
        try:
            if source["type"] == "pdf":
                raw = extract_pdf(source["file"])
            else:
                raw = extract_web(source["url"])

            cleaner = CLEANERS.get(sid, clean_text)
            cleaned = cleaner(raw)

            out_path = os.path.join(TEXTS_DIR, f"{sid}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"  -> Saved {len(cleaned)} chars to {out_path}")

        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nExtraction complete.")


if __name__ == "__main__":
    main()