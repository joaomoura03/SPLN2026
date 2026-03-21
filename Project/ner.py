"""
ner.py
------
Usa a ferramenta spaCy para fazer NER (Named Entity Recognition)
e identificar as entidades nomeadas presentes em cada fonte.

Categorias identificadas pelo modelo en_core_web_sm:
    PERSON  - pessoas (artistas, músicos, autores)
    ORG     - organizações (bandas, gravadoras, instituições)
    GPE     - locais geopolíticos (países, cidades)
    DATE    - datas e períodos de tempo
    WORK_OF_ART - títulos de obras (músicas, álbuns, livros)
"""

import os
import json
import spacy

TEXTS_DIR = os.path.join(os.path.dirname(__file__), "texts")
NER_DIR   = os.path.join(os.path.dirname(__file__), "ner")
SOURCE_IDS = ["kajanova", "larson", "short_history", "wikipedia"]

# Categorias de entidades que nos interessam
LABELS = ["PERSON", "ORG", "GPE", "DATE", "WORK_OF_ART"]


def load_text(source_id):
    path = os.path.join(TEXTS_DIR, f"{source_id}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_ner(nlp, text):
    """
    Corre o NER do spaCy no texto e devolve as entidades
    agrupadas por categoria.
    """
    # Processa em chunks para evitar problemas com textos longos
    max_len = 100000
    all_ents = {label: set() for label in LABELS}

    for i in range(0, len(text), max_len):
        chunk = text[i:i + max_len]
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ in LABELS:
                # Limpa espaços e ignora entidades muito curtas
                cleaned = ent.text.strip()
                if len(cleaned) > 1:
                    all_ents[ent.label_].add(cleaned)

    # Converte sets para listas ordenadas
    return {label: sorted(ents) for label, ents in all_ents.items() if ents}


def main():
    print("=" * 50)
    print("PASSO D) - NER com spaCy")
    print("=" * 50)

    # Carrega o modelo de inglês
    print("\nA carregar modelo spaCy (en_core_web_sm)...")
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("ERRO: Modelo não encontrado. Instala com:")
        print("  python3 -m spacy download en_core_web_sm")
        return

    print(f"Modelo carregado: {nlp.meta['name']} v{nlp.meta['version']}")

    os.makedirs(NER_DIR, exist_ok=True)
    results = {}

    for sid in SOURCE_IDS:
        print(f"\n--- {sid} ---")
        text = load_text(sid)
        ents = run_ner(nlp, text)
        results[sid] = ents

        for label, items in ents.items():
            print(f"  {label} ({len(items)}): {items[:5]}{'...' if len(items) > 5 else ''}")

    # Guarda resultados
    out_path = os.path.join(NER_DIR, "ner_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResultados NER guardados em: {out_path}")


if __name__ == "__main__":
    main()