# -*- coding: utf8 -*-
class CurrencyHelper:
	@staticmethod
	def get_currency_desc(currency_code):
		return {
		840: "USD",
		978: "EUR",
		980: "UAH",
		643: "RUB", # RUB (643) — российский рубль после деноминации 1998 года;
		810: "RUR", # RUR (810) — российский рубль до деноминации 1998 года; https://ru.wikipedia.org/wiki/ISO_4217
		}[currency_code]