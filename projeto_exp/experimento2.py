"""
Experimento 2 - Busca Gulosa e A* (enunciado, seção "Experimento 2").

20 instâncias sem obstáculos. Para cada uma, roda as 4 variações:
    (a) Busca Gulosa com DE
    (b) Busca Gulosa com DM
    (c) A* com DE
    (d) A* com DM

Salva:
    - as instâncias geradas (com código), em dados/exp2_instancias.json
    - os resultados de cada execução, em dados/exp2_resultados.csv
"""

import os

from mapa import gerar_instancia_valida, gerar_vizinhos
from heuristicas import distancia_euclidiana, distancia_manhattan
from busca_informada import busca_gulosa, a_estrela
from utils_dados import salvar_instancias, salvar_resultados_csv

N_INSTANCIAS = 20
PASTA_DADOS = "dados"
ARQUIVO_INSTANCIAS = os.path.join(PASTA_DADOS, "exp2_instancias.json")
ARQUIVO_RESULTADOS = os.path.join(PASTA_DADOS, "exp2_resultados.csv")


def gerar_instancias_exp2() -> list:
    """Gera as 20 instâncias do experimento, cada uma com um código único."""
    instancias = []
    for i in range(1, N_INSTANCIAS + 1):
        codigo = f"exp2_{i:03d}"
        instancia = gerar_instancia_valida(n=15, pct_obstaculos=0.0, seed=1000 + i)
        instancia["codigo"] = codigo
        instancias.append(instancia)
    return instancias


def rodar_experimento() -> None:
    os.makedirs(PASTA_DADOS, exist_ok=True)

    instancias = gerar_instancias_exp2()
    salvar_instancias(instancias, ARQUIVO_INSTANCIAS)
    print(f"{len(instancias)} instâncias geradas e salvas em {ARQUIVO_INSTANCIAS}")

    heuristicas = {"DE": distancia_euclidiana, "DM": distancia_manhattan}
    algoritmos = {"Busca Gulosa": busca_gulosa, "A*": a_estrela}

    resultados = []
    for instancia in instancias:
        mapa = instancia["mapa"]
        inicio = instancia["inicio"]
        objetivo = instancia["objetivo"]
        codigo = instancia["codigo"]

        # mesmo conjunto de entradas para TODAS as variações (exigência do enunciado)
        for nome_alg, funcao_alg in algoritmos.items():
            for nome_h, funcao_h in heuristicas.items():
                resultado = funcao_alg(mapa, inicio, objetivo, funcao_h, gerar_vizinhos)
                resultado.algoritmo = nome_alg
                resultado.heuristica = nome_h

                linha = resultado.resumo()
                linha["codigo_entrada"] = codigo
                resultados.append(linha)

    salvar_resultados_csv(resultados, ARQUIVO_RESULTADOS)
    print(f"{len(resultados)} execuções registradas em {ARQUIVO_RESULTADOS}")


if __name__ == "__main__":
    rodar_experimento()
