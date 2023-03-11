"""Анализ csv файла и для контракта, кд, договора вытаскивать
только цифры с разбиением по столбцам"""

import re
import time

import pandas as pd

start_time = time.time()

# паттерн фио
fio_pattern = r"([А-ЯЁ][А-Яа-яёЁ]+\s{1,2}?([А-ЯЁ][А-Яа-яёЁ]+\s?|[А-ЯЁ]+\.|[А-ЯЁ]+\,|[А-ЯЁ]+|[А-ЯЁ]+\/){2})"  # noqa: E501

# паттерн для финального вытаскивания только цифр кд,договора
# или контракта без дат
contract_pattern = r"(\d{3,})"

# года для исключения в финальном паттерне
years = {year for year in range(2000, 2023, 1)}


def analysis_csv_file(in_file):
    """Анализ csv файла и запись данных в списки: фио, контракт
    и общие данные"""
    # объявляем списки, куда будем записывать все фио, контракты
    # и все считанные данные
    all_fio, all_data, all_contract = list(), list(), list()

    # считываем файл
    df = pd.read_csv(
        in_file, sep=";", encoding="cp1251", keep_default_na=False
    )  # noqa: E501

    for line in df["comments"]:
        try:
            print(line)

            fio = re.findall(fio_pattern, str(line))
            print(fio)

            fio_text = "; ".join(map(str, [f[0].strip() for f in fio]))
            print(fio_text)

            contract = re.findall(contract_pattern, str(line))
            print(contract)

            contract_text = ";".join(
                map(str, [c.strip() for c in contract if int(c) not in years])
            )
            print(contract_text)
        except Exception as e:
            print("Перехват ошибок и выяснение, где проблема", e)

        all_fio.append(fio_text)
        all_data.append(line)
        all_contract.append(contract_text)

    return all_data, all_fio, all_contract


def create_csv_after_analysis(in_file, out_file):
    """Создание файла на основании проанализированных данных"""
    data, fio, contract = analysis_csv_file(in_file)

    df2 = pd.DataFrame({"comments": data, "ФИО": fio, "Договор(-а)": contract})
    df2.to_csv(out_file, sep=";", encoding="cp1251")


def main():
    input_file = "regular0612.csv"
    output_file = "out_full_final.csv"
    create_csv_after_analysis(input_file, output_file)


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
