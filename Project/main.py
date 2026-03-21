"""
main.py
-------
Pipeline completo do projeto SPLN 2025/26.
Corre todos os passos em sequência:

    a) extractclean.py    - Extrai e limpa o texto das fontes
    b) ngram_model.py     - Tokeniza e constrói o modelo de n-gramas
    c) score_sentences.py - Faz o scoring e seleciona as 3 frases
    d) ner.py             - Análise NER com spaCy
    e) generate_latex.py  - Gera os artigos LaTeX e compila os PDFs

Uso:
    python3 main.py          -> corre todos os passos
    python3 main.py --from c -> corre a partir do passo c)
"""

import subprocess
import sys
import os
import time

SCRIPTS = [
    ("a", "extractclean.py",    "Extração e limpeza do texto"),
    ("b", "ngram_model.py",     "Tokenização e modelo de n-gramas"),
    ("c", "score_sentences.py", "Scoring e seleção de frases"),
    ("d", "ner.py",             "NER com spaCy"),
    ("e", "generate_latex.py",  "Geração dos artigos LaTeX e PDFs"),
]


def run_script(script_name, description, step):
    script_path = os.path.join(os.path.dirname(__file__), script_name)

    if not os.path.exists(script_path):
        print(f"  ERRO: ficheiro '{script_name}' não encontrado.")
        return False

    print(f"\n{'='*60}")
    print(f"  PASSO {step.upper()}) {description}")
    print(f"  Ficheiro: {script_name}")
    print(f"{'='*60}")

    start = time.time()
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=os.path.dirname(__file__)
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"\n  ✓ Passo {step.upper()}) concluído em {elapsed:.1f}s")
        return True
    else:
        print(f"\n  ✗ Passo {step.upper()}) falhou (código {result.returncode})")
        return False


def main():
    start_from = "a"
    if "--from" in sys.argv:
        idx = sys.argv.index("--from")
        if idx + 1 < len(sys.argv):
            start_from = sys.argv[idx + 1].lower()

    print("\n" + "="*60)
    print("  PIPELINE SPLN 2025/26 - História do Rock 'n' Roll")
    print("="*60)

    if start_from != "a":
        print(f"\n  A começar a partir do passo {start_from.upper()})")

    steps_to_run = [s for s in SCRIPTS if s[0] >= start_from]

    total_start = time.time()
    success_count = 0

    for step, script, description in steps_to_run:
        success = run_script(script, description, step)
        if success:
            success_count += 1
        else:
            print(f"\n  Pipeline interrompido no passo {step.upper()}).")
            break

    total_elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print(f"  PIPELINE CONCLUÍDO: {success_count}/{len(steps_to_run)} passos com sucesso")
    print(f"  Tempo total: {total_elapsed:.1f}s")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()