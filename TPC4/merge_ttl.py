import rdflib

g = rdflib.Graph()

# carrega a ontologia base
g.parse("biblioteca_temporal.ttl", format="turtle")

# carrega os datasets já convertidos
g.parse("datasets.ttl", format="turtle")

# grava tudo num só ficheiro
g.serialize(destination="biblioteca_temporal_com_datasets.ttl", format="turtle")

print("Ficheiro criado: biblioteca_temporal_com_datasets.ttl")
print(f"Número total de triplos: {len(g)}")