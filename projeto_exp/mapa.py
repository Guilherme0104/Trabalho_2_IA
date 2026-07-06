"""
Representação do problema: mapa em grid 15x15, geração de instâncias,
validação de conectividade e geração de vizinhos.

Este módulo é COMPARTILHADO entre os dois parceiros — tudo que depende
da representação do mapa mora aqui, para garantir que os algoritmos de
ambos rodem sobre exatamente os mesmos dados.
"""

import random
from collections import deque
from typing import List, Tuple, Optional

Estado = Tuple[int, int]
Mapa = List[List[int]]

# Ordem cardinal fixa exigida pelo enunciado: N - L - S - O
# (linha, coluna) -> N: linha-1 | L: coluna+1 | S: linha+1 | O: coluna-1
DIRECOES_NLSO = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def gerar_mapa(n: int = 15, custo_min: int = 3, custo_max: int = 6,
               seed: Optional[int] = None) -> Mapa:
    """Gera uma matriz n x n com custos inteiros entre custo_min e custo_max (sem obstáculos)."""
    rng = random.Random(seed)
    return [[rng.randint(custo_min, custo_max) for _ in range(n)] for _ in range(n)]


def gerar_mapa_com_obstaculos(n: int = 15, custo_min: int = 3, custo_max: int = 6,
                               pct_obstaculos: float = 0.2,
                               seed: Optional[int] = None) -> Mapa:
    """Gera uma matriz n x n com custos e uma porcentagem de células bloqueadas (-1)."""
    rng = random.Random(seed)
    mapa = [[rng.randint(custo_min, custo_max) for _ in range(n)] for _ in range(n)]
    total_celulas = n * n
    qtd_bloqueadas = int(total_celulas * pct_obstaculos)
    posicoes = [(i, j) for i in range(n) for j in range(n)]
    rng.shuffle(posicoes)
    for (i, j) in posicoes[:qtd_bloqueadas]:
        mapa[i][j] = -1
    return mapa


def dentro_do_grid(estado: Estado, n: int) -> bool:
    x, y = estado
    return 0 <= x < n and 0 <= y < n


def gerar_vizinhos(estado: Estado, mapa: Mapa) -> List[Tuple[Estado, int]]:
    """
    Retorna a lista de (vizinho, custo_do_passo) na ordem N-L-S-O,
    ignorando posições fora do grid ou bloqueadas (-1).

    O custo do passo é o valor da célula de DESTINO (custo de entrar
    naquela interseção), conforme a modelagem do enunciado.
    """
    n = len(mapa)
    x, y = estado
    vizinhos = []
    for dx, dy in DIRECOES_NLSO:
        novo = (x + dx, y + dy)
        if dentro_do_grid(novo, n) and mapa[novo[0]][novo[1]] != -1:
            vizinhos.append((novo, mapa[novo[0]][novo[1]]))
    return vizinhos


def validar_conectividade(mapa: Mapa, inicio: Estado, objetivo: Estado) -> bool:
    """
    BFS simples que ignora custo - serve só para checar se existe ALGUM
    caminho entre início e objetivo (usado na geração de instâncias com
    obstáculos, conforme pedido na Q0A do enunciado).
    """
    if mapa[inicio[0]][inicio[1]] == -1 or mapa[objetivo[0]][objetivo[1]] == -1:
        return False
    visitados = {inicio}
    fila = deque([inicio])
    while fila:
        atual = fila.popleft()
        if atual == objetivo:
            return True
        for vizinho, _ in gerar_vizinhos(atual, mapa):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    return False


def _coordenada_aleatoria(n: int, rng: random.Random) -> Estado:
    return (rng.randint(0, n - 1), rng.randint(0, n - 1))


def gerar_instancia_valida(n: int = 15, pct_obstaculos: float = 0.0,
                            custo_min: int = 3, custo_max: int = 6,
                            seed: Optional[int] = None,
                            max_tentativas: int = 1000) -> dict:
    """
    Gera um mapa (com ou sem obstáculos) + origem + destino válidos e
    conectados. Repete a geração até achar uma instância válida (Q0A).

    Retorna um dicionário pronto para serialização/salvamento.
    """
    rng = random.Random(seed)
    for _ in range(max_tentativas):
        semente_mapa = rng.randint(0, 2**31)
        if pct_obstaculos > 0:
            mapa = gerar_mapa_com_obstaculos(n, custo_min, custo_max, pct_obstaculos, seed=semente_mapa)
        else:
            mapa = gerar_mapa(n, custo_min, custo_max, seed=semente_mapa)

        inicio = _coordenada_aleatoria(n, rng)
        objetivo = _coordenada_aleatoria(n, rng)

        if inicio == objetivo:
            continue
        if mapa[inicio[0]][inicio[1]] == -1 or mapa[objetivo[0]][objetivo[1]] == -1:
            continue
        if validar_conectividade(mapa, inicio, objetivo):
            return {"mapa": mapa, "inicio": inicio, "objetivo": objetivo,
                    "pct_obstaculos": pct_obstaculos}

    raise RuntimeError(f"Não foi possível gerar instância válida em {max_tentativas} tentativas.")
