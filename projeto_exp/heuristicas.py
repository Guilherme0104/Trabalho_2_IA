"""
Funções heurísticas: Distância Euclidiana (DE) e Distância Manhattan (DM).

Ambas aceitam um parâmetro `fator`, usado no Experimento 3 para testar
heurísticas ponderadas (h1=1x, h2=3x, h3=6x). Use functools.partial para
fixar o fator antes de passar a heurística para os algoritmos de busca:

    from functools import partial
    h = partial(distancia_euclidiana, fator=3)
"""

import math
from typing import Tuple

Estado = Tuple[int, int]


def distancia_euclidiana(a: Estado, b: Estado, fator: float = 1) -> float:
    """DE = piso(sqrt((x1-x2)^2 + (y1-y2)^2)) * fator"""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.floor(math.sqrt(dx * dx + dy * dy)) * fator


def distancia_manhattan(a: Estado, b: Estado, fator: float = 1) -> float:
    """DM = (|x1-x2| + |y1-y2|) * fator"""
    return (abs(a[0] - b[0]) + abs(a[1] - b[1])) * fator
