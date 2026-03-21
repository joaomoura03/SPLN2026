"""
generate_latex.py
-----------------
Passo e) do projeto SPLN 2025/26.

Produz um artigo LaTeX para cada fonte com:
  - Abstract: as 3 frases selecionadas pelo modelo n-gram (em itemize)
  - Corpo: entidades nomeadas identificadas pelo spaCy (PERSON, ORG, GPE, DATE, WORK_OF_ART)
  - Bibliografia: citação da fonte original
"""

import os
import json
import re
import subprocess

SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores", "scored_sentences.json")
NER_FILE    = os.path.join(os.path.dirname(__file__), "ner", "ner_results.json")
LATEX_DIR   = os.path.join(os.path.dirname(__file__), "latex")

# Metadados de cada fonte
SOURCES_META = {
    "kajanova": {
        "title":     "On the History of Rock Music",
        "author":    "Yvetta Kajanová",
        "year":      "2014",
        "publisher": "Peter Lang GmbH",
        "location":  "Frankfurt am Main",
        "bibtype":   "book",
        "bibkey":    "kajanova2014",
    },
    "larson": {
        "title":     "The Roots of Rock and Roll",
        "author":    "Thomas Larson",
        "year":      "2020",
        "publisher": "Kendall Hunt Publishing",
        "location":  "Dubuque, IA",
        "bibtype":   "book",
        "bibkey":    "larson2020",
    },
    "short_history": {
        "title":     "A Short History of Rock 'n' Roll",
        "author":    "Ken Best",
        "year":      "2023",
        "publisher": "Self-published",
        "location":  "",
        "bibtype":   "misc",
        "bibkey":    "best2023",
    },
    "wikipedia": {
        "title":     "Rock and Roll",
        "author":    "Wikipedia contributors",
        "year":      "2025",
        "publisher": "Wikipedia, The Free Encyclopedia",
        "location":  "",
        "bibtype":   "misc",
        "bibkey":    "wikipedia2025",
        "url":       "https://en.wikipedia.org/wiki/Rock\\_and\\_roll",
    },
}

# Nomes das categorias NER para apresentar no artigo
NER_LABELS = {
    "PERSON":     "People and Artists",
    "ORG":        "Bands, Labels and Organisations",
    "GPE":        "Places and Locations",
    "DATE":       "Dates and Time Periods",
    "WORK_OF_ART":"Works of Art",
}


def latex_escape(text):
    """Escapa caracteres especiais do LaTeX."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&',  r'\&'),
        ('%',  r'\%'),
        ('$',  r'\$'),
        ('#',  r'\#'),
        ('^',  r'\textasciicircum{}'),
        ('~',  r'\textasciitilde{}'),
        ('{',  r'\{'),
        ('}',  r'\}'),
        ('\u2019', "'"),
        ('\u2018', "`"),
        ('\u201c', "``"),
        ('\u201d', "''"),
        ('\u2013', '--'),
        ('\u2014', '---'),
        ('\u2026', r'\ldots{}'),
        ('\u00e9', r'\'e'),
        ('\u00e1', r'\'a'),
        ('\u00f3', r'\'o'),
        ('\u00fa', r'\'u'),
        ('\u00ed', r'\'i'),
        ('\u00e0', r'\`a'),
        ('\u00e2', r'\^a'),
        ('\u00ea', r'\^e'),
        ('\u00f4', r'\^o'),
        ('\u00e3', r'\~a'),
        ('\u00f5', r'\~o'),
        ('\u00fc', r'\"u'),
        ('\u00e4', r'\"a'),
        ('\u00f6', r'\"o'),
        ('\u00c9', r'\'E'),
        ('\u00c1', r'\'A'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def make_abstract(sentences):
    """Gera o bloco abstract com as 3 frases em itemize."""
    items = "\n".join(
        f"  \\item {latex_escape(s['sentence'])}"
        for s in sentences
    )
    return rf"""
The following three sentences were automatically selected from the source text
using a trigram language model trained on the full corpus of four sources.
Each sentence was scored by the average log-probability of its constituent
trigrams. Sentences whose trigrams appear more frequently in the corpus
receive a higher score, making them the most \emph{{representative}} sentences
of the source.

