Introduction
------
currency_converter.py is a command line utility, for currency conversion using third party rate of exchange provider's API


Usage examples:
---------------

    currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK

    currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD

    currency_converter.py --amount 10.92 --input_currency £ --source cs

Available options:
------------------
    -h --help
    --amount            mandatory
    --input_currency    mandatory
    --output_currency   optional
    --source            optional, rates provider, eg. cs (Ceska Sporitelna)
                        default value: currencyconverterapi
                        (module of corresponding name must be present in "providers" folder)


Available rate of exchange provider modules
-------------------------------------------

**CurrencyConverterAPI** module:

- default module
- limitation: in free mode, they only return 10 rates at most, sometimes even less

**Ceska sporitelna** module, cs.py:

- uses cnbMid rate of exchange
- API Key needed, can be set in config.json as "apikey-CS"


To extend with additional modules:

- module must be placed to "providers" folder
- module name corresponds to the desired value of "source" command line option
- module must contain function of same name as module name
- function has 3 parameters of string type:

>   

    curr_in: iso code of input currency, string

    curr_in: iso code of input currency, string

    amount: amount in input currency, string

- function will return list of tuples, eg.:

>

     [(currency - string, output amount - float)]

or

     [(currency - string, output amount - float),
      (currency - string, output amount - float),
     ...]

Accuracy
--------

CurrencyConverterAPI: accuracy as per CurrencyConverterAPI terms

Ceska sporitelna and CNB modules:

* for amounts where CZK is neither output nor input currency, **resulting amount is inaccurate**, as rate of exchange in such case is an approximation
  only, based on CZK rates of exchange

Currency symbols
----------------

Besides valid currency ISO codes, also non-ISO symbols are allowed.
Since certain currencies use identical symbols, in config.json
it's possible to specify single ISO used for particular symbol.
