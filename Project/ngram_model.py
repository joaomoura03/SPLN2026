"""
ngram_model.py
--------------
Tokeniza o texto das fontes e constrói um modelo de linguagem
baseado em trigramas (n=3), treinado no corpus completo
(todas as fontes combinadas).

Segue o mesmo padrão das aulas (exerciciodaaula.py / n-gramtutorial.py)
usando nltk para tokenização e construção dos n-grams.
"""

import os
import json
import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

# Download dos recursos necessários do nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

TEXTS_DIR = os.path.join(os.path.dirname(__file__), "texts")
SOURCE_IDS = ["kajanova", "larson", "short_history", "wikipedia"]
NGRAMS_DIR = os.path.join(os.path.dirname(__file__), "ngrams")

# Tamanho do n-gram (trigrama)
N = 3


def load_text(source_id):
    """Carrega o texto limpo de uma fonte."""
    path = os.path.join(TEXTS_DIR, f"{source_id}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tokenize(text):
    """Tokeniza o texto em palavras usando nltk."""
    tokens = word_tokenize(text)
    # Converte para lowercase e filtra tokens não-alfabéticos
    tokens = [t.lower() for t in tokens if t.isalpha()]
    return tokens


def build_ngram_model(tokens, n=3):
    """
    Constrói um modelo de n-gramas com probabilidades de transição.
    Igual ao padrão do exerciciodaaula.py.
    """
    n_grams = list(ngrams(tokens, n))
    model = defaultdict(lambda: defaultdict(int))

    # Conta as ocorrências de cada n-grama
    for gram in n_grams:
        prefix = tuple(gram[:-1])
        next_word = gram[-1]
        model[prefix][next_word] += 1

    # Converte as frequências em probabilidades
    for prefix in model:
        total_count = float(sum(model[prefix].values()))
        for next_word in model[prefix]:
            model[prefix][next_word] /= total_count

    return model


def predict_next_word(model, prefix):
    """
    Prevê a próxima palavra dado um prefixo.
    Igual ao padrão do exerciciodaaula.py.
    """
    next_word_probs = model[tuple(prefix)]
    if next_word_probs:
        return max(next_word_probs, key=next_word_probs.get)
    else:
        return "No prediction available"


def main():
    # 1. Carregar e tokenizar todos os textos
    print("=" * 50)
    print("PASSO B) - Tokenização e Modelo de N-gramas")
    print("=" * 50)

    all_tokens = []
    source_tokens = {}

    for sid in SOURCE_IDS:
        text = load_text(sid)
        tokens = tokenize(text)
        source_tokens[sid] = tokens
        all_tokens.extend(tokens)
        print(f"\n{sid}:")
        print(f"  Tokens totais:  {len(tokens)}")
        print(f"  Vocab único:    {len(set(tokens))}")
        print(f"  Primeiros 10:   {tokens[:10]}")

    print(f"\nCorpus completo: {len(all_tokens)} tokens | {len(set(all_tokens))} únicos")

    # 2. Construir modelo de trigramas no corpus completo
    print(f"\nConstruindo modelo de {N}-gramas no corpus completo...")
    model = build_ngram_model(all_tokens, n=N)
    print(f"  Contextos únicos (bigramas): {len(model)}")

    # 3. Exemplos de previsão
    print("\nExemplos de previsão de próxima palavra:")
    exemplos = [
        ["rock", "and"],
        ["rhythm", "and"],
        ["the", "history"],
        ["electric", "guitar"],
        ["jazz", "and"],
    ]
    for prefix in exemplos:
        next_w = predict_next_word(model, prefix)
        print(f"  '{' '.join(prefix)} ___' -> '{next_w}'")

    # 4. Guardar modelo e tokens para uso nos passos seguintes
    model_serializable = {
        str(k): v for k, v in model.items()
    }
    out_model = os.path.join(NGRAMS_DIR, "ngram_model.json")
    with open(out_model, "w", encoding="utf-8") as f:
        json.dump(model_serializable, f, ensure_ascii=False, indent=2)
    print(f"\nModelo guardado em: {out_model}")

    out_tokens = os.path.join(NGRAMS_DIR, "source_tokens.json")
    with open(out_tokens, "w", encoding="utf-8") as f:
        json.dump(source_tokens, f, ensure_ascii=False)
    print(f"Tokens guardados em: {out_tokens}")

    return model, source_tokens


if __name__ == "__main__":
    main()