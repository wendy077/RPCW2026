# TPC5 — Biblioteca Temporal

## Metainformação
- **Título:** TPC5 — Aplicação Web sobre a Biblioteca Temporal  
- **Data:** 2026  
- **Autor:**  
  - **Id:** PG61534  
  - **Nome:** Mariana Pinto  

## Resumo

Este trabalho consiste no desenvolvimento de uma pequena aplicação web para exploração do dataset **Biblioteca Temporal**, previamente modelado em RDF.

A aplicação foi implementada em **Python com Flask** e comunica com um repositório **GraphDB** através de **queries SPARQL**. O objetivo é permitir navegar pelos livros e eventos existentes no dataset e explorar as relações entre estes elementos do domínio.

Os dados são obtidos diretamente do repositório RDF carregado no GraphDB (`bib_temp.ttl`) e apresentados através de templates HTML renderizados pelo Flask.

## Funcionalidades implementadas

A aplicação disponibiliza quatro rotas principais:

- `/` e `/livros`  
  apresentam o catálogo completo de livros existentes no dataset.

- `/livro/<id>`  
  apresenta a página individual de um livro, incluindo:
  - título
  - tipo de livro
  - autor
  - país de origem
  - biblioteca a que pertence
  - linhas temporais onde existe
  - eventos referidos pelo livro.

- `/eventos`  
  apresenta a lista de eventos existentes na base de conhecimento.

- `/evento/<id>`  
  apresenta a página individual de um evento, incluindo:
  - designação
  - descrição
  - lista de livros que referem esse evento.

A navegação entre livros e eventos é feita através de ligações diretas entre as páginas, permitindo explorar as relações definidas no dataset.

As queries SPARQL utilizadas recorrem a agregação (`GROUP_CONCAT`) para reunir relações muitos-para-muitos diretamente no resultado da query, simplificando o tratamento dos dados no lado da aplicação.

## Estrutura do projeto

A aplicação encontra-se organizada na pasta `TPC5`, contendo os seguintes ficheiros principais:

- **`app.py`**  
  Ficheiro principal da aplicação Flask.  
  Define as rotas da aplicação (`/livros`, `/livro/<id>`, `/eventos`, `/evento/<id>`) e faz a ligação entre os resultados das queries SPARQL e os templates HTML que são apresentados ao utilizador.

- **`query.py`**  
  Contém as funções auxiliares responsáveis por executar queries SPARQL sobre o repositório GraphDB.  
  Este módulo trata da comunicação com o endpoint SPARQL e devolve os resultados já estruturados para serem utilizados pela aplicação Flask.

- **`bib_temp.ttl`**  
  Dataset RDF utilizado pela aplicação.  
  Este ficheiro é importado para um repositório GraphDB e contém a descrição da **Biblioteca Temporal**, incluindo livros, autores, eventos e linhas temporais.

- **`requirements.txt`**  
  Lista das dependências Python necessárias para executar a aplicação (por exemplo `Flask` e `SPARQLWrapper`).

### Templates HTML

Os templates encontram-se na pasta `templates/` e são utilizados pelo Flask para gerar as páginas web:

- **`layout.html`**  
  Template base da aplicação.  
  Define a estrutura geral das páginas (menu de navegação, cabeçalho e rodapé).

- **`livros.html`**  
  Apresenta o catálogo completo de livros disponíveis na base de conhecimento.

- **`livro.html`**  
  Template da página individual de um livro, onde são apresentados os seus detalhes e os eventos associados.

- **`eventos.html`**  
  Mostra a lista de eventos existentes no dataset.

- **`evento.html`**  
  Template da página individual de um evento, incluindo a sua descrição e os livros que o referem.