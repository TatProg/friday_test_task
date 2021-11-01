from pprint import pprint
from dadata import Dadata
import pandas as pd
import json


def main():
    data = pd.read_excel('external_resources/example.xlsx')
    data_list = data['ИНН'].tolist()
    print(data_list)

    api_key = '20a2e19e13aa2e1934b929252bf13b9e17417532'
    secret_key = '6babcd2dfaede669600b3e7992ce86e14fb986cf'
    dadata = Dadata(api_key)
    result = []
    for dl in data_list:
        res = dadata.find_by_id(name="party", query=dl)

        if len(res) > 0:
            alert_flag = False

            for r in res:
                if r['data']['state']['liquidation_date'] is not None:
                    alert_flag = True

            if alert_flag:
                result.append('is bad')
            else:
                result.append('is good')
        else:
            result.append('invalid Value')

    print(result)
    s1 = pd.Series(data_list, name='INN')
    s2 = pd.Series(result, name='RESULT')
    final_res = pd.concat([s1, s2], axis=1)
    final_res.to_excel('external_resources/final_result.xlsx')


if __name__ == '__main__':
    main()
