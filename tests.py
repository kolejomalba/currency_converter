import unittest
import httpretty
import requests
import json

import currency_converter as cc

from providers.currencyconverterapi import currencyconverterapi
from providers.cs import cs

res = [{'valBuy': 16.69, 'valMid': 17.296, 'cnbMid': 17.3, 'name': 'dolar', 'version': 1, 'currMid': 17.296, 'amount': 1, 'shortName': 'AUD', 'validFrom': '2016-02-18', 'country': 'Australie', 'move': 0.18, 'currSell': 17.729, 'valSell': 17.9, 'currBuy': 16.864},
{'valBuy': 0.0, 'valMid': 0.0, 'cnbMid': 13.822, 'name': 'leva', 'version': 1, 'currMid': 13.82, 'amount': 1, 'shortName': 'BGN', 'validFrom': '2016-02-18', 'country': 'Bulharsko', 'move': -0.04, 'currSell': 14.165, 'valSell': 0.0, 'currBuy': 13.474},
{'valBuy': 16.97, 'valMid': 17.59, 'cnbMid': 17.567, 'name': 'dolar', 'version': 1, 'currMid': 17.59, 'amount': 1, 'shortName': 'CAD', 'validFrom': '2016-02-18', 'country': 'Kanada', 'move': 0.88, 'currSell': 18.029, 'valSell': 18.21, 'currBuy': 17.15},
{'valBuy': 23.77, 'valMid': 24.478, 'cnbMid': 24.498, 'name': 'frank', 'version': 1, 'currMid': 24.478, 'amount': 1, 'shortName': 'CHF', 'validFrom': '2016-02-18', 'country': 'Svycarsko', 'move': -0.27, 'currSell': 25.09, 'valSell': 25.19, 'currBuy': 23.867},
{'valBuy': 3.49, 'valMid': 3.621, 'cnbMid': 3.621, 'name': 'koruna', 'version': 1, 'currMid': 3.621, 'amount': 1, 'shortName': 'DKK', 'validFrom': '2016-02-18', 'country': 'Dansko', 'move': -0.06, 'currSell': 3.711, 'valSell': 3.75, 'currBuy': 3.53},
{'valBuy': 20.53, 'valMid': 21.277, 'cnbMid': 21.27, 'name': 'jen', 'version': 1, 'currMid': 21.277, 'amount': 100, 'shortName': 'JPY', 'validFrom': '2016-02-18', 'country': 'Japonsko', 'move': 0.17, 'currSell': 21.808, 'valSell': 22.02, 'currBuy': 20.745},
{'valBuy': 8.52, 'valMid': 8.735, 'cnbMid': 8.721, 'name': 'forint', 'version': 1, 'currMid': 8.735, 'amount': 100, 'shortName': 'HUF', 'validFrom': '2016-02-18', 'country': 'Madarsko', 'move': 0.52, 'currSell': 8.953, 'valSell': 9.0, 'currBuy': 8.516}]

res = json.dumps(res)


class TestCurrencyconverterapiModule(unittest.TestCase):
    @httpretty.activate
    def test_curr_curr_amount(self):
        httpretty.register_uri(httpretty.GET,
            'http://free.currencyconverterapi.com/api/v3/convert?q=CZK_USD&compact=ultra',
            body='{"CZK_USD":0.0402}')
        self.assertListEqual(currencyconverterapi('CZK', 'USD', 103.95), [("USD", 4.18)])

    @httpretty.activate
    def test_curr_none_amount(self):
        result = [('CNY', 27.95), ('EUR', 3.85), ('GBP', 2.99), ('HUF', 1192.9), ('JPY', 487.64), ('NOK', 36.64),
                  ('RUB', 322.71), ('SEK', 36.44), ('USD', 4.28)]
        httpretty.register_uri(httpretty.GET,
            "http://free.currencyconverterapi.com/api/v3/convert?q=CZK_USD,CZK_GBP,CZK_EUR,CZK_RUB,CZK_HUF,CZK_CNY,CZK_SEK,CZK_JPY,CZK_NOK&compact=ultra",
            body='{"CZK_USD":0.0412,"CZK_GBP":0.0288,"CZK_EUR":0.037,"CZK_RUB":3.1045,"CZK_HUF":11.4757,"CZK_CNY":0.2689,"CZK_SEK":0.3506,"CZK_JPY":4.6911,"CZK_NOK":0.3525}')
        self.assertListEqual(currencyconverterapi('CZK', None, 103.95), result)


