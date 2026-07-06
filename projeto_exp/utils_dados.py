"""
Salvamento/carregamento de instâncias (com código identificador) e
de resultados de execuções (CSV), compartilhado entre os experimentos.
"""

import json
import csv
import os
from statistics import mean
from typing import List, Dict


def salvar_instancias(instancias: List[dict], caminho_arquivo: str) -> None:
    """
    Salva uma lista de instâncias, cada uma como um dict contendo pelo
    menos {'codigo', 'mapa', 'inicio', 'objetivo'}, em um JSON único.
    Isso é o que garante que os dois parceiros rodem seus algoritmos
    sobre EXATAMENTE as mesmas entradas.
    """
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(instancias, f, ensure_ascii=False, indent=2)


def carregar_instancias(caminho_arquivo: str) -> List[dict]:
    """
    Carrega instâncias salvas em JSON. Reconverte 'inicio' e 'objetivo'
    para tupla (o JSON os transforma em lista, e listas não servem como
    chave de dict/set - o que quebraria a busca silenciosamente).
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        instancias = json.load(f)
    for instancia in instancias:
        instancia["inicio"] = tuple(instancia["inicio"])
        instancia["objetivo"] = tuple(instancia["objetivo"])
    return instancias


def salvar_resultados_csv(resultados: List[Dict], caminho_arquivo: str) -> None:
    """
    Acrescenta uma lista de dicts (ex: resultado.resumo() + 'codigo_entrada')
    a um CSV. Cria o arquivo com cabeçalho se ele ainda não existir.
    """
    if not resultados:
        return
    campos = list(resultados[0].keys())
    escrever_cabecalho = not os.path.exists(caminho_arquivo)
    with open(caminho_arquivo, "a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        if escrever_cabecalho:
            escritor.writeheader()
        escritor.writerows(resultados)


def agregar_media(resultados: List[Dict], chave_agrupamento: str,
                   campos_numericos: List[str]) -> List[Dict]:
    """
    Agrupa `resultados` pelo valor de `chave_agrupamento` (ex: heurística,
    ou densidade de obstáculos) e calcula a média de cada campo em
    `campos_numericos`. Usado para as tabelas de valores médios pedidas
    nos Experimentos 3 e 4.
    """
    grupos: Dict = {}
    for linha in resultados:
        chave = linha[chave_agrupamento]
        grupos.setdefault(chave, []).append(linha)

    agregados = []
    for chave, linhas in grupos.items():
        agregado = {chave_agrupamento: chave, "n_execucoes": len(linhas)}
        for campo in campos_numericos:
            valores = [l[campo] for l in linhas if l[campo] is not None]
            agregado[f"media_{campo}"] = mean(valores) if valores else None
        agregados.append(agregado)
    return agregados
