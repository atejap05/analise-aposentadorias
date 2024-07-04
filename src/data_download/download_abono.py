import os
import requests
from datetime import datetime


def get_current_mes_ano():
    current = datetime.now().strftime("%m%Y")
    mes = int(current[:2])
    ano = int(current[2:])
    return mes, ano


def generate_month_year_sequence(start_month, start_year, end_month, end_year):
    sequence = []
    current_year = start_year
    current_month = start_month
    while current_year < end_year or (current_year == end_year and current_month <= end_month):
        sequence.append(f"{current_month:02d}{current_year}")
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    return sequence


def download_csv(url, file_path):
    # Envia uma requisição GET para o URL
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Escreve o conteúdo da resposta em um arquivo
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado com sucesso e salvo como {file_path}")
    else:
        print(
            f"Falha ao baixar o arquivo. Código de status: {response.status_code}")


def download_all():
    [mes, ano] = get_current_mes_ano()
    sequence = generate_month_year_sequence(1, 2017, mes, ano)
    if not os.path.exists("all_files"):
        os.makedirs("all_files")
    for month_year in sequence:
        url = f"https://repositorio.dados.gov.br/segrt/ABONOP_{month_year}.csv"
        file_path = f"all_files/ABONOP_{month_year}.csv"
        download_csv(url, file_path)


if __name__ == "__main__":
    download_all()
