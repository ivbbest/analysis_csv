"""Анализ csv файла и для контракта, кд, договора
вытаскивать максимум информации, включая дату и тд."""

import re
import time

import pandas as pd

start_time = time.time()

# паттерн первый для договора, используется в общем случае и универсален
contract_pattern_main = r"((дог|кд|к\/д|догN|КД|КД_|к\.д|к\д)?\s+(№|N)?\s?(\d){2,}\s+(от\s?(\w{2}(\.|\/|\,)){2}\w{2,4}))"  # noqa: E501
# паттерн фио
fio_pattern = r"([А-ЯЁ][А-Яа-яёЁ]+\s{1,2}?([А-ЯЁ][А-Яа-яёЁ]+\s?|[А-ЯЁ]+\.|[А-ЯЁ]+\,|[А-ЯЁ]+|[А-ЯЁ]+\/){2})"  # noqa: E501
# второй паттерн работает для отдельных случаев, чтобы добавить больше договор в итоговый файл # noqa: E501
contract_pattern_other = r"(дог|кд|к\/д|догN|КД|КД_|к\.д|к\д|N|№|Дог\.|кд\.|Дог\.№|дог\.№|КД\s+№)([\s|\d|\.|\-|от|ОЦ|НД|/|_|N|Z|PHA|УПД]{3,})"  # noqa: E501


def analysis_csv_file(in_file):
    """Анализ csv файла и запись данных в списки:
    фио, контракт и общие данные"""
    # объявляем списки, куда будем записывать все фио,
    # контракты и все считанные данные
    all_fio = list()
    all_data = list()
    all_contract = list()

    # считываем файл
    df = pd.read_csv(
        in_file, sep=";", encoding="cp1251", keep_default_na=False
    )  # noqa: E501

    for line in df["comments"]:
        print(line)

        fio = re.findall(fio_pattern, str(line))
        print(fio)

        fio_text = "; ".join(map(str, [f[0].strip() for f in fio]))
        print(fio_text)

        contract = re.findall(contract_pattern_main, str(line))
        print(contract)

        # если для контракта не срабатывает первый паттерн для анализа,
        # то использую второй
        try:
            if len(contract) == 0:
                contract = re.findall(contract_pattern_other, str(line))
                print(contract)
                # если не срабатывает второй, то записываем пустую строку
                if len(contract) != 0:
                    contract_text = "".join(map(str, contract[0])).strip()
                else:
                    contract_text = ""
            else:
                contract_text = "; ".join(
                    map(str, [c[0].strip() for c in contract])
                ).strip()
        except Exception as e:
            print("Перехват ошибок и выяснение, где проблема", e)
        finally:
            print(contract_text)

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
    output_file = "out_full6.csv"
    create_csv_after_analysis(input_file, output_file)


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
