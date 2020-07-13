"""
Currency Converter, currency_converter.py by Tomas D., 2016-01-16
Converts input currency to output currency(ies) at currrent ROX

Usage examples:
    currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
    currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
    currency_converter.py --amount 10.92 --input_currency £

Options:
    -h --help
    --amount            mandatory
    --input_currency    mandatory
    --output_currency   optional
    --source            optional, rates provider, eg. cs (Ceska Sporitelna)


Configuration:
    through config.json
"""
import argparse
import simplejson
import sys

with open('config.json', encoding='utf-8') as data_file:
    config = simplejson.load(data_file)


def normalize_currency(c):
    """
    Accepts ISO 4217 currency code or currency symbol, returns currency code.
    Default currency code for particular symbols can be set in config.json.
    """
    with open('currencies.json', encoding='utf-8') as data_file:
        currencies = simplejson.load(data_file)

    if c in currencies:
        return c
    elif c in config:
        return config[c]
    else:
        with open('symbols.json', encoding='utf-8') as data_file:
            symbols = simplejson.load(data_file)
        if c in symbols.values():
            return list(symbols.keys())[list(symbols.values()).index(c)]
        else:
            raise ValueError('Could not find {} in our list.'.format(c))


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--amount', type = float, required = True,
                    help = "amount to convert in input currency")
    parser.add_argument('--input_currency', required = True,
                    help = "3 letters name or currency symbol")
    parser.add_argument('--output_currency',
                    help = "optional, 3 letters name or currency symbol")
    parser.add_argument('--source',
                    help = "source of rates, default: currencyconverterapi")
    return parser

def launch(amount, input_currency, output_currency, source='currencyconverterapi'):
    if not source:
        source = 'currencyconverterapi'

    curr_in = normalize_currency(input_currency)

    if output_currency:
        curr_out = normalize_currency(output_currency)
    else:
        curr_out = output_currency

    if curr_in == curr_out:
        raise ValueError('Input and output currency identical. Nothing to convert.')

    provider = source.lower()

    try:
        processor = import_from("providers.{}".format(provider), '{}'.format(provider))
    except:
        raise ImportError('Selected rates provider invalid. Module missing.')

    result = {}
    result["output"] = dict(processor(curr_in,curr_out, amount))
    result["input"] = {"amount": amount, "currency": curr_in }

    # for easier unittests, vary output depending on how script is run
    if __name__ == '__main__':
        sys.stdout.write(simplejson.dumps(result, indent = 4, sort_keys=True))
    else:
        return(simplejson.dumps(result, indent = 4, sort_keys=True))

def main():
    parser = create_parser()
    args = parser.parse_args()
    launch(args.amount, args.input_currency, args.output_currency, args.source)

if __name__ == '__main__':
    main()
