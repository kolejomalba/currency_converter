import requests
import json


def call_api(curr_pair):
    url = 'http://free.currencyconverterapi.com/api/v3/convert?q={}&compact=ultra'.format(curr_pair)
    return requests.get(url).json()


def currencyconverterapi(curr_in, curr_out, amount):
    """return list of tuples (currency - string, output amount - float)

    parameters:
        curr_in: iso code of input currency, string
        curr_out: iso code of output currency, string
        amount: amount in input currency, string
    """


    if curr_out is not None:
        curr_pair = curr_in + '_' + curr_out
        rox = call_api(curr_pair)
        return [(curr_out, round(float(amount) * float(rox[curr_pair]), 2))]

    elif curr_out is None:
        # free currencyconverterapi is limited to 10 pairs but in fact returns
        # even less sometimes, thus the extra lc list as workaround
        lc = ['USD', 'CZK', 'GBP', 'EUR', 'RUB', 'HUF', 'CNY', 'SEK', 'JPY', 'NOK']
        curr_pair = ','.join(list(map(lambda x: curr_in + '_' + x, [value for value in lc if value != curr_in])))
        rox = call_api(curr_pair)
        return sorted([(x[4:], round(float(amount) * float(rox[x]), 2)) for x in rox])
