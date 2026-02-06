# TPC1 - Ontologia da História

## Resumo
Modelação OWL/RDF (Turtle) da história fornecida no enunciado, com classes, propriedades e indivíduos.

## Ficheiros
- `historia.ttl` — ontologia e instâncias (Turtle)

## Perguntas do enunciado (como responder a partir da ontologia)
- Quantas línguas fala o Eduardo?
  - Contar os objetos de `:Eduardo :fluenteEm ?lingua`.
- Quem se inscreveu no curso de alemão?
  - Listar sujeitos de `?s :frequentaCurso :CursoAlemao`.
- Quantos indivíduos existem na ontologia?
  - Contar instâncias (recursos que não são owl:Class nem propriedades).
- Quem é Hanna?
  - Ver triplos com sujeito `:Hanna` (tipo, línguas, curso, parceria).
