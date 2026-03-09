from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

from rdflib import Graph

PREFIXES = """
PREFIX : <http://rpcw.di.uminho.pt/2026/biblioteca-temporal#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
""".strip()

QUERIES: Dict[str, str] = {
    "Query 1 — Livros na linha original": PREFIXES + """

SELECT DISTINCT ?livro
WHERE {
  ?livro :existeEm ?linha .
  ?linha a :LinhaOriginal .
}
ORDER BY ?livro
""",
    "Query 2 — Livros em múltiplas linhas temporais": PREFIXES + """

SELECT ?livro (COUNT(?linha) AS ?numLinhas)
WHERE {
  ?livro :existeEm ?linha .
}
GROUP BY ?livro
HAVING (COUNT(?linha) > 1)
ORDER BY DESC(?numLinhas)
""",
    "Query 3 — Livros paradoxais": PREFIXES + """

SELECT ?livro
WHERE {
  ?livro a :LivroParadoxal .
}
ORDER BY ?livro
""",
    "Query 4 — LivroHistorico e eventos históricos": PREFIXES + """

SELECT ?livro ?evento
WHERE {
  ?livro a :LivroHistorico .
  ?livro :refereEvento ?evento .
  ?evento a :EventoHistorico .
}
ORDER BY ?livro ?evento
""",
    "Query 5 — Inconsistências semânticas": PREFIXES + """

SELECT ?livro ?evento
WHERE {
  ?livro a :LivroHistorico .
  ?livro :refereEvento ?evento .
  ?evento a :EventoFuturo .
}
ORDER BY ?livro ?evento
""",
    "Query 6 — Autores mais prolíficos": PREFIXES + """

SELECT ?autor (COUNT(?livro) AS ?numLivros)
WHERE {
  ?livro :escritoPor ?autor .
}
GROUP BY ?autor
ORDER BY DESC(?numLivros) ?autor
""",
    "Query 7 — Autores de livros paradoxais": PREFIXES + """

SELECT DISTINCT ?autor
WHERE {
  ?livro a :LivroParadoxal .
  ?livro :escritoPor ?autor .
}
ORDER BY ?autor
""",
    "Query 8 — Livros em linhas alternativas": PREFIXES + """

SELECT DISTINCT ?livro
WHERE {
  ?livro :existeEm ?linha .
  ?linha a :LinhaAlternativa .
}
ORDER BY ?livro
""",
    "Query 9 — Bibliotecários e biblioteca": PREFIXES + """

SELECT ?bibliotecario ?biblioteca
WHERE {
  ?bibliotecario a :Bibliotecario .
  ?bibliotecario :trabalhaEm ?biblioteca .
}
ORDER BY ?bibliotecario
""",
    "Query 10 — Livros escritos por Cronos": PREFIXES + """

SELECT ?livro ?linha
WHERE {
  ?livro :escritoPor :Cronos .
  ?livro :existeEm ?linha .
}
ORDER BY ?livro ?linha
""",
    "Bónus 1 — Livros que não referem nenhum evento": PREFIXES + """

SELECT ?livro
WHERE {
  ?livro :existeEm ?linha .
  FILTER NOT EXISTS { ?livro :refereEvento ?evento . }
}
ORDER BY ?livro
""",
    "Bónus 2 — Livros sem linha temporal associada": PREFIXES + """

SELECT ?livro
WHERE {
  ?livro :escritoPor ?autor .
  FILTER NOT EXISTS { ?livro :existeEm ?linha . }
}
ORDER BY ?livro
""",
    "Bónus 3 — Autores que são também leitores": PREFIXES + """

SELECT DISTINCT ?pessoa
WHERE {
  ?pessoa a :Autor .
  ?pessoa a :Leitor .
}
ORDER BY ?pessoa
""",
    "Validação — Autor é também leitor do mesmo livro na mesma linha temporal": PREFIXES + """

SELECT ?pessoa ?livro ?linha
WHERE {
  ?livro :escritoPor ?pessoa .

  ?emprestimo a :Emprestimo ;
              :temLeitor ?pessoa ;
              :temLivro ?livro ;
              :emLinhaTemporal ?linha .
}
ORDER BY ?pessoa ?livro ?linha
""",
}


def short(value) -> str:
    text = str(value)
    if "#" in text:
        return text.split("#")[-1]
    if "/" in text:
        return text.rsplit("/", 1)[-1]
    return text


def print_results(title: str, results) -> None:
    print(f"\n{'=' * 100}\n{title}\n{'=' * 100}")

    variables = [str(var) for var in results.vars]
    rows = list(results)

    if not rows:
        print("Sem resultados.")
        return

    print("Variáveis:", ", ".join(variables))
    print(f"Total de resultados: {len(rows)}\n")

    for idx, row in enumerate(rows, 1):
        values = [f"{var}={short(row[var])}" for var in variables]
        print(f"{idx:>3}. " + " | ".join(values))


def load_graph(ttl_path: Path) -> Graph:
    if not ttl_path.exists():
        raise FileNotFoundError(f"Ficheiro não encontrado: {ttl_path}")

    g = Graph()
    g.parse(ttl_path, format="turtle")
    return g


def main() -> int:
    default_file = Path("biblioteca_temporal_com_datasets.ttl")
    ttl_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_file

    try:
        graph = load_graph(ttl_path)
    except Exception as exc:
        print(f"Erro ao carregar a ontologia: {exc}")
        return 1

    print(f"Ficheiro carregado: {ttl_path}")
    print(f"Total de triplos no grafo: {len(graph)}")

    for title, query in QUERIES.items():
        try:
            results = graph.query(query)
            print_results(title, results)
        except Exception as exc:
            print(f"\n[ERRO] {title}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
