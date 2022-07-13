import select
import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


class YahooStockData:
    def __init__(self, stock_code="RELIANCE.NS"):
        self.stock_code = stock_code
        self._url = "https://finance.yahoo.com/quote/" + self.stock_code + "?p=" + self.stock_code + "&.tsrc=fin-srch"
        self.stock_values = {
            "price": None,
            "percentage_change": None,
            "volume": None,
            "pattern": None,
            "target": None,
            "change": None,
            'market_cap': None
        }
        self._web_content = None

    def get_real_time_data(self):
        self._web_content = BeautifulSoup(requests.get(self._url).text, "lxml")
        self._real_time_price("fin-streamer", "My(6px) Pos(r) smartphone_Mt(6px) W(100%)")
        self._get_volume("td",
                         "D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)")
        self._get_target("td",
                         "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)")
        self._get_pattern("span", "Fz(xs) Mb(4px)")

    def _real_time_price(self, search_key, class_path):
        try:
            texts = self._web_content_div(search_key, class_path)
            if texts:
                self.stock_values['price'] = texts[0]
                self.stock_values['change'] = texts[1]
                self.stock_values['percentage_change'] = texts[2]

        except ConnectionError:
            print("Connection Error")
            pass

    def _get_volume(self, search_key, class_path):
        try:
            texts = self._web_content_div(search_key, class_path)
            if texts:
                for count, key in enumerate(texts):
                    if key == "Volume":
                        self.stock_values["volume"] = texts[count + 1]
        except ConnectionError:
            print("Connection Error")
            pass

    def _get_pattern(self, search_key, class_path):
        try:
            texts = self._web_content_div(search_key, class_path)
            if texts:
                self.stock_values["latest_pattern"] = texts[0]
        except ConnectionError:
            print("Connection Error")
            pass

    def _get_target(self, search_key, class_path):
        try:
            texts = self._web_content_div(search_key, class_path)
            if texts:
                for count, target in enumerate(texts):
                    if target == "1y Target Est":
                        self.stock_values["target"] = texts[count + 1]
                    if target == 'Market Cap':
                        self.stock_values['market_cap'] = texts[count + 1]

        except ConnectionError:
            print("Connection Error")
            pass

    def _web_content_div(self, search_key, class_path):
        web_content_div = self._web_content.find_all("div", {"class": class_path})
        # print(web_content_div)
        try:
            spans = web_content_div[0].find_all(search_key)
            texts = [span.get_text() for span in spans]
        except IndexError:
            texts = []

        return texts


obj = YahooStockData()

while True:
    info = []
    col = []
    time_stamp = datetime.datetime.now() - datetime.timedelta(hours=3.5)
    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    obj.get_real_time_data()
    print(obj.stock_values)
    col = [[time_stamp], list(obj.stock_values.values())]
    col = sum(col, [])
    df = pd.DataFrame(col)
    df = df.T
    # df.to_csv(str(time_stamp[0:11]) + 'stock_data.csv', mode='a', header=False)
    print(col)
