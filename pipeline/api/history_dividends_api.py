import certifi
import json
from urllib.request import urlopen
import os


def get_jsonparsed_data_history_dividends(symbol: str, api_key: str):
    """
    https://site.financialmodelingprep.com/developer/docs/#Historical-Dividends
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    api_key : str
    symbol : str
    Returns
    -------
    dict
    """
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}?apikey={api_key}'
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

