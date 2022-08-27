import os
import certifi
import json
from urllib.request import urlopen

'''
https://site.financialmodelingprep.com/developer/docs/delisted-companies-api/
OVERVIEW
Access a list of delisted companies from the US exchanges.
Stock delisting is the removal of a recorded stock from a stock trade exchange, and accordingly it would presently don't be exchanged on the bourse.
Unlike delisted stock, the ones still trading often pay dividend, you can access them via our Dividend Calendar API .

Query String Parameters
page : Number
'''


def get_jsonparsed_data_delisted_company(api_key: str):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    api_key : str

    Returns
    -------
    dict
    """
    url = f"https://financialmodelingprep.com/api/v3/delisted-companies?page=0&apikey={api_key}"
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

