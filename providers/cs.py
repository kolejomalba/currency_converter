import requests
import json
from decimal import Decimal

def cs(curr_in, curr_out, amount):
    """return list of tuples (currency - string, output amount - float)

    parameters:
        curr_in: iso code of input currency, string
        curr_out: iso code of output currency, string
        amount: amount in input currency, string
    """

    amount = Decimal(amount)

    with open('config.json', encoding='utf-8') as data_file:
        conf = json.load(data_file)
        try:
            api_key = conf["apikey-CS"]
        except KeyError:
            raise

    res = requests.get("https://api.csas.cz/sandbox/webapi/api/v1/exchangerates",
                    headers={"WEB-API-key":api_key}).json()

    # create new list where every currency base amount is 1 and rates are Decimal object
    r = []
    for i in res:
        i['cnbMid'] = Decimal(i['cnbMid']) / Decimal(i['amount'])
        r.append(i)
        # while at it, let's also find curr_in_rox, for later use, to save 1 for-loop
        if i['shortName'] == curr_in:
            curr_in_rox = i['cnbMid']

    # output is single currency:
    if curr_out is not None:
        if curr_in == 'CZK':
            for i in r:
                if i['shortName'] == curr_out:
                    return [(curr_out, round(float(amount / i['cnbMid']),2))]
        elif curr_out == 'CZK':
            for i in r:
                if i['shortName'] == curr_in:
                    return [(curr_out, round(float(amount * i['cnbMid']),2))]
        #neither output nor input is 'CZK':
        else:
            for i in r:
                if i['shortName'] == curr_in:
                    rate_in = i['cnbMid']
                if i['shortName'] == curr_out:
                    rate_out = i['cnbMid']
            return [(curr_out, round(float(amount*rate_in/rate_out),2))]

    # else, output is multiple currencies:
    else:
        o = []
        new_rates = []

        # input CZK
        if curr_in == 'CZK':
            for i in r:
                o.append((i['shortName'], float(round(amount / i['cnbMid'], 2))))

        # input 'not CZK'
        else:
            for i in r:
                if i['shortName'] != curr_in:
                    new_rates.append(( i['shortName'], curr_in_rox / i['cnbMid'] ))
                else:
                    new_rates.append(('CZK', i['cnbMid'] ))

            for i in new_rates:
                o.append((i[0], round(float(amount * i[1]), 2)))

        return o
