"""
Teste rápido de sanidade: gera uma instância, roda Busca Gulosa e A*
com DE e DM, e imprime os resultados. Não substitui os scripts de
experimento de verdade, é só pra validar que o pipeline funciona.
"""

from functools import partial

from mapa import gerar_instancia_valida, gerar_vizinhos
from heuristicas import distancia_euclidiana, distancia_manhattan
from busca_informada import busca_gulosa, a_estrela


def main():
    instancia = gerar_instancia_valida(n=15, pct_obstaculos=0.0, seed=42)
    mapa = instancia["mapa"]
    inicio = instancia["inicio"]
    objetivo = instancia["objetivo"]
    print(f"Início: {inicio}  Objetivo: {objetivo}\n")

    heuristicas = {"DE": distancia_euclidiana, "DM": distancia_manhattan}
    algoritmos = {"Busca Gulosa": busca_gulosa, "A*": a_estrela}

    for nome_alg, funcao in algoritmos.items():
        for nome_h, h in heuristicas.items():
            resultado = funcao(mapa, inicio, objetivo, h, gerar_vizinhos)
            resultado.heuristica = nome_h
            print(f"{nome_alg:15s} | {nome_h} | {resultado.resumo()}")

    # teste rápido também com obstáculos + heurística ponderada (fator do Exp. 3)
    print("\nCom obstáculos (20%) e DE x3:")
    instancia2 = gerar_instancia_valida(n=15, pct_obstaculos=0.2, seed=7)
    h_ponderada = partial(distancia_euclidiana, fator=3)
    resultado2 = a_estrela(instancia2["mapa"], instancia2["inicio"], instancia2["objetivo"],
                            h_ponderada, gerar_vizinhos)
    print(resultado2.resumo())


if __name__ == "__main__":
    main()
