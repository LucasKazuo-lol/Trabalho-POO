"""Programa principal do PBL: tela gráfica ou demonstração no terminal."""
import argparse
from pathlib import Path

from ClienteBackendEstudo import ClienteBackendEstudo, RepositorioSQLite


def main():
    # Sem opções, segue a missão 10 e usa o backend C# fornecido na aula.
    argumentos = argparse.ArgumentParser(description="FecapStudy — Trabalho POO")
    argumentos.add_argument("--console", action="store_true", help="Demonstra as missões 1 a 8 com Rich")
    argumentos.add_argument("--local", action="store_true", help="Usa SQLite em vez da API C#")
    argumentos.add_argument("--backend", default="http://localhost:5080", help="Endereço da API C#")
    opcoes = argumentos.parse_args()
    if opcoes.console:
        from Demonstracao import Demonstrar
        Demonstrar()
        return

    if opcoes.local:
        caminho = Path(__file__).parent / "dados" / "estudos.sqlite3"
        repositorio = RepositorioSQLite(caminho)
    else:
        repositorio = ClienteBackendEstudo(opcoes.backend)

    # Tkinter é importado somente no modo gráfico.
    from TelaEstudo import TelaEstudo
    TelaEstudo(repositorio).mainloop()


if __name__ == "__main__":
    main()
