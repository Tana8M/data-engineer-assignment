import certifi
import json
from urllib.request import urlopen
import os


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


api_key = os.environ['API_KEY']

url = f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/AAPL?apikey={api_key}'
print(get_jsonparsed_data(url))
