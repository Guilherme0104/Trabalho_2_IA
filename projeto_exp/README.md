# Projeto - Resolução de Problemas com Busca (IA 2026.1)

## Estrutura

```
estruturas.py        # No e Resultado (formato ÚNICO de retorno para TODOS os algoritmos)
mapa.py               # geração do grid, obstáculos, vizinhos (ordem N-L-S-O), validação de conectividade
heuristicas.py        # distancia_euclidiana, distancia_manhattan (com fator, para o Exp. 3)
busca_informada.py    # PESSOA B: Busca Gulosa + A* (função genérica única, f(n) muda)
busca_local.py         # PESSOA A: as 3 variações de Subida de Encosta (stub a preencher)
utils_dados.py          # salvar/carregar instâncias em JSON, salvar resultados em CSV
test_busca.py            # teste de sanidade rápido (já validado, roda sem erro)
```

## Contrato de interface

Todo algoritmo de busca recebe:

```python
algoritmo(mapa, inicio, objetivo, heuristica, gerar_vizinhos, ...) -> Resultado
```

- `mapa`: matriz 15x15 (lista de listas), células `-1` = obstáculo
- `inicio`, `objetivo`: tuplas `(linha, coluna)`
- `heuristica`: função `(estado, objetivo) -> float`, de `heuristicas.py`
  (usar `functools.partial(..., fator=3)` para o Experimento 3)
- `gerar_vizinhos`: sempre `mapa.gerar_vizinhos`, já devolve vizinhos na ordem N-L-S-O

Todo algoritmo retorna um `estruturas.Resultado`, com:
`caminho`, `custo_total`, `estados_gerados`, `estados_visitados`, `sucesso`.

## Convenção de contagem (importante alinhar!)

- **estados_gerados**: todo nó/vizinho *examinado* durante a execução (mesmo que descartado por já ter sido visitado ou por não melhorar o caminho).
- **estados_visitados**: todo nó efetivamente *expandido/processado* pelo algoritmo.

Isso já está implementado assim em `busca_informada.py`. A Pessoa A deve seguir a
mesma convenção em `busca_local.py`, para os dados dos dois serem comparáveis nas
tabelas do relatório (principalmente no Experimento 4, que mistura os dois grupos
de algoritmos).

## Divisão de trabalho

- **Pessoa B (fazendo)**: `busca_informada.py` — Busca Gulosa e A*, unificados numa
  função genérica que só troca `f(n) = h(n)` por `f(n) = g(n) + h(n)`.
- **Pessoa A (a fazer)**: `busca_local.py` — implementar `hill_climbing` com as
  3 estratégias (`deterministica`, `maior_aclive`, `estocastica`). O contrato e
  as regras de cada variação já estão documentados no docstring do arquivo.

## Próximos passos

1. Pessoa A implementa `busca_local.py`.
2. Escrever os 4 scripts de experimento (um por experimento do enunciado),
   usando `mapa.gerar_instancia_valida` + `utils_dados.salvar_instancias` para
   gerar e persistir as entradas (mesmo conjunto de entradas pros dois!).
3. Rodar os algoritmos sobre essas entradas e salvar os resultados com
   `utils_dados.salvar_resultados_csv`.
4. Implementar visualização do caminho encontrado (recomendado no enunciado).
