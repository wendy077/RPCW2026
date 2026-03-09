import json
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal
from rdflib.namespace import XSD

BASE = "http://rpcw.di.uminho.pt/2026/biblioteca-temporal#"
NS = Namespace(BASE)

INPUT_FILES = [
    "dataset_temporal_100.json",
    "dataset_temporal_v2_100.json"
]

OUTPUT_FILE = "datasets.ttl"


def add_value(g: Graph, subj, pred, value):
    if isinstance(value, list):
        for v in value:
            add_value(g, subj, pred, v)
    elif isinstance(value, str):
        g.add((subj, pred, NS[value]))


def main():
    g = Graph()
    g.bind("", NS)

    for filename in INPUT_FILES:
        path = Path(filename)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            subj = NS[item["id"]]

            if "tipo" in item:
                g.add((subj, RDF.type, NS[item["tipo"]]))

            for key, value in item.items():
                if key in {"id", "tipo"}:
                    continue

                if key == "nome":
                    g.add((subj, NS.nome, Literal(value, datatype=XSD.string)))
                else:
                    add_value(g, subj, NS[key], value)

    g.serialize(destination=OUTPUT_FILE, format="turtle")
    print(f"Ficheiro gerado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()