# TPC6 — Biblioteca Temporal (Linhas Temporais)

## Metainformação

- **Título:** TPC6 — Extensão da Aplicação Web com Linhas Temporais  
- **Data:** 2026  
- **Autor:**  
  - **Id:** PG61534  
  - **Nome:** Mariana Pinto  

## Resumo

Este trabalho consiste na evolução da aplicação desenvolvida no **TPC5**, adicionando suporte à exploração explícita das **linhas temporais** presentes no dataset *Biblioteca Temporal*.

A aplicação foi implementada em **Python com Flask**, comunicando com um repositório **GraphDB** através de **queries SPARQL**.  
O objetivo principal foi introduzir uma nova dimensão de navegação baseada no tempo, permitindo relacionar livros com diferentes linhas temporais.

---

## Funcionalidades implementadas

### 1. Listagem de linhas temporais

- **Rota:** `/linhas`

Apresenta todas as linhas temporais existentes no dataset.

Para cada linha são mostrados:

- identificador
- tipo de linha:
  - Original
  - Alternativa
  - Temporal

Foi implementada lógica em SPARQL para:

- evitar duplicação de linhas
- escolher o tipo mais relevante quando existem múltiplos (`LinhaOriginal > LinhaAlternativa > LinhaTemporal`)

---

### 2. Detalhe de linha temporal

- **Rota:** `/linha/<id>`

Apresenta:

- tipo da linha
- lista de livros existentes nessa linha

Para cada livro são apresentados:

- título
- tipo(s) de livro

Quando um livro possui múltiplos tipos RDF (por exemplo *Ficcional* e *Paradoxal*), esses tipos são:

- agregados com `GROUP_CONCAT`
- apresentados em conjunto na interface

---

### 3. Integração com livros

Na página de cada livro (`/livro/<id>`):

- as linhas temporais passaram a ser **clicáveis**
- permitem navegar diretamente para `/linha/<id>`

Isto cria navegação bidirecional:

- Livro → Linha
- Linha → Livro

---

## Aspetos técnicos relevantes

- Uso de **SPARQL com agregação (`GROUP_CONCAT`)** para:
  - juntar múltiplos tipos de um mesmo livro
  - evitar duplicação de resultados
  - representar relações muitos-para-muitos

- Uso de **subqueries SPARQL** para:
  - agrupar corretamente os tipos por livro
  - garantir consistência dos dados apresentados

- Uso da propriedade:
  - `:existeEm` (Livro → Linha Temporal)

- Transformação dos resultados SPARQL em estruturas Python adaptadas aos templates HTML

---

## Estrutura do projeto

```
TPC6/
├── app.py
├── query.py
├── requirements.txt
└── templates/
    ├── layout.html
    ├── livros.html
    ├── livro.html
    ├── eventos.html
    ├── evento.html
    ├── linhas.html
    ├── linha.html
    └── 404.html
```

---

## Templates adicionados

- **`linhas.html`**  
  Lista todas as linhas temporais

- **`linha.html`**  
  Página de detalhe de uma linha temporal com os livros associados

---

## Conclusão

A aplicação passou a suportar uma nova dimensão de exploração baseada em **linhas temporais**, permitindo uma navegação mais rica sobre o dataset RDF.

Este TPC demonstra:

- integração entre Flask e GraphDB
- utilização de SPARQL em cenários com relações complexas
- tratamento de dados RDF com múltiplas classificações

A aplicação final permite explorar livros, eventos e linhas temporais de forma interligada e consistente.
