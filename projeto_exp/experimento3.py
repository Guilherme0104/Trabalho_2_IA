"""
Experimento 3 - A* e Admissibilidade (enunciado, seção "Experimento 3").

20 instâncias com 20% de obstáculos (geradas e validadas quanto à
conectividade por mapa.gerar_instancia_valida). Para cada uma, roda o
A* com 6 variações de heurística:

    h1 = 1 x DE      h4 = 1 x DM
    h2 = 3 x DE      h5 = 3 x DM
    h3 = 6 x DE      h6 = 6 x DM

Salva:
    - as instâncias geradas (com código), em dados/exp3_instancias.json
    - os resultados de cada execução, em dados/exp3_resultados.csv
    - os valores médios por variação de heurística, em dados/exp3_agregado.csv
      (conforme sugerido no enunciado, para facilitar a análise de Q3A-C)
"""

import os
from functools import partial

from mapa import gerar_instancia_valida, gerar_vizinhos
from heuristicas import distancia_euclidiana, distancia_manhattan
from busca_informada import a_estrela
from utils_dados import salvar_instancias, salvar_resultados_csv, agregar_media

N_INSTANCIAS = 20
PCT_OBSTACULOS = 0.2
PASTA_DADOS = "dados"
ARQUIVO_INSTANCIAS = os.path.join(PASTA_DADOS, "exp3_instancias.json")
ARQUIVO_RESULTADOS = os.path.join(PASTA_DADOS, "exp3_resultados.csv")
ARQUIVO_AGREGADO = os.path.join(PASTA_DADOS, "exp3_agregado.csv")


def gerar_instancias_exp3() -> list:
    """Gera as 20 instâncias com 20% de obstáculos, cada uma com um código único."""
    instancias = []
    for i in range(1, N_INSTANCIAS + 1):
        codigo = f"exp3_{i:03d}"
        instancia = gerar_instancia_valida(n=15, pct_obstaculos=PCT_OBSTACULOS, seed=2000 + i)
        instancia["codigo"] = codigo
        instancias.append(instancia)
    return instancias


def construir_variacoes_heuristica():
    """As 6 variações (identificador, função heurística já com fator fixado)."""
    return [
        ("h1_DE_x1", partial(distancia_euclidiana, fator=1)),
        ("h2_DE_x3", partial(distancia_euclidiana, fator=3)),
        ("h3_DE_x6", partial(distancia_euclidiana, fator=6)),
        ("h4_DM_x1", partial(distancia_manhattan, fator=1)),
        ("h5_DM_x3", partial(distancia_manhattan, fator=3)),
        ("h6_DM_x6", partial(distancia_manhattan, fator=6)),
    ]


def rodar_experimento() -> None:
    os.makedirs(PASTA_DADOS, exist_ok=True)

    instancias = gerar_instancias_exp3()
    salvar_instancias(instancias, ARQUIVO_INSTANCIAS)
    print(f"{len(instancias)} instâncias (20% obstáculos) geradas e salvas em {ARQUIVO_INSTANCIAS}")

    variacoes = construir_variacoes_heuristica()

    resultados = []
    for instancia in instancias:
        mapa = instancia["mapa"]
        inicio = instancia["inicio"]
        objetivo = instancia["objetivo"]
        codigo = instancia["codigo"]

        # mesmo conjunto de entradas para as 6 variações (exigência do enunciado)
        for identificador, funcao_h in variacoes:
            resultado = a_estrela(mapa, inicio, objetivo, funcao_h, gerar_vizinhos)
            resultado.algoritmo = "A*"
            resultado.heuristica = identificador

            linha = resultado.resumo()
            linha["codigo_entrada"] = codigo
            resultados.append(linha)

    salvar_resultados_csv(resultados, ARQUIVO_RESULTADOS)
    print(f"{len(resultados)} execuções registradas em {ARQUIVO_RESULTADOS}")

    agregados = agregar_media(
        resultados,
        chave_agrupamento="heuristica",
        campos_numericos=["estados_gerados", "estados_visitados", "custo_total"],
    )
    salvar_resultados_csv(agregados, ARQUIVO_AGREGADO)
    print(f"Valores médios por heurística salvos em {ARQUIVO_AGREGADO}")


if __name__ == "__main__":
    rodar_experimento()
