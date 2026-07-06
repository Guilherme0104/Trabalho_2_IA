"""
MÓDULO DA PESSOA B: Busca Gulosa e A*.

Os dois algoritmos são o MESMO esqueleto (busca em grafo com fronteira
de prioridade), diferindo apenas na função de avaliação f(n):

    Busca Gulosa:  f(n) = h(n)
    A*:            f(n) = g(n) + h(n)

Por isso implementamos uma única função genérica `busca_informada` e
duas funções finas por cima dela (`busca_gulosa` e `a_estrela`), que é
o que deve ser chamado nos scripts de experimento.
"""

import heapq
import itertools
from typing import Callable, List, Tuple

from estruturas import No, Resultado

Estado = Tuple[int, int]


def _reconstruir_caminho(no: No) -> List[Estado]:
    caminho = []
    atual = no
    while atual is not None:
        caminho.append(atual.estado)
        atual = atual.pai
    caminho.reverse()
    return caminho


def busca_informada(mapa, inicio: Estado, objetivo: Estado,
                     heuristica: Callable[[Estado, Estado], float],
                     gerar_vizinhos: Callable,
                     usar_custo_g: bool) -> Resultado:
    """
    Busca em grafo com fronteira de prioridade (heap).

    usar_custo_g=False -> Busca Gulosa (f(n) = h(n))
    usar_custo_g=True  -> A*           (f(n) = g(n) + h(n))
    """
    contador = itertools.count()  # desempate estável no heap (evita comparar Nós)

    no_inicial = No(estado=inicio, pai=None, custo_g=0)
    h_inicial = heuristica(inicio, objetivo)
    f_inicial = h_inicial if not usar_custo_g else (0 + h_inicial)

    fronteira = [(f_inicial, next(contador), no_inicial)]
    melhor_g = {inicio: 0}   # menor custo g conhecido até agora, por estado
    visitados = set()

    estados_gerados = 1       # o nó inicial conta como gerado
    estados_visitados = 0

    while fronteira:
        _, _, no_atual = heapq.heappop(fronteira)

        if no_atual.estado in visitados:
            continue
        visitados.add(no_atual.estado)
        estados_visitados += 1

        if no_atual.estado == objetivo:
            return Resultado(
                caminho=_reconstruir_caminho(no_atual),
                custo_total=no_atual.custo_g,
                estados_gerados=estados_gerados,
                estados_visitados=estados_visitados,
                sucesso=True,
            )

        for vizinho, custo_passo in gerar_vizinhos(no_atual.estado, mapa):
            estados_gerados += 1
            if vizinho in visitados:
                continue

            novo_g = no_atual.custo_g + custo_passo
            # só (re)expande se é a primeira vez que vemos o estado, ou se
            # achamos um caminho mais barato até ele
            if vizinho not in melhor_g or novo_g < melhor_g[vizinho]:
                melhor_g[vizinho] = novo_g
                h = heuristica(vizinho, objetivo)
                f = h if not usar_custo_g else (novo_g + h)
                novo_no = No(estado=vizinho, pai=no_atual, custo_g=novo_g)
                heapq.heappush(fronteira, (f, next(contador), novo_no))

    # fronteira esvaziou sem alcançar o objetivo
    return Resultado(
        caminho=[],
        custo_total=None,
        estados_gerados=estados_gerados,
        estados_visitados=estados_visitados,
        sucesso=False,
    )


def busca_gulosa(mapa, inicio: Estado, objetivo: Estado,
                  heuristica: Callable, gerar_vizinhos: Callable) -> Resultado:
    resultado = busca_informada(mapa, inicio, objetivo, heuristica, gerar_vizinhos,
                                 usar_custo_g=False)
    resultado.algoritmo = "Busca Gulosa"
    return resultado


def a_estrela(mapa, inicio: Estado, objetivo: Estado,
               heuristica: Callable, gerar_vizinhos: Callable) -> Resultado:
    resultado = busca_informada(mapa, inicio, objetivo, heuristica, gerar_vizinhos,
                                 usar_custo_g=True)
    resultado.algoritmo = "A*"
    return resultado
