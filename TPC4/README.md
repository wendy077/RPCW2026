# TPC4: Ontologia OWL, Raciocínio e SPARQL — Biblioteca Temporal

## Metainformação
- **Título:** TPC4 - Ontologia OWL, Raciocínio e SPARQL (Biblioteca Temporal)
- **Data:** 08/03/2026
- **Autor:**
  - **Id:** PG61534
  - **Nome:** Mariana Pinto

## Resumo

Este trabalho consiste na modelação de uma ontologia OWL para o domínio da **Biblioteca Temporal**, seguindo o enunciado da semana 4 e a especificação apresentada em `biblioteca_temporal.pdf`.

A ontologia representa agentes, bibliotecas, livros, eventos e linhas temporais, incluindo restrições OWL sobre existência temporal, tipologia dos livros e coerência semântica entre livros e eventos. Após a definição da ontologia base, os dois datasets JSON fornecidos foram convertidos para RDF/Turtle e integrados na ontologia e formuladas 10 queries SPARQL sobre os dados carregados.

## Decisões de modelação e estratégia adotada

### 1) Estrutura geral do domínio
A ontologia foi organizada em torno de cinco blocos principais:

- **Agentes**: `Agente`, `Pessoa`, `Autor`, `Leitor`, `Bibliotecario`
- **Infraestrutura**: `Biblioteca`
- **Objetos bibliográficos**: `Livro`, `LivroHistorico`, `LivroFiccional`, `LivroParadoxal`
- **Temporalidade**: `EntidadeTemporal`, `LinhaTemporal`, `LinhaOriginal`, `LinhaAlternativa`, `Evento`, `EventoHistorico`, `EventoFuturo`
- **Circulação de livros**: `Emprestimo`

Esta divisão permitiu separar claramente os conceitos do domínio e tornar mais simples a definição das propriedades e das restrições OWL.

### 2) Axiomas principais
Foram modelados os axiomas centrais pedidos no enunciado:

- Todo o `Bibliotecario` trabalha em exatamente uma `Biblioteca`
- Todo o `Livro` existe em pelo menos uma `LinhaTemporal`
- `LivroHistorico` apenas refere `EventoHistorico`
- `LivroFiccional` não pode referir `EventoHistorico`
- `LivroHistorico` e `LivroFiccional` são disjuntos
- `LivroParadoxal` existe simultaneamente numa `LinhaOriginal` e numa `LinhaAlternativa`

No caso de `LivroParadoxal`, além das restrições em `rdfs:subClassOf`, foi ainda usada uma `owl:equivalentClass` para permitir inferência automática da classe a partir das linhas temporais associadas.

### 3) Propriedades e respetivos domínios/ranges
As propriedades do domínio foram definidas com `domain` e `range` explícitos, de forma a garantir coerência estrutural e facilitar inferência:

- `trabalhaEm`: `Bibliotecario -> Biblioteca`
- `pertenceA`: `Livro -> Biblioteca`
- `escritoPor`: `Livro -> Autor`
- `existeEm`: `Livro -> LinhaTemporal`
- `refereEvento`: `Livro -> Evento`
- `ocorreEm`: `Evento -> LinhaTemporal`
- `requisita`: `Leitor -> Livro`
- `temLeitor`: `Emprestimo -> Leitor`
- `temLivro`: `Emprestimo -> Livro`
- `emLinhaTemporal`: `Emprestimo -> LinhaTemporal`

Foram também definidas as inversas `temAutor` e `temBibliotecario` para tornar o modelo mais expressivo.

### 4) Modelação de empréstimos
Foi criada a classe `Emprestimo` como mecanismo auxiliar de modelação. Cada empréstimo é restringido por três cardinalidades qualificadas:

- `temLeitor exactly 1 Leitor`
- `temLivro exactly 1 Livro`
- `emLinhaTemporal exactly 1 LinhaTemporal`

Esta decisão foi tomada para representar explicitamente o ato de empréstimo e preparar a ontologia para restrições mais complexas relacionadas com leitores, autores, livros e linhas temporais.

### 5) Tratamento da restrição Autor/Leitor

O enunciado exige a restrição:

> Um Autor não pode ser Leitor do mesmo livro na mesma linha temporal.

Esta condição depende simultaneamente de três dimensões: pessoa, livro e linha temporal. Em OWL DL puro, este tipo de restrição ternária não é naturalmente expressável de forma exata apenas com axiomas de classes e propriedades binárias.

Por esse motivo, a ontologia foi reestruturada com a classe `Emprestimo`, que explicita:

- o leitor (`temLeitor`)
- o livro (`temLivro`)
- a linha temporal (`emLinhaTemporal`)

Esta modelação permite representar corretamente o fenómeno no nível ontológico.

A verificação exata da violação da regra foi realizada por query SPARQL de validação, que identifica casos em que uma mesma pessoa é simultaneamente autora de um livro e leitora desse mesmo livro na mesma linha temporal.

### 6) Cronos e inferências contraditórias
Para cumprir o requisito de permitir inferências contraditórias associadas a `Cronos`, foi criada uma versão específica da ontologia com o indivíduo:

- `Livro_Cronos_Paradoxo` tipado como `LivroHistorico`

Este livro:

- é escrito por `Cronos`
- existe em `Linha_T0`
- refere o evento `Nascimento_da_IA`

Por sua vez, `Nascimento_da_IA` foi tipado como `EventoFuturo`.

