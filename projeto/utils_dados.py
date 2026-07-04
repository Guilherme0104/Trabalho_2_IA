"""
Salvamento/carregamento de instâncias (com código identificador) e
de resultados de execuções (CSV), compartilhado entre os experimentos.
"""

import json
import csv
import os
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
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


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
