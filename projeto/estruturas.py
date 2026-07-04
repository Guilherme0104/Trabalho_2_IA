"""
Estruturas de dados compartilhadas entre TODOS os algoritmos do trabalho.

Tanto a família "busca com fronteira" (Gulosa, A*) quanto a família
"busca local" (as 3 variações de SdE) devem retornar um objeto Resultado,
para que a coleta/agregação de dados dos experimentos seja idêntica
independente de quem implementou o algoritmo.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional

Estado = Tuple[int, int]


@dataclass
class No:
    """Nó de busca: representa um estado alcançado durante a expansão,
    junto com o ponteiro para o nó pai (usado para reconstruir o caminho)."""
    estado: Estado
    pai: Optional["No"]
    custo_g: int


@dataclass
class Resultado:
    """
    Resultado padronizado de uma execução de busca.

    Convenções adotadas (documentar isso no relatório):
      - estados_gerados: quantidade de nós CRIADOS ao longo da execução
        (todo vizinho examinado conta como "gerado", mesmo que não seja
        efetivamente expandido depois).
      - estados_visitados: quantidade de nós efetivamente EXPANDIDOS
        (retirados da fronteira/atual e processados).
      - custo_total: soma dos custos das interseções percorridas no
        caminho encontrado (None se sucesso=False).
    """
    caminho: List[Estado]
    custo_total: Optional[int]
    estados_gerados: int
    estados_visitados: int
    sucesso: bool
    algoritmo: str = ""
    heuristica: str = ""

    def resumo(self) -> dict:
        """Formato pronto para virar uma linha de tabela/CSV nos experimentos."""
        return {
            "algoritmo": self.algoritmo,
            "heuristica": self.heuristica,
            "estados_gerados": self.estados_gerados,
            "estados_visitados": self.estados_visitados,
            "custo_total": self.custo_total,
            "sucesso": self.sucesso,
            "tamanho_caminho": len(self.caminho),
        }