\begin{{itemize}}
{items}
\end{{itemize}}
""".strip()


def make_ner_section(ner_data):
    """Gera a secção de NER com subsecções por categoria."""
    lines = []
    for label, heading in NER_LABELS.items():
        entities = ner_data.get(label, [])
        if not entities:
            continue
        lines.append(f"\\subsection{{{heading}}}")
        lines.append("\\begin{itemize}")
        for ent in entities:
            cleaned = ent.replace('\n', ' ').strip()
            if len(cleaned) > 1:
                lines.append(f"  \\item {latex_escape(cleaned)}")
        lines.append("\\end{itemize}")
        lines.append("")
    return "\n".join(lines)


def make_bibliography(sid):
    """Gera a entrada bibliográfica."""
    m = SOURCES_META[sid]
    key    = m["bibkey"]
    author = latex_escape(m["author"])
    title  = latex_escape(m["title"])
    year   = m["year"]
    pub    = latex_escape(m["publisher"])
    loc    = latex_escape(m.get("location", ""))

    if m["bibtype"] == "book":
        entry = (
            f"\\bibitem{{{key}}}\n"
            f"{author}.\n"
            f"\\textit{{{title}}}.\n"
            f"{loc}: {pub}, {year}."
        )
    else:
        entry = (
            f"\\bibitem{{{key}}}\n"
            f"{author}.\n"
            f"\\textit{{{title}}}.\n"
            f"{pub}, {year}."
        )
        if "url" in m:
            entry += f"\nAvailable at: \\url{{{m['url']}}}"

    return entry


def generate_latex(sid, sentences, ner_data):
    """Gera o documento LaTeX completo para uma fonte."""
    m      = SOURCES_META[sid]
    title  = latex_escape(m["title"])
    author = latex_escape(m["author"])

    abstract   = make_abstract(sentences)
    ner_sec    = make_ner_section(ner_data)
    bib_entry  = make_bibliography(sid)

    doc = rf"""\documentclass[12pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\usepackage[english]{{babel}}
\usepackage{{hyperref}}
\usepackage{{microtype}}
\usepackage{{geometry}}
\geometry{{margin=2.5cm}}

\title{{\textbf{{{title}}}}}
\author{{{author} \\\\
\small SPLN --- 2025/26}}
\date{{{m['year']}}}

\begin{{document}}

\maketitle

% ── Abstract ──────────────────────────────────────────────────
\begin{{abstract}}
{abstract}
\end{{abstract}}

% ── Named Entity Recognition ──────────────────────────────────
\section{{Named Entity Recognition}}

The following named entities were automatically identified in the source
text using the spaCy NLP library with the \texttt{{en\_core\_web\_sm}} model.

{ner_sec}

% ── Source Information ────────────────────────────────────────
\section{{Source Information}}

This article was produced from the following
source~\cite{{{m['bibkey']}}}:

\begin{{itemize}}
  \item \textbf{{Title:}} \textit{{{title}}}
  \item \textbf{{Author(s):}} {author}
  \item \textbf{{Year:}} {m['year']}
  \item \textbf{{Publisher:}} {latex_escape(m['publisher'])}
\end{{itemize}}

% ── Bibliography ──────────────────────────────────────────────
\begin{{thebibliography}}{{9}}
{bib_entry}
\end{{thebibliography}}

\end{{document}}
"""
    return doc


def compile_latex(tex_path):
    """Compila um ficheiro .tex para PDF com pdflatex."""
    out_dir = os.path.dirname(tex_path)
    for _ in range(2):  # duas passagens para referências
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode",
             "-output-directory", out_dir, tex_path],
            capture_output=True, text=True
        )
    # Limpa ficheiros auxiliares
    base = os.path.splitext(tex_path)[0]
    for ext in [".aux", ".log", ".out"]:
        if os.path.exists(base + ext):
            os.remove(base + ext)

    pdf_path = base + ".pdf"
    return pdf_path if os.path.exists(pdf_path) else None


def main():
    print("=" * 60)
    print("  PASSO E) - Geração de Artigos LaTeX")
    print("=" * 60)

    # Carrega frases e NER
    with open(SCORES_FILE, encoding="utf-8") as f:
        scores = json.load(f)
    with open(NER_FILE, encoding="utf-8") as f:
        ner_all = json.load(f)

    os.makedirs(LATEX_DIR, exist_ok=True)

    pdfs = []
    for sid in SOURCES_META:
        print(f"\n--- {sid} ---")

        if sid not in scores:
            print("  AVISO: sem frases scored para esta fonte.")
            continue
        if sid not in ner_all:
            print("  AVISO: sem NER para esta fonte.")
            continue

        # Gera LaTeX
        tex_content = generate_latex(sid, scores[sid], ner_all[sid])
        tex_path = os.path.join(LATEX_DIR, f"{sid}.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)
        print(f"  .tex gerado: {tex_path}")

        # Compila para PDF
        print(f"  A compilar PDF...")
        pdf_path = compile_latex(tex_path)
        if pdf_path:
            size_kb = os.path.getsize(pdf_path) / 1024
            print(f"  ✓ PDF gerado: {pdf_path} ({size_kb:.1f} KB)")
            pdfs.append(pdf_path)
        else:
            print(f"  ✗ Falha na compilação do PDF")

    print(f"\n{'='*60}")
    print(f"  {len(pdfs)}/4 PDFs gerados com sucesso")
    if pdfs:
        print("\n  Ficheiros PDF:")
        for p in pdfs:
            print(f"    {p}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()