"""
MÓDULO DA PESSOA A: Subida de Encosta (SdE) - 3 variações.

Implementa o algoritmo de busca local Subida de Encosta em três estratégias,
usado no Experimento 1 do trabalho. Segue a MESMA interface e as mesmas
convenções de contagem de `busca_informada.py` (Gulosa/A*), para que os dados
dos dois grupos de algoritmos sejam comparáveis nas tabelas do relatório.

Interface:
    hill_climbing(mapa, inicio, objetivo, heuristica, gerar_vizinhos,
                  estrategia, rng=None) -> estruturas.Resultado

Estratégias (estrategia ∈ {"deterministica", "maior_aclive", "estocastica"}):
    - "deterministica": percorre os vizinhos na ordem N-L-S-O e move para o
      PRIMEIRO cuja heurística seja estritamente melhor (menor) que a do atual.
    - "maior_aclive": avalia TODOS os vizinhos e move para o de MELHOR
      heurística (menor); empate mantém o primeiro na ordem N-L-S-O.
    - "estocastica": avalia TODOS os vizinhos e sorteia (via `rng`)
      uniformemente entre os que são estritamente melhores que o atual.

Em qualquer variação, se nenhum vizinho for melhor que o estado atual, chegou-se
a um ótimo local e a busca para. Só há sucesso se o estado final for o objetivo.

Convenção de contagem (alinhada com busca_informada.py):
    - estados_gerados: todo vizinho examinado (inclui o nó inicial e os
      descartados por não melhorarem o atual).
    - estados_visitados: todo estado efetivamente processado/expandido
      (o inicial + cada estado para o qual o algoritmo se moveu).

Reaproveita do resto do projeto:
    - estruturas.No, estruturas.Resultado  (formato de retorno único)
    - mapa.gerar_vizinhos                   (vizinhos já na ordem N-L-S-O)
    - heuristicas.distancia_euclidiana / distancia_manhattan
"""

import random
from typing import Callable, List, Tuple

from estruturas import No, Resultado

Estado = Tuple[int, int]

ESTRATEGIAS = ("deterministica", "maior_aclive", "estocastica")


def _reconstruir_caminho(no: No) -> List[Estado]:
    """Segue os ponteiros de pai até a raiz."""
    caminho = []
    atual = no
    while atual is not None:
        caminho.append(atual.estado)
        atual = atual.pai
    caminho.reverse()
    return caminho


def _escolher_proximo(vizinhos: List[Tuple[Estado, int]], h_atual: float,
                       heuristica: Callable, objetivo: Estado,
                       estrategia: str, rng: random.Random):
    """
    Recebe a lista de vizinhos (ordem N-L-S-O) e devolve:

    onde par_escolhido é ou None se nenhumvizinho for estritamente melhor que o estado atual,
    e examinados é quantosvizinhos foram olhados .
    """
    examinados = 0
    candidatos = []  # (h_vizinho, estado, custo_passo)

    for vizinho, custo_passo in vizinhos:
        examinados += 1
        h_viz = heuristica(vizinho, objetivo)

        if estrategia == "deterministica":
            # move para o PRIMEIRO vizinho estritamente melhor
            if h_viz < h_atual:
                return (vizinho, custo_passo), examinados
        else:
            # maior_aclive e estocastica avaliam TODOS
            if h_viz < h_atual:
                candidatos.append((h_viz, vizinho, custo_passo))

    if not candidatos:
        return None, examinados

    if estrategia == "maior_aclive":
        # menor heurística; empate mantém o primeiro da ordem N-L-S-O
        _, estado, custo_passo = min(candidatos, key=lambda c: c[0])
        return (estado, custo_passo), examinados

    # estocastica: sorteia uniformemente entre os que melhoram o atual
    _, estado, custo_passo = rng.choice(candidatos)
    return (estado, custo_passo), examinados


def hill_climbing(mapa, inicio: Estado, objetivo: Estado,
                   heuristica: Callable, gerar_vizinhos: Callable,
                   estrategia: str, rng: random.Random = None) -> Resultado:
    """
    Subida de Encosta com 3 variações

    Mantém um único estado atual e, a cada passo, move para um vizinho de
    heurística estritamente menor. Para ao chegar no objetivo ou ao atingir
    um ótimo local.
    """
    if estrategia not in ESTRATEGIAS:
        raise ValueError(f"Estratégia desconhecida: {estrategia!r}. "
                         f"Use uma de {ESTRATEGIAS}.")
    if rng is None:
        rng = random.Random()

    no_atual = No(estado=inicio, pai=None, custo_g=0)
    estados_gerados = 1     
    estados_visitados = 0

    #nº de passos como rede de segurança sera limitado.
    max_passos = len(mapa) * len(mapa)

    for _ in range(max_passos + 1):
        estados_visitados += 1  

        if no_atual.estado == objetivo:
            break

        vizinhos = gerar_vizinhos(no_atual.estado, mapa)
        h_atual = heuristica(no_atual.estado, objetivo)

        escolha, examinados = _escolher_proximo(
            vizinhos, h_atual, heuristica, objetivo, estrategia, rng)
        estados_gerados += examinados

        if escolha is None:
            break  # ótimo local

        proximo, custo_passo = escolha
        no_atual = No(estado=proximo, pai=no_atual,
                      custo_g=no_atual.custo_g + custo_passo)

    sucesso = (no_atual.estado == objetivo)
    resultado = Resultado(
        caminho=_reconstruir_caminho(no_atual),
        custo_total=no_atual.custo_g,
        estados_gerados=estados_gerados,
        estados_visitados=estados_visitados,
        sucesso=sucesso,
    )
    resultado.algoritmo = f"SdE-{estrategia}"
    return resultado