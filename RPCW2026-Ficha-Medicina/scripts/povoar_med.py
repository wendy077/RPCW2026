from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal
import pandas as pd
import json
import re
import unicodedata
from pathlib import Path

BASE = "http://www.example.org/disease-ontology#"
NS = Namespace(BASE)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output"

def clean_text(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    s = " ".join(s.split())
    return s

def norm_token(s: str) -> str:
    s = clean_text(s)
    s = s.replace(" _", "_").replace("_ ", "_")
    s = s.replace(" ", "_")
    s = s.replace("(", "").replace(")", "")
    s = s.replace(",", "")
    s = s.replace("/", "_")
    s = s.replace("-", "_")
    s = s.lower()
    s = re.sub(r"_+", "_", s)

    corrections = {
        "dimorphic_hemmorhoidspiles": "dimorphic_hemorrhoidspiles",
        "dischromic_patches": "dischromic_patches",
        "spotting_urination": "spotting_urination",
        "foul_smell_of_urine": "foul_smell_of_urine",
    }

    return corrections.get(s, s)

def patient_id(i: int, nome: str) -> str:
    base = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")
    return f"Patient_{i:03d}_{base}"

def ensure_datatype_properties(g: Graph):
    g.add((NS.description, RDF.type, OWL.DatatypeProperty))
    g.add((NS.description, RDFS.domain, NS.Disease))
    g.add((NS.description, RDFS.range, XSD.string))

    g.add((NS.name, RDF.type, OWL.DatatypeProperty))
    g.add((NS.name, RDFS.domain, NS.Patient))
    g.add((NS.name, RDFS.range, XSD.string))

def add_disease(g: Graph, disease_name: str):
    d = NS[norm_token(disease_name)]
    g.add((d, RDF.type, NS.Disease))
    return d

def add_symptom(g: Graph, symptom_name: str):
    s = NS[norm_token(symptom_name)]
    g.add((s, RDF.type, NS.Symptom))
    return s

def add_treatment(g: Graph, treatment_name: str):
    t = NS[norm_token(treatment_name)]
    g.add((t, RDF.type, NS.Treatment))
    return t

def populate_diseases_symptoms(g: Graph):
    df = pd.read_csv(DATA / "Disease_Syntoms.csv")
    symptom_cols = [c for c in df.columns if c.lower().startswith("symptom")]

    for _, row in df.iterrows():
        disease = clean_text(row["Disease"])
        if not disease:
            continue

        d = add_disease(g, disease)

        for col in symptom_cols:
            val = row.get(col)
            if pd.isna(val):
                continue
            symptom = clean_text(val)
            if not symptom:
                continue
            s = add_symptom(g, symptom)
            g.add((d, NS.hasSymptom, s))

def add_descriptions(g: Graph):
    df = pd.read_csv(DATA / "Disease_Description.csv")
    for _, row in df.iterrows():
        disease = clean_text(row["Disease"])
        desc = clean_text(row["Description"])
        if disease and desc:
            d = add_disease(g, disease)
            g.set((d, NS.description, Literal(desc, datatype=XSD.string)))

def populate_treatments(g: Graph):
    df = pd.read_csv(DATA / "Disease_Treatment.csv")
    treatment_cols = [c for c in df.columns if c.lower().startswith("precaution")]

    for _, row in df.iterrows():
        disease = clean_text(row["Disease"])
        if not disease:
            continue

        d = add_disease(g, disease)

        for col in treatment_cols:
            val = row.get(col)
            if pd.isna(val):
                continue
            treatment = clean_text(val)
            if not treatment:
                continue
            t = add_treatment(g, treatment)
            g.add((d, NS.hasTreatment, t))

def populate_patients(g: Graph):
    with open(DATA / "doentes.json", "r", encoding="utf-8") as f:
        patients = json.load(f)

    for i, p in enumerate(patients, start=1):
        nome = clean_text(p["nome"])
        pid = NS[patient_id(i, nome)]

        g.add((pid, RDF.type, NS.Patient))
        g.set((pid, NS.name, Literal(nome, datatype=XSD.string)))

        for sym in p.get("sintomas", []):
            symptom = clean_text(sym)
            if not symptom:
                continue
            s = add_symptom(g, symptom)
            g.add((pid, NS.exhibitsSymptom, s))

def remove_seed_instances(g: Graph):
    instance_classes = [NS.Disease, NS.Symptom, NS.Treatment, NS.Patient]

    for cls in instance_classes:
        subjects = list(g.subjects(RDF.type, cls))
        for subj in subjects:
            for triple in list(g.triples((subj, None, None))):
                g.remove(triple)
            for triple in list(g.triples((None, None, subj))):
                g.remove(triple)

def main():
    OUT.mkdir(exist_ok=True)

    g = Graph()
    g.parse(DATA / "medical.ttl", format="turtle")
    g.bind("", NS)

    remove_seed_instances(g)
    ensure_datatype_properties(g)
    populate_diseases_symptoms(g)
    add_descriptions(g)
    g.serialize(OUT / "med_doencas.ttl", format="turtle")

    populate_treatments(g)
    g.serialize(OUT / "med_tratamentos.ttl", format="turtle")

    populate_patients(g)
    g.serialize(OUT / "med_doentes.ttl", format="turtle")

    print("Gerados:")
    print("-", OUT / "med_doencas.ttl")
    print("-", OUT / "med_tratamentos.ttl")
    print("-", OUT / "med_doentes.ttl")

if __name__ == "__main__":
    main()