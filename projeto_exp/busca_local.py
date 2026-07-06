"""
MÓDULO DA PESSOA A: Subida de Encosta (SdE) - 3 variações.

Preencher a função hill_climbing abaixo. Interface (mesma convenção do
busca_informada.py, para os dados dos experimentos serem comparáveis):

    hill_climbing(mapa, inicio, objetivo, heuristica, gerar_vizinhos, estrategia) -> Resultado

estrategia ∈ {"deterministica", "maior_aclive", "estocastica"}

Reaproveitar do resto do projeto:
    - estruturas.No, estruturas.Resultado  (mesmo formato de retorno do A*/Gulosa)
    - mapa.gerar_vizinhos                   (já retorna vizinhos na ordem N-L-S-O)
    - heuristicas.distancia_euclidiana / distancia_manhattan

Regras do enunciado por variação:
    - "deterministica": percorrer vizinhos na ordem N-L-S-O; mover para o
      PRIMEIRO vizinho cuja heurística seja melhor (menor) que a do estado atual.
    - "maior_aclive": avaliar TODOS os vizinhos; mover para o de MELHOR heurística.
    - "estocastica": avaliar TODOS os vizinhos; sortear aleatoriamente entre
      os que são melhores que o estado atual.

Em qualquer variação: se nenhum vizinho for melhor que o atual, é ótimo
local -> parar (sucesso = (estado_atual == objetivo)).

Lembrar de contar estados_gerados (nós examinados/criados) e
estados_visitados (nós pelos quais o algoritmo efetivamente passou)
com a MESMA convenção usada em busca_informada.py, para os dados dos
dois serem comparáveis nas tabelas do relatório (isso é combinado com
a Pessoa B, não decidir sozinho).
"""

import random
from typing import Callable, Tuple

from estruturas import No, Resultado

Estado = Tuple[int, int]


def hill_climbing(mapa, inicio: Estado, objetivo: Estado,
                   heuristica: Callable, gerar_vizinhos: Callable,
                   estrategia: str, rng: random.Random = None) -> Resultado:
    raise NotImplementedError("Implementar: Pessoa A")
