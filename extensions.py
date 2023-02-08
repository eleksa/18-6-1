import requests
from config import available_currencies
import json


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Указаны одинаковые валюты {base}, перевод невозможен')
        else:

            try:
                base_param = available_currencies[base]
            except KeyError:
                raise APIException(f'Указанная валюта {base} недоступна')

            try:
                quote_param = available_currencies[quote]
            except KeyError:
                raise APIException(f'Указанная валюта {quote} недоступна')

            try:
                amount = int(amount)
            except ValueError:
                raise APIException(f'Невозможно обработать указанное количество {amount}')

            url_api_resourse = f'https://min-api.cryptocompare.com/data/price?fsym={base_param}&tsyms={quote_param}'
            output_data = json.loads(requests.get(url=url_api_resourse).text)
            per_unit = float(output_data[quote_param])
            return per_unit
