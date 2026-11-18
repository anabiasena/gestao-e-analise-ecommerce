
import csv
from pathlib import Path

# Caminho da pasta onde estão os arquivos CSV
pasta_dados = Path("data/raw")

# Percorre todos os arquivos CSV da pasta
for arquivo in sorted(pasta_dados.glob("*.csv")):

    with open(arquivo, "r", encoding="utf-8-sig", newline="") as dados:

        leitor = csv.reader(dados)

        # A primeira linha contém os nomes das colunas
        cabecalho = next(leitor, [])

        # Conta os registros, sem considerar o cabeçalho
        quantidade_registros = sum(1 for linha in leitor)

        # Exibe os resultados
        print("-" * 60)
        print(f"Arquivo: {arquivo.name}")
        print(f"Quantidade de registros: {quantidade_registros}")
        print(f"Quantidade de colunas: {len(cabecalho)}")
        print(f"Colunas: {cabecalho}")