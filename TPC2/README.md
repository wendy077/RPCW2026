# TPC2: Ontologia do Cinema

## Metainformação
- **Título:** TPC2 - Ontologia do Cinema
- **Data:** 14/02/2026
- **Autor:**
  - **Id:** PG61534
  - **Nome:** Mariana Pinto

## Resumo

Este trabalho consiste na criação de uma ontologia OWL desenvolvida no âmbito do tutorial de Protégé, modelando o domínio do cinema.

A ontologia inclui classes para representar filmes, pessoas, géneros, países, línguas, obras e personagens, bem como as respetivas relações semânticas. A classe Ator é modelada como classe definida, permitindo inferência automática com base na propriedade Atuou.

Foram definidas propriedades de objeto e de dados para representar relações entre indivíduos (como participação em filmes, realização, composição e escrita) e atributos como data de lançamento, duração e sexo.

A ontologia integra:

- Propriedades inversas;
- Enumeração de classes (como Género e País);
- Restrições de cardinalidade;
- Restrições sobre intervalos de valores;
- Axiomas de cobertura na classe Ator.

Foram instanciados vários filmes e respetivos participantes, permitindo validar a ontologia através de raciocínio automático, nomeadamente para classificação de atores e filmes com base nas restrições definidas.

## Lista de Resultados

| Ficheiro | Descrição |
|----------|-----------|
| [cinema.ttl](./cinema.ttl) | Ontologia completa do domínio do cinema em formato Turtle |
