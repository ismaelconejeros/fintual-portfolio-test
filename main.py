import requests
from datetime import datetime

URL_VERY_CONVERSAVIVE_STREEP = "https://fintual.cl/api/real_assets/15077/days"
URL_CONSERVATIVE_CLOONEY = "https://fintual.cl/api/real_assets/188/days"
URL_MODERATE_PIT = "https://fintual.cl/api/real_assets/187/days"
URL_RISKY_NORRIS = "https://fintual.cl/api/real_assets/186/days"

class Stock():
    def __init__(self, url):
        self.investment = 0
        self.shares = 0
        self.price_now = 0
        self.url = url
    
    def price(self, date):
        parameters = {
            "date" : date
        }
        my_request = requests.get(self.url, params=parameters).json()
        return my_request['data'][0]['attributes']['price']

    def last_price(self):
        my_request = requests.get(self.url).json()
        self.price_now = my_request['data'][0]['attributes']['price']
        return self.price_now

class Portfolio():
    def __init__(self):
        self.stocks = []
        self.investment = 0
        self.value = 0

    def update(self):
        self.value = 0
        for stock in self.stocks:
            self.value += stock.shares * stock.last_price()

    def add_stock(self, url, amount):
        new_stock = Stock(url)
        new_stock.shares = amount / new_stock.last_price()
        self.investment += amount
        new_stock.amount = amount
        self.stocks.append(new_stock)

    def profit(self, date_from, date_to):
        value_1 = 0
        value_2 = 0
        for stock in self.stocks:
            value_1 += stock.price(date_from) * stock.shares
            value_2 += stock.price(date_to) * stock.shares
        return ((value_2 - value_1) / value_1)

    def profit_annualized(self, date_from, date_to):
        date_list_1 = date_from.split("-")
        date_list_2 = date_to.split("-")
        date_1 = datetime(int(date_list_1[0]), int(date_list_1[1]), int(date_list_1[2]))
        date_2 = datetime(int(date_list_2[0]), int(date_list_2[1]), int(date_list_2[2]))
        days = (date_2 - date_1).days

        value_1 = 0
        value_2 = 0
        for stock in self.stocks:
            value_1 += stock.price(date_from) * stock.shares
            value_2 += stock.price(date_to) * stock.shares
        return (((value_2 - value_1) / value_1) / days) * 365

portfolio = Portfolio()

portfolio.add_stock(URL_VERY_CONVERSAVIVE_STREEP, 1000)
portfolio.add_stock(URL_CONSERVATIVE_CLOONEY, 800)
portfolio.add_stock(URL_MODERATE_PIT, 300)
portfolio.add_stock(URL_RISKY_NORRIS, 500)
portfolio.update()

profit = portfolio.profit("2021-01-01", "2021-02-01")
annualized_profit = portfolio.profit_annualized("2021-01-01", "2021-02-01")

print(f"The profit of the portfolio between those dates is: {profit*100:.2f}%.")
print(f"The annualized profit of the portfolio between those dates is: {annualized_profit*100:.2f}%.")


