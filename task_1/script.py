from pprint import pprint
from dadata import Dadata
import pandas as pd
import json
import datetime


def check_company(json_list: list):
    """
    Проверка компании по двум критериям:
    1 - Ликвидрована ли компания
    2 - Насколько компания "молода"
    Была идея проверить по адресам, указанным при государственной регистрации (ссылка на датасет ниже)
    в качестве места нахождения несколькими юридическими лицам, однако немного не хватило времени для этого.
    Другие проверки сделать сложно или невозможно, ввиду отсутствия данных (проверка уставного капитала, проверка лиц и тд)
    https://www.nalog.gov.ru/opendata/7707329152-masaddress/
    :param json_list: результат запроса find_by_id. Может быть несколько объектов.
    :return: True or False. Ответ на вопрос, можно ли доверять этой компании?
    """
    for jl in json_list:
        if jl['data']['state']['liquidation_date'] is not None:
            return False
        try:
            # Из запроса получаем Epoch в милисекундах. Поэтому делим на 1000 и вычисляем разницу.
            delta_registration_date = datetime.datetime.now() - datetime.datetime.fromtimestamp(
                jl['data']['state']['registration_date'] / 1000)
            # Проверка на возраст компании, должна быть старше 1 года, те 365 дней
            if delta_registration_date.days < 365:
                return False
        # Филиалы и дочки имеют другой формат даты регистрации.
        except TypeError:
            print('Нет информации о дате регистрации компании')
            print(jl['data']['inn'])
            print(jl['value'])

        return True


def main():
    data = pd.read_excel('external_resources/example.xlsx')
    data_list = data['ИНН'].tolist()
    print(data_list)

    # Оставил исключительно для тестов.
    api_key = '20a2e19e13aa2e1934b929252bf13b9e17417532'

    dadata = Dadata(api_key)
    result_list = []
    for dl in data_list:
        res = dadata.find_by_id(name="party", query=dl)
        if check_company(res):
            result_list.append(' is a good company')
        else:
            result_list.append('ALARM!')

    # Печать и добавление в xlsx
    print(result_list)
    final_res = pd.concat([pd.Series(data_list, name='INN'), pd.Series(result_list, name='RESULT')], axis=1)
    final_res.to_excel('external_resources/final_result.xlsx')


if __name__ == '__main__':
    main()
