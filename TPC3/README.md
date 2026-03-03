# TPC3: GraphDB e SPARQL — O Polvo Filosófico

## Metainformação
- **Título:** TPC3 - GraphDB e SPARQL (Polvo Filosófico)
- **Data:** 21/02/2026
- **Autor:**
  - **Id:** PG61534
  - **Nome:** Mariana Pinto

## Resumo

Este trabalho consiste na importação e análise de uma ontologia em Turtle no GraphDB, identificação e correção de problemas na ontologia/dataset e execução de queries SPARQL para responder às questões propostas.

A ontologia representa o domínio do restaurante "O Polvo Filosófico", com agentes (pessoas, animais e máquinas), funcionários, clientes, pedidos, pratos e ingredientes, incluindo restrições OWL.

## Problemas detetados e correções efetuadas

### 1) Propriedade usada mas não declarada (`:feitoPor`)
**Problema:** Existiam pedidos associados a clientes através da propriedade `:feitoPor`, mas esta propriedade não estava declarada na ontologia.  
**Correção:** Foi declarada `:feitoPor` como `owl:ObjectProperty`, com `domain :Pedido` e `range :Cliente`, e definida como inversa de `:fazPedido`.

### 2) Inconsistência OWL: `:Polvo` a comer prato com ingrediente `:Polvo`
**Problema:** A ontologia define que polvos não comem pratos com ingrediente polvo (`:Polvo` só come pratos que não sejam `:PratoComPolvo`). No dataset, o indivíduo `:Aristoteles` (tipado como `:Polvo`) consumia pratos que tinham ingredientes tipados como `:Polvo`, violando o axioma.  
**Correção:** Foram removidos os consumos inconsistentes e substituídos por um consumo consistente (`:Aristoteles :come :BifeDeterminista`).

### 3) Colisão de identificador: `:Pedido1` definido em dois blocos
**Problema:** O identificador `:Pedido1` aparecia em dois blocos diferentes com pratos distintos, levando o mesmo pedido a ficar com múltiplos pratos por acumulação de triplos.  
**Correção:** O pedido do bloco “Exemplo de Pedido Problemático” foi renomeado para `:PedidoProblematico1`, mantendo `:Pedido1` como pedido real no bloco final de pedidos.

## Nota metodológica

A ontologia não define explicitamente uma relação entre o restaurante e os pratos servidos (por exemplo, uma propriedade `:serve` ou um conceito de menu).

Assim, a interpretação adotada para responder à pergunta *“Que pratos serve o restaurante?”* foi considerar como pratos servidos todos os pratos associados a instâncias da classe `:Pedido`.  

Ou seja, um prato é considerado servido se aparece na relação `:contemPrato` de um `:Pedido`.

Esta decisão garante coerência com o modelo existente e evita introduzir novas propriedades não previstas na ontologia original.

## Estrutura do repositório

| Caminho | Descrição |
|--------|-----------|
| `polvo_filosofico_corrigido.ttl` | Ontologia/dataset corrigido em Turtle |
| `queries/clientes.rq` | Query SPARQL para listar clientes |
| `queries/pratos.rq` | Query SPARQL para listar pratos servidos |
| `queries/ingredientes.rq` | Query SPARQL para ingredientes por prato |
| `queries/funcionarios_clientes.rq` | Query SPARQL para indivíduos que são funcionários e clientes |