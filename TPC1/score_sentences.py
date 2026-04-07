"""
score_sentences.py
------------------
Usa o modelo de trigramas construído em ngram_model.py para fazer
o scoring de cada frase de cada fonte e selecionar as 3 melhores.

Método de scoring:
    Para cada frase, calcula a média das log-probabilidades absolutas
    dos trigramas que a compõem:

        score(frase) = mean( log P(trigrama) )
        P(trigrama) = count(trigrama) / total_trigramas

    Frases com score mais alto são aquelas cujos trigramas aparecem
    mais frequentemente no corpus — ou seja, as frases mais
    representativas de cada fonte.

    Para trigramas não vistos usa fallback de 1/|V|.
"""

import os
import re
import json
import math
from collections import defaultdict
from nltk import ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

TEXTS_DIR = os.path.join(os.path.dirname(__file__), "texts")
SOURCE_IDS = ["kajanova", "larson", "short_history", "wikipedia"]
SCORES_DIR = os.path.join(os.path.dirname(__file__), "scores")


def load_text(source_id):
    path = os.path.join(TEXTS_DIR, f"{source_id}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    tokens = word_tokenize(text)
    return [t.lower() for t in tokens if t.isalpha()]


def build_ngram_model(tokens, n=3):
    """
    Constrói modelo com probabilidades absolutas dos trigramas:
        P(trigrama) = count(trigrama) / total_trigramas
    """
    n_grams = list(ngrams(tokens, n))
    total = len(n_grams)
    counts = defaultdict(int)

    for gram in n_grams:
        counts[gram] += 1

    model = {gram: count / total for gram, count in counts.items()}

    return model, total


def get_sentences(text):
    """Divide o texto em frases usando nltk sent_tokenize."""
    sentences = sent_tokenize(text)
    sentences = [re.sub(r'\s+', ' ', s).strip() for s in sentences]
    sentences = [s for s in sentences if len(s.split()) >= 8]
    return sentences


def score_sentence(model, vocab_size, sentence, n=3):
    """
    Calcula o score de uma frase = média das log-probabilidades
    absolutas dos trigramas que a compõem.

    Frases cujos trigramas são mais frequentes no corpus
    têm score mais alto (menos negativo).
    """
    tokens = tokenize(sentence)
    if len(tokens) < n:
        return float('-inf')

    log_probs = []
    for gram in ngrams(tokens, n):
        prob = model.get(gram, 1 / vocab_size)
        log_probs.append(math.log(prob))

    return sum(log_probs) / len(log_probs)


def select_top3(model, vocab_size, sentences):
    """
    Seleciona as 3 frases com maior score garantindo diversidade
    (evita frases com mais de 60% de overlap de palavras).
    """
    scored = [(s, score_sentence(model, vocab_size, s)) for s in sentences]
    scored.sort(key=lambda x: x[1], reverse=True)

    selected = []
    for sentence, score in scored:
        if len(selected) >= 3:
            break
        words_s = set(tokenize(sentence))
        too_similar = False
        for sel_s, _ in selected:
            words_sel = set(tokenize(sel_s))
            overlap = len(words_s & words_sel) / max(len(words_s | words_sel), 1)
            if overlap > 0.6:
                too_similar = True
                break
        if not too_similar:
            selected.append((sentence, score))

    if len(selected) < 3:
        seen = {s for s, _ in selected}
        for sentence, score in scored:
            if len(selected) >= 3:
                break
            if sentence not in seen:
                selected.append((sentence, score))
                seen.add(sentence)

    return selected


def main():
    print("=" * 50)
    print("PASSO C) - Scoring e Seleção de Frases")
    print("=" * 50)

    print("\nA construir modelo de trigramas no corpus completo...")
    all_tokens = []
    source_texts = {}

    for sid in SOURCE_IDS:
        text = load_text(sid)
        source_texts[sid] = text
        all_tokens.extend(tokenize(text))

    vocab_size = len(set(all_tokens))
    model, total_trigrams = build_ngram_model(all_tokens, n=3)
    print(f"  Corpus: {len(all_tokens)} tokens | vocab: {vocab_size} únicas")
    print(f"  Trigramas únicos no modelo: {len(model)}")

    results = {}
    for sid in SOURCE_IDS:
        print(f"\n--- {sid} ---")
        sentences = get_sentences(source_texts[sid])
        print(f"  Total de frases: {len(sentences)}")

        top3 = select_top3(model, vocab_size, sentences)
        results[sid] = [{"sentence": s, "score": round(sc, 4)} for s, sc in top3]

        for i, (s, sc) in enumerate(top3, 1):
            print(f"  [{i}] score={sc:.4f}")
            print(f"       {s[:120]}...")

    os.makedirs(SCORES_DIR, exist_ok=True)
    out_path = os.path.join(SCORES_DIR, "scored_sentences.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResultados guardados em: {out_path}")


if __name__ == "__main__":
    main()