class TestNormalizeCurrency(unittest.TestCase):
    def test_currency_symbol_normalization(self):
        self.assertEqual(cc.normalize_currency("$"), "USD")
        self.assertEqual(cc.normalize_currency("؋"), "AFN")
        self.assertEqual(cc.normalize_currency("kr"), "SEK")
        self.assertEqual(cc.normalize_currency("£"), "GBP")
        self.assertEqual(cc.normalize_currency("BGN"), "BGN")


class TestCsModule(unittest.TestCase):
    @httpretty.activate
    def test_curr_cs_conversion(self):
        httpretty.register_uri(httpretty.GET,
            "https://api.csas.cz/sandbox/webapi/api/v1/exchangerates",
            body = res)
        #regular conversion
        self.assertListEqual(cs("CZK", "AUD", 103.95), [("AUD", 6.01)])
        self.assertListEqual(cs("AUD", "CZK", 103.95), [("CZK", 1798.34)])
        #conversion of currency with base amount > 1
        self.assertListEqual(cs("CZK", "JPY", 103.95), [("JPY", 488.72)])
        self.assertListEqual(cs("JPY", "CZK", 103.95), [("CZK", 22.11)])

        # curr to curr, each non-czk, each with base amount > 1
        self.assertListEqual(cs("JPY", "HUF", 103.95), [("HUF", 253.53)])
        # curr to curr, each non-czk, one with base amount > 1
        self.assertListEqual(cs("JPY", "AUD", 103.95), [("AUD", 1.28)])
        self.assertListEqual(cs("AUD", "JPY", 103.95), [("JPY", 8454.8)])
        # curr to curr, each non-czk, each with base amount == 1
        self.assertListEqual(cs("AUD", "CHF", 103.95), [("CHF", 73.41)])

        # in CZK, out None
        self.assertListEqual(cs("CZK", None, 103.95), [('AUD', 6.01), ('BGN', 7.52), ('CAD', 5.92), ('CHF', 4.24), ('DKK', 28.71), ('JPY', 488.72),  ('HUF', 1191.95)])
        # in 'not CZK', out None
        self.assertListEqual(cs("CHF", None, 103.95), [('AUD', 147.2), ('BGN', 184.24), ('CAD', 144.96), ('CZK', 2546.57), ('DKK', 703.28), ('JPY', 11972.58), ('HUF', 29200.4)])
        # in 'not CZK', out None, curr with base amount > 1, and in the test response, there must be at least TWO lines where base amount > 1, to cover all the cases
        self.assertListEqual(cs("JPY", None, 5103.01), [('AUD', 62.74), ('BGN', 78.53), ('CAD', 61.79), ('CHF', 44.31), ('DKK', 299.75), ('CZK', 1085.41), ('HUF', 12445.94)])



class CommandLineTestCase(unittest.TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """
    @classmethod
    def setUpClass(cls):
        parser = cc.create_parser()
        cls.parser = parser


class CommandLineCurrencyconverterapiTestCase(CommandLineTestCase):
    @httpretty.activate
    def test_currencyconverterapi_cli(self):
        """
        Test currencyconverter API through command line
        """
        httpretty.register_uri(httpretty.GET,
            'http://free.currencyconverterapi.com/api/v3/convert?q=CZK_USD&compact=ultra',
            body='{"EUR_CZK":25.0}')

        args = self.parser.parse_args(['--amount', '100.0', '--input_currency', 'EUR', '--output_currency', 'CZK'])
        result = cc.launch(args.amount, args.input_currency, args.output_currency)
        r = json.loads(result)
        self.assertDictEqual((r["output"]),{'CZK': 2500.0})
        self.assertDictEqual((r["input"]),{'amount': 100.0, 'currency': 'EUR'})


class CommandLineCSTestCase(CommandLineTestCase):
    @httpretty.activate
    def test_cs_cli(self):
        """
        Test Ceska sporitelna API through command line
        """
        httpretty.register_uri(httpretty.GET,
            "https://api.csas.cz/sandbox/webapi/api/v1/exchangerates",
            body = res)

        args = self.parser.parse_args(['--amount', '103.95', '--input_currency', 'CZK', '--output_currency', 'AUD', '--source', 'cs'])
        result = cc.launch(args.amount, args.input_currency, args.output_currency, args.source)
        r = json.loads(result)
        self.assertDictEqual((r["output"]),{'AUD': 6.01})
        self.assertDictEqual((r["input"]),{'amount': 103.95, 'currency': 'CZK'})


if __name__ == '__main__':
    unittest.main()
