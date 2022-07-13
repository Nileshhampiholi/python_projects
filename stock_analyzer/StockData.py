import time

import requests
import pandas as pd
import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class StockData:

    def __init__(self):
        self.headers = {
            'User-Agent':
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def pre_market_data(self):
        pre_market_key = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                          "Others": "OTHERS", "All": "ALL"}
        key = "Securities in F&O"  # input
        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_key[key]}",
                                headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        # return list(df['symbol'])
        return df

    def live_market_data(self):
        live_market_index = {
            'Broad Market Indices': ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                                     'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100',
                                     'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200'],
            'Sectoral Indices': ["NIFTY AUTO", "NIFTY BANK", "NIFTY ENERGY", "NIFTY FINANCIAL SERVICES",
                                 "NIFTY FINANCIAL SERVICES 25/50", "NIFTY FMCG", "NIFTY IT", "NIFTY MEDIA",
                                 "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK", "NIFTY REALTY",
                                 "NIFTY PRIVATE BANK"],
            'Others': ['Securities in F&O', 'Permitted to Trade'],
            'Strategy Indices': ['NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
                                 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30',
                                 'NIFTY ALPHA 50', 'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30',
                                 'NIFTY200 MOMENTUM 30'],
            'Thematic Indices': ['NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE',
                                 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                                 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15']}

        indices = "Broad Market Indices"  # input
        key = "NIFTY 50"  # input
        data = self.session.get(
            f"https://www.nseindia.com/api/equity-stockIndices?index={live_market_index[indices][live_market_index[indices].index(key)].upper().replace(' ', '%20').replace('&', '%26')}",
            headers=self.headers).json()["data"]
        df = pd.DataFrame(data)

        # return list(df["symbol"])
        return df

    def get_fno_data(self):
        stocks = ["WIPRO"]
        key = stocks[0]  # input
        data = self.session.get("https://www.nseindia.com/get-quotes/derivatives?symbol=WIPRO",
                                headers=self.headers).json()["data"]
        print(data)
        # new_data = []
        # for i in data:
        #     new_data.append(i["metadata"])
        # df = pd.DataFrame(new_data)
        # # return list(df['symbol'])
        # return df

    def holidays(self):
        holiday = ["clearing", "trading"]
        # key = input(f'Select option {holiday}\n: ')
        key = "trading"  # input
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={holiday[holiday.index(key)]}',
                                headers=self.headers).json()
        df = pd.DataFrame(list(data.values())[0])
        return df


nse = StockData()
columns = ["open", "dayHigh", "dayLow", "lastPrice", "previousClose", "change", "pChange", "totalTradedVolume",
           "totalTradedValue", "lastUpdateTime"]
data = []
# print(nse.pre_market_data())
start_time = time.time()
file = 0
while True:

    data.append(nse.live_market_data().loc[0, ["open", "dayHigh", "dayLow", "lastPrice", "previousClose",
                                               "change", "pChange", "totalTradedVolume", "totalTradedValue",
                                               "lastUpdateTime"]].values)
    stock_df = pd.DataFrame(data, columns=columns)
    stock_df.to_csv('nifty_data' + str(file) + '.csv', mode='a', header=False)
    print(data)

    if time.time() >= start_time + 600:
        start_time = time.time()
        file += 1
        data = []
# print(nse.get_fno_data())
# print(nse.holidays())
