"""
EXPERIMENTO 1 - Variações da Subida de Encosta (SdE).

Compara as 3 variações de SdE (determinística, maior aclive, estocástica)
com as heurísticas DE e DM, sobre 15 entradas SEM obstáculos. Isso dá as
6 variações (a)-(f) pedidas no enunciado.

Saídas (pasta dados/):
    instancias_exp1.json  -> as 15 entradas com seus códigos
    resultados_exp1.csv   -> uma linha por (entrada x variação x heurística)

Colunas do CSV (o que o PDF pede para tabular):
    codigo_entrada, algoritmo (variação da SdE), heuristica,
    estados_gerados, estados_visitados, custo_total, sucesso, tamanho_caminho
"""

import random

from mapa import gerar_vizinhos
from heuristicas import distancia_euclidiana, distancia_manhattan
from busca_local import hill_climbing
from utils_dados import salvar_instancias, salvar_resultados_csv
from experimentos_comum import gerar_conjunto, caminho_dados, reiniciar_csv

# --- Parâmetros do experimento ---------------------------------------------
N_ENTRADAS = 15            # exigido pelo enunciado
SEED_BASE = 1000           # fixa o conjunto de entradas (reprodutível)
SEED_ESTOCASTICA = 42      # fixa os sorteios da variação estocástica

ARQ_INSTANCIAS = "instancias_exp1.json"
ARQ_RESULTADOS = "resultados_exp1.csv"

ESTRATEGIAS = ["deterministica", "maior_aclive", "estocastica"]
HEURISTICAS = {"DE": distancia_euclidiana, "DM": distancia_manhattan}


def main():
    # 1) Gera e salva o conjunto único de 15 entradas (sem obstáculos).
    instancias = gerar_conjunto(N_ENTRADAS, pct_obstaculos=0.0,
                                 seed_base=SEED_BASE, prefixo="E1")
    salvar_instancias(instancias, caminho_dados(ARQ_INSTANCIAS))

    # rng dedicado à variação estocástica, para os sorteios serem reprodutíveis
    rng = random.Random(SEED_ESTOCASTICA)

    # 2) Roda as 6 variações sobre cada entrada e coleta as linhas da tabela.
    resultados = []
    for inst in instancias:
        mapa = inst["mapa"]
        inicio = inst["inicio"]
        objetivo = inst["objetivo"]

        for estrategia in ESTRATEGIAS:
            for nome_h, h in HEURISTICAS.items():
                r = hill_climbing(mapa, inicio, objetivo, h,
                                   gerar_vizinhos, estrategia, rng)
                r.heuristica = nome_h
                linha = {"codigo_entrada": inst["codigo"], **r.resumo()}
                resultados.append(linha)

    # 3) Salva a tabela em CSV (recomeça do zero a cada execução).
    caminho_csv = caminho_dados(ARQ_RESULTADOS)
    reiniciar_csv(caminho_csv)
    salvar_resultados_csv(resultados, caminho_csv)

    _imprimir_resumo(instancias, resultados)


def _imprimir_resumo(instancias, resultados):
    """Imprime a tabela no console + um agregado leve para ajudar na análise."""
    print(f"Experimento 1: {len(instancias)} entradas x "
          f"{len(ESTRATEGIAS)} estrategias x {len(HEURISTICAS)} heuristicas "
          f"= {len(resultados)} execucoes\n")

    print(f"{'entrada':8s} {'variacao':16s} {'h':3s} "
          f"{'gerados':>8s} {'visitados':>10s} {'custo':>6s} {'ok':>4s}")
    print("-" * 62)
    for lin in resultados:
        custo = lin["custo_total"] if lin["custo_total"] is not None else "-"
        print(f"{lin['codigo_entrada']:8s} {lin['algoritmo']:16s} "
              f"{lin['heuristica']:3s} {lin['estados_gerados']:>8d} "
              f"{lin['estados_visitados']:>10d} {str(custo):>6s} "
              f"{'S' if lin['sucesso'] else 'N':>4s}")

    # Agregado: por (variacao, heuristica), taxa de sucesso e custo medio
    # (apenas dos casos com sucesso). Ajuda a discutir Q1A/Q1B/Q1C.
    print("\nAgregado por variacao/heuristica:")
    print(f"{'variacao':16s} {'h':3s} {'taxa_sucesso':>13s} "
          f"{'custo_medio_ok':>15s} {'gerados_medio':>14s}")
    print("-" * 66)
    for estrategia in ESTRATEGIAS:
        alg = f"SdE-{estrategia}"
        for nome_h in HEURISTICAS:
            grupo = [r for r in resultados
                     if r["algoritmo"] == alg and r["heuristica"] == nome_h]
            n = len(grupo)
            ok = [r for r in grupo if r["sucesso"]]
            taxa = 100.0 * len(ok) / n if n else 0.0
            custo_medio = (sum(r["custo_total"] for r in ok) / len(ok)
                           if ok else float("nan"))
            gerados_medio = sum(r["estados_gerados"] for r in grupo) / n if n else 0.0
            custo_str = f"{custo_medio:.1f}" if ok else "-"
            print(f"{estrategia:16s} {nome_h:3s} {taxa:>12.1f}% "
                  f"{custo_str:>15s} {gerados_medio:>14.1f}")

    print(f"\nArquivos salvos em dados/: {ARQ_INSTANCIAS}, {ARQ_RESULTADOS}")


if __name__ == "__main__":
    main()