Como a ontologia estabelece que um `LivroHistorico` apenas pode referir `EventoHistorico`, o reasoner infere que `Nascimento_da_IA` também teria de ser um `EventoHistorico`. Como `EventoHistorico` e `EventoFuturo` são classes disjuntas, a ontologia com contradição torna-se inconsistente.

Este caso foi usado intencionalmente para demonstrar deteção de inconsistências e análise de justificações no Protégé.

## Indivíduos obrigatórios
Foram incluídos os indivíduos pedidos na especificação:

- `Cronos`
- `Linha_T0`
- `Linha_T1`
- `Biblioteca_Entre_Ontem_e_Amanha`

`Cronos` foi tipado simultaneamente como `Autor` e `Bibliotecario`, trabalhando na biblioteca obrigatória.


## Nota metodológica

Foram consideradas três versões principais de trabalho da ontologia:

### `biblioteca_temporal.ttl`
Versão base da ontologia, adequada para modelação do domínio, validação estrutural e integração posterior dos datasets.

### `biblioteca_temporal_com_contradicao.ttl`
Versão derivada da ontologia base que inclui o caso `Livro_Cronos_Paradoxo` / `Nascimento_da_IA`, destinada à execução do reasoner e análise de inconsistências semânticas.

### `biblioteca_temporal_com_datasets.ttl`
Versão final obtida por fusão da ontologia base com os dois datasets fornecidos, usada para execução das queries SPARQL e validação da consistência global do conhecimento carregado.

Esta separação foi adotada para distinguir claramente três objetivos: modelação da ontologia, teste de inconsistências e exploração/querying sobre os dados integrados.

## Execução do reasoner 

### 1) Ontologia base — `biblioteca_temporal.ttl`
Foi executado o reasoner sobre a ontologia base.

**Resultado:** a ontologia foi considerada **consistente**.

Esta versão foi mantida estável para servir de base à integração dos datasets e à execução das queries SPARQL.

### 2) Ontologia com datasets — `biblioteca_temporal_com_datasets.ttl`
Foi executado o reasoner sobre a ontologia resultante da fusão da ontologia base com os dois datasets fornecidos.

**Resultado:** a ontologia foi considerada **consistente**.

Isto mostra que a integração dos dados não introduziu conflitos lógicos com os axiomas definidos na ontologia.

### 3) Ontologia com contradição — `biblioteca_temporal_com_contradicao.ttl`
Foi executado o reasoner sobre a versão da ontologia que inclui o caso contraditório associado a `Cronos`.

**Resultado:** a ontologia foi considerada **inconsistente**.

### 4) Justificação da inconsistência
A explicação apresentada pelo Protégé envolve os seguintes elementos:

- `EventoFuturo disjointWith EventoHistorico`
- `LivroHistorico SubClassOf refereEvento only EventoHistorico`
- `Nascimento_da_IA Type EventoFuturo`
- `Livro_Cronos_Paradoxo refereEvento Nascimento_da_IA`
- `Livro_Cronos_Paradoxo Type LivroHistorico`

Dado que `Livro_Cronos_Paradoxo` é um `LivroHistorico`, tudo o que ele refere tem de ser um `EventoHistorico`. Como ele refere `Nascimento_da_IA`, o reasoner infere que `Nascimento_da_IA` teria de ser `EventoHistorico`. No entanto, esse mesmo indivíduo foi explicitamente tipado como `EventoFuturo`. Como `EventoHistorico` e `EventoFuturo` são disjuntos, a ontologia torna-se inconsistente.

## Execução das queries SPARQL

As 10 queries pedidas no enunciado foram executadas sobre o ficheiro `biblioteca_temporal_com_datasets.ttl`, após integração da ontologia base com os dois datasets.

Os resultados obtidos mostraram coerência com a modelação ontológica realizada. Em particular:

- a Query 2 identificou os livros presentes em múltiplas linhas temporais
- a Query 3 devolveu exatamente os livros inferidos como `LivroParadoxal`
- a Query 5 não devolveu resultados na ontologia consistente com datasets, como esperado
- a Query 10 devolveu o livro `Livro_Cronos_001`, confirmando a presença de obras atribuídas a `Cronos`
- a query adicional de validação da restrição Autor/Leitor não encontrou violações nos dados carregados

## Estrutura recomendada do repositório

| Caminho | Descrição |
|--------|-----------|
| `biblioteca_temporal.ttl` | Ontologia base em Turtle |
| `biblioteca_temporal_com_contradicao.ttl` | Versão com o caso contraditório de Cronos |
| `biblioteca_temporal_com_datasets.ttl` | Ontologia final com os datasets integrados |
| `dataset_temporal_100.json` | Primeiro dataset fornecido |
| `dataset_temporal_v2_100.json` | Segundo dataset fornecido |
| `json_to_ttl.py` | Script Python para converter os datasets JSON em Turtle |
| `merge_ttl.py` | Script Python para fundir ontologia base e datasets |
| `queries.sparql` | Conjunto final de Queries SPARQL |
| `README.md` | Documentação do trabalho |

## Etapas realizadas

No desenvolvimento do trabalho foram realizadas as seguintes etapas:

1. modelação da ontologia base em OWL/Turtle
2. criação de uma versão separada com contradição para teste de inconsistência
3. conversão dos dois datasets JSON para RDF/Turtle
4. fusão da ontologia base com os datasets
5. execução do reasoner OWL sobre as diferentes versões da ontologia
6. formulação das 10 queries SPARQL pedidas
7. criação de queries adicionais de validação e exploração