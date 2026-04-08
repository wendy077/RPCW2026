# RPCW2026 - Ficha Medicina

## Metainformação

- **Título:** Ficha Medicina
- **Data:** Março 2026  
- **Autor:**  
  - **Id:** PG61534  
  - **Nome:** Mariana Pinto  

## Objetivo

O objetivo deste trabalho foi povoar uma ontologia médica em RDF/OWL a partir de vários datasets fornecidos com o enunciado, gerar versões intermédias e finais da ontologia em Turtle, importar a ontologia final no GraphDB e desenvolver queries SPARQL para interrogação e diagnóstico automático de doentes.

Foram utilizados os seguintes ficheiros de entrada:

* `medical.ttl`
* `Disease_Syntoms.csv`
* `Disease_Description.csv`
* `Disease_Treatment.csv`
* `doentes.json`

No final foram produzidos os ficheiros:

* `output/med_doencas.ttl`
* `output/med_tratamentos.ttl`
* `output/med_doentes.ttl`
* `sparql.txt`

---

## Estrutura do projeto

```text
data/
├── Disease_Description.csv
├── Disease_Syntoms.csv
├── Disease_Treatment.csv
├── doentes.json
└── medical.ttl

scripts/
└── povoar_med.py

output/
├── med_doencas.ttl
├── med_tratamentos.ttl
└── med_doentes.ttl

PR.md
sparql.txt
```

---

## Abordagem adotada

A solução foi implementada em Python com recurso às bibliotecas `rdflib` e `pandas`.

O processo seguiu estas etapas:

1. Carregamento da ontologia base `medical.ttl`.
2. Remoção das instâncias de exemplo já existentes na ontologia base, mantendo apenas a estrutura da ontologia, ou seja, classes e propriedades.
3. Criação programática das propriedades de dados `:name` e `:description`.
4. Povoamento das doenças e sintomas a partir de `Disease_Syntoms.csv`.
5. Associação das descrições às doenças a partir de `Disease_Description.csv`.
6. Gravação do ficheiro intermédio `med_doencas.ttl`.
7. Associação dos tratamentos às doenças a partir de `Disease_Treatment.csv`.
8. Gravação do ficheiro intermédio `med_tratamentos.ttl`.
9. Criação dos pacientes e associação dos seus sintomas a partir de `doentes.json`.
10. Gravação do ficheiro final `med_doentes.ttl`.
11. Importação da ontologia final no GraphDB.
12. Execução das queries SPARQL pedidas no enunciado.
13. Diagnóstico automático dos doentes através de uma query `CONSTRUCT` e posterior `INSERT` dos triplos `:hasDisease` na ontologia.

---

## Normalização dos dados

Durante o desenvolvimento verificou-se que os datasets continham inconsistências nos identificadores, por exemplo:

* diferenças entre maiúsculas e minúsculas
* espaços extra
* underscores separados por espaços
* pequenas variações ortográficas

Para garantir consistência semântica na ontologia final, foi aplicada uma normalização aos identificadores de doenças, sintomas e tratamentos. Essa normalização incluiu:

* remoção de espaços redundantes
* substituição de espaços por underscores
* conversão para minúsculas
* compressão de underscores repetidos
* correção manual de alguns casos problemáticos

Exemplos de correções aplicadas:

* `dimorphic_hemmorhoidspiles` → `dimorphic_hemorrhoidspiles`
* `spotting_ urination` → `spotting_urination`
* `foul_smell_of urine` → `foul_smell_of_urine`
* `dischromic _patches` → `dischromic_patches`

Esta etapa foi importante para evitar duplicação de recursos e resultados incorretos na inferência SPARQL.

---

## Remoção das instâncias seed da ontologia base

A ontologia base `medical.ttl` continha algumas instâncias de exemplo, nomeadamente doenças, sintomas, tratamentos e pacientes de teste.

Como o objetivo era povoar a ontologia a partir dos datasets fornecidos, essas instâncias foram removidas antes do processamento dos dados. Esta decisão foi tomada para evitar:

* duplicação entre instâncias de exemplo e instâncias geradas a partir dos datasets
* contagens incorretas em queries de agregação
* interferência na inferência de diagnósticos

Desta forma, a ontologia final ficou coerente e baseada apenas nos dados efetivamente fornecidos para o exercício.

---

## Script de povoamento

O ficheiro `scripts/povoar_med.py` implementa toda a lógica do processo.

Principais funções implementadas:

* `clean_text()` – limpeza de texto
* `norm_token()` – normalização dos identificadores RDF
* `patient_id()` – geração de IDs únicos para pacientes
* `remove_seed_instances()` – remoção das instâncias de exemplo da ontologia base
* `ensure_datatype_properties()` – criação das propriedades de dados
* `populate_diseases_symptoms()` – povoamento de doenças e sintomas
* `add_descriptions()` – associação de descrições às doenças
* `populate_treatments()` – associação de tratamentos às doenças
* `populate_patients()` – criação dos pacientes e seus sintomas

---

## Execução

### Instalação de dependências

```bash
pip install rdflib pandas
```

### Execução do script

```bash
python scripts/povoar_med.py
```

### Resultado esperado

O script gera os seguintes ficheiros:

```text
output/med_doencas.ttl
output/med_tratamentos.ttl
output/med_doentes.ttl
```

---

## Importação no GraphDB

Foi criado um novo repositório no GraphDB e importado o ficheiro final:

```text
output/med_doentes.ttl
```

Depois da importação foram executadas queries de validação para confirmar:

* número de doenças
* número de pacientes
* consistência dos identificadores
* presença correta das relações `:hasSymptom`, `:hasTreatment` e `:exhibitsSymptom`

---

## Queries SPARQL

Todas as queries desenvolvidas foram guardadas no ficheiro `sparql.txt`, devidamente identificadas.

As queries respondem às questões pedidas no enunciado:

* número de doenças presentes na ontologia
* doenças associadas ao sintoma `yellowish_skin`
* doenças associadas ao tratamento `exercise`
* lista ordenada alfabeticamente com os nomes dos doentes
* `CONSTRUCT` para inferência de diagnósticos
* `INSERT` para acrescentar diagnósticos ao grafo
* distribuição dos doentes pelas doenças
* distribuição das doenças pelos sintomas
* distribuição das doenças pelos tratamentos
* lista das doenças e respetivos sintomas

---

## Diagnóstico automático

Para diagnosticar automaticamente os doentes foi usada uma query SPARQL `CONSTRUCT` com a seguinte lógica:

Um paciente é associado a uma doença quando todos os sintomas dessa doença estão presentes nos sintomas exibidos pelo paciente.

Depois disso, foi usada uma query `INSERT` para acrescentar ao grafo os triplos com a forma:

```ttl
:patientX :hasDisease :diseaseY .
```

Foi também acrescentada a condição `FILTER EXISTS` para impedir que doenças sem sintomas fossem atribuídas indevidamente a todos os doentes.

---

## Resultados principais

Depois da correção e normalização final dos dados, obtiveram-se os seguintes resultados:

* número de doenças: **41**
* número de pacientes: **10000**
* número de diagnósticos inferidos: **6558**

Alguns resultados relevantes observados nas queries:

* doença com mais doentes diagnosticados: `heart_attack` com **361** doentes
* sintoma associado ao maior número de doenças: `vomiting` e `fatigue`, ambos presentes em **17** doenças
* tratamento mais partilhado por doenças: `consult_doctor`, presente em **15** doenças

---

## Conclusão

O objetivo da ficha foi cumprido.

A ontologia médica foi povoada com sucesso a partir dos datasets fornecidos, foram geradas versões intermédias e finais em Turtle, a ontologia foi importada no GraphDB, e as queries SPARQL pedidas no enunciado foram implementadas e testadas.

Além disso, foi criada uma inferência automática de diagnósticos com base nos sintomas dos doentes, sendo os respetivos triplos adicionados ao grafo final.
