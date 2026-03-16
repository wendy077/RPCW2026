from flask import Flask, render_template, abort
from query import run_query

app = Flask(__name__)

TYPE_META = {
    "LivroHistorico": {"label": "Histórico", "color": "w3-blue"},
    "LivroFiccional": {"label": "Ficcional", "color": "w3-purple"},
    "LivroParadoxal": {"label": "Paradoxal", "color": "w3-red"},
}


def humanize_identifier(value: str) -> str:
    return value.replace("_", " ")


def split_grouped_pairs(raw: str, item_sep: str = "||", pair_sep: str = "::"):
    if not raw:
        return []

    items = []
    for block in raw.split(item_sep):
        if not block:
            continue
        if pair_sep in block:
            item_id, label = block.split(pair_sep, 1)
        else:
            item_id, label = block, block
        items.append({"id": item_id, "label": label or humanize_identifier(item_id)})
    return items


def normalize_book_type(raw_type: str):
    meta = TYPE_META.get(raw_type, {"label": raw_type, "color": "w3-grey"})
    return {"id": raw_type, "label": meta["label"], "color": meta["color"]}


@app.route("/")
@app.route("/livros")
def livros():
    query = """
    PREFIX : <http://example.org/biblioteca-temporal#>

    SELECT ?id ?titulo ?tipo ?autor ?pais WHERE {
        ?livro a ?tipoURI ;
               :titulo ?titulo ;
               :escritoPor ?autorRef .

        ?autorRef :nome ?autor ;
                  :paisOrigem ?pais .

        FILTER(?tipoURI IN (:LivroHistorico, :LivroFiccional, :LivroParadoxal))

        BIND(STRAFTER(STR(?livro), "#") AS ?id)
        BIND(STRAFTER(STR(?tipoURI), "#") AS ?tipo)
    }
    ORDER BY LCASE(?titulo)
    """

    data = run_query(query)
    livros = []

    for row in data["results"]["bindings"]:
        tipo = normalize_book_type(row["tipo"]["value"])
        livros.append(
            {
                "id": row["id"]["value"],
                "titulo": row["titulo"]["value"],
                "tipo": tipo["label"],
                "color": tipo["color"],
                "autor": row["autor"]["value"],
                "pais": row["pais"]["value"],
            }
        )

    return render_template("livros.html", livros=livros, total=len(livros))


@app.route("/livro/<livro_id>")
def livro_detail(livro_id):
    query = f"""
    PREFIX : <http://example.org/biblioteca-temporal#>

    SELECT ?titulo ?tipo ?autor ?pais ?biblioteca
           (GROUP_CONCAT(DISTINCT STRAFTER(STR(?linha), "#"); separator="|") AS ?linhas)
           (GROUP_CONCAT(DISTINCT CONCAT(STRAFTER(STR(?evento), "#"), "::", ?eventoNome); separator="||") AS ?eventos)
    WHERE {{
        :{livro_id} a ?tipoURI ;
                    :titulo ?titulo ;
                    :escritoPor ?autorRef ;
                    :pertenceA ?bibliotecaRef .

        ?autorRef :nome ?autor ;
                  :paisOrigem ?pais .

        OPTIONAL {{ :{livro_id} :existeEm ?linha . }}
        OPTIONAL {{
            :{livro_id} :refereEvento ?evento .
            ?evento :designacao ?eventoNome .
        }}

        BIND(STRAFTER(STR(?tipoURI), "#") AS ?tipo)
        BIND(STRAFTER(STR(?bibliotecaRef), "#") AS ?biblioteca)
    }}
    GROUP BY ?titulo ?tipo ?autor ?pais ?biblioteca
    """

    data = run_query(query)
    bindings = data["results"]["bindings"]
    if not bindings:
        abort(404)

    row = bindings[0]
    tipo = normalize_book_type(row["tipo"]["value"])

    livro = {
        "id": livro_id,
        "titulo": row["titulo"]["value"],
        "tipo": tipo["label"],
        "color": tipo["color"],
        "autor": row["autor"]["value"],
        "pais": row["pais"]["value"],
        "biblioteca": humanize_identifier(row["biblioteca"]["value"]),
        "linhas": [humanize_identifier(v) for v in row.get("linhas", {}).get("value", "").split("|") if v],
        "eventos": split_grouped_pairs(row.get("eventos", {}).get("value", "")),
    }

    return render_template("livro.html", livro=livro)

@app.route("/eventos")
def eventos():
    query = """
    PREFIX : <http://example.org/biblioteca-temporal#>

    SELECT ?id ?designacao (SAMPLE(?descricao) AS ?descricao)
           (GROUP_CONCAT(DISTINCT CONCAT(STRAFTER(STR(?livro), "#"), "::", ?tituloLivro); separator="||") AS ?livros)
    WHERE {
        ?evento :designacao ?designacao .
        BIND(STRAFTER(STR(?evento), "#") AS ?id)

        OPTIONAL { ?evento :descricao ?descricao . }
        OPTIONAL {
            ?livro :refereEvento ?evento ;
                   :titulo ?tituloLivro .
        }
    }
    GROUP BY ?id ?designacao
    ORDER BY LCASE(?designacao)
    """

    data = run_query(query)
    eventos = []

    for row in data["results"]["bindings"]:
        eventos.append(
            {
                "id": row["id"]["value"],
                "designacao": row["designacao"]["value"],
                "descricao": row.get("descricao", {}).get("value", "Sem descrição disponível."),
                "livros": split_grouped_pairs(row.get("livros", {}).get("value", "")),
            }
        )

    return render_template("eventos.html", eventos=eventos, total=len(eventos))


@app.route("/evento/<evento_id>")
def evento_detail(evento_id):
    query = f"""
    PREFIX : <http://example.org/biblioteca-temporal#>

    SELECT ?designacao (SAMPLE(?descricao) AS ?descricao)
           (GROUP_CONCAT(DISTINCT CONCAT(STRAFTER(STR(?livro), "#"), "::", ?tituloLivro); separator="||") AS ?livros)
    WHERE {{
        :{evento_id} :designacao ?designacao .
        OPTIONAL {{ :{evento_id} :descricao ?descricao . }}
        OPTIONAL {{
            ?livro :refereEvento :{evento_id} ;
                   :titulo ?tituloLivro .
        }}
    }}
    GROUP BY ?designacao
    """

    data = run_query(query)
    bindings = data["results"]["bindings"]
    if not bindings:
        abort(404)

    row = bindings[0]
    evento = {
        "id": evento_id,
        "designacao": row["designacao"]["value"],
        "descricao": row.get("descricao", {}).get("value", "Sem descrição disponível."),
        "livros": split_grouped_pairs(row.get("livros", {}).get("value", "")),
    }

    return render_template("evento.html", evento=evento)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
