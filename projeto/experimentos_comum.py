"""
Utilitários compartilhados pelos 4 scripts de experimento.

Centraliza:
  - geração de um CONJUNTO de instâncias válidas, cada uma com um 'codigo'
    identificador e reprodutível (o PDF exige guardar as entradas e seus
    códigos, e rodar todas as variações sobre EXATAMENTE as mesmas entradas);
  - caminhos padronizados das pastas de dados/resultados;
  - helper para começar um CSV do zero (o salvar_resultados_csv acrescenta,
    então apagamos um arquivo antigo antes de reexecutar um experimento).
"""

import os

from mapa import gerar_instancia_valida

# Pastas de saída, relativas a este arquivo (funciona de qualquer cwd).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DADOS = os.path.join(BASE_DIR, "dados")


def caminho_dados(nome_arquivo: str) -> str:
    """Devolve o caminho completo dentro da pasta de dados, criando-a se preciso."""
    os.makedirs(DIR_DADOS, exist_ok=True)
    return os.path.join(DIR_DADOS, nome_arquivo)


def gerar_conjunto(n_instancias: int, pct_obstaculos: float,
                    seed_base: int, prefixo: str, n: int = 15) -> list:
    """
    Gera `n_instancias` instâncias válidas (mapa + início + objetivo conectados),
    cada uma com um 'codigo' único e reprodutível no formato "<prefixo>-<i>".

    Usar um seed_base fixo garante que reexecutar o experimento produza
    exatamente o mesmo conjunto de entradas.
    """
    instancias = []
    for i in range(n_instancias):
        inst = gerar_instancia_valida(n=n, pct_obstaculos=pct_obstaculos,
                                       seed=seed_base + i)
        inst["codigo"] = f"{prefixo}-{i:02d}"
        # normaliza para tupla (JSON não tem tupla; em memória mantemos tupla)
        inst["inicio"] = tuple(inst["inicio"])
        inst["objetivo"] = tuple(inst["objetivo"])
        instancias.append(inst)
    return instancias


def reiniciar_csv(caminho_arquivo: str) -> None:
    """Remove um CSV de resultados anterior para evitar linhas duplicadas."""
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
