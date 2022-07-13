import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import matplotlib
import math

matplotlib.use('Qt5Agg')


class Visualization:
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=[width, height], dpi=dpi)
        self.fig.patch.set_facecolor('#121416')
        self.gs = self.fig.add_gridspec(6, 6)
        self.stock_data = None  # self.read_data()
        self.plot_data = self.read_data_nifty()
        self.animation = None
        self.axes = [self.fig.add_subplot(self.gs[0:4, 0:4]),
                     self.fig.add_subplot(self.gs[0, 4:6]),
                     self.fig.add_subplot(self.gs[1, 4:6]),
                     self.fig.add_subplot(self.gs[2, 4:6]),
                     self.fig.add_subplot(self.gs[3, 4:6]),
                     self.fig.add_subplot(self.gs[4, 4:6]),
                     self.fig.add_subplot(self.gs[5, 4:6]),
                     self.fig.add_subplot(self.gs[4, 0:4]),
                     self.fig.add_subplot(self.gs[5, 0:4])]
        for ax in self.axes:
            self.figure_design(ax)

        self.animate()

    @staticmethod
    def figure_design(ax):
        ax.set_facecolor("#091217")
        ax.tick_params(axis='both', labelsize=14, colors='white')
        ax.ticklabel_format(useOffset=None)
        ax.spines['bottom'].set_color('#808080')
        ax.spines['top'].set_color('#808080')
        ax.spines['left'].set_color('#808080')
        ax.spines['right'].set_color('#808080')

    @staticmethod
    def sub_plot(ax, stock_name, data, latest_price=0, latest_change="+5.5 (+ 1.0 %)", pattern="Bullish", target=0):
        ax.clear()
        ax.plot(list(range(1, len(data["close"]) + 1)), data["close"], color='white', linewidth=2)

        y_min = data["close"].min()
        y_max = data['close'].max()
        y_std = data['close'].std()

        if not math.isnan(y_max):
            ax.set_ylim([y_min - y_std * 0.5, y_max + y_std * 3])

        ax.text(0.02, 0.95, stock_name, transform=ax.transAxes, color='#FFBF00', fontsize=8,
                fontweight='bold', horizontalalignment='left', verticalalignment='top')

        ax.text(0.2, 0.95, latest_price, transform=ax.transAxes, color='white', fontsize=8,
                fontweight='bold', horizontalalignment='left', verticalalignment='top')

        if latest_change == '+':
            color_code = '#18b800'
        else:
            color_code = '#ff3503'

        ax.text(0.4, 0.95, latest_change, transform=ax.transAxes, color=color_code, fontsize=8,
                fontweight='bold', horizontalalignment='left', verticalalignment='top')

        if pattern == "Bullish":
            color_code = '#18b800'
        elif pattern == "Bearish":
            color_code = '#ff3503'
        else:
            color_code = 'white'

        ax.text(0.98, 0.95, pattern, transform=ax.transAxes, color=color_code, fontsize=8,
                fontweight='bold', horizontalalignment='right', verticalalignment='top')
        ax.text(0.98, 0.75, target, transform=ax.transAxes, color=color_code, fontsize=8,
                fontweight='bold', horizontalalignment='right', verticalalignment='top')

        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

    def plot_rsi(self, i):
        self.axes[8].clear()
        self.axes[8].axes.yaxis.set_visible(False)
        self.axes[8].set_ylim([-5, 105])

        self.axes[8].axhline(30, linestyle='-', color='green', linewidth=0.5)
        self.axes[8].axhline(50, linestyle='-', color='white', linewidth=0.5)
        self.axes[8].axhline(70, linestyle='-', color='red', linewidth=0.5)
        self.axes[8].plot(self.plot_data['x_axis'].iloc[0:i], self.plot_data['rsi'].iloc[0:i], color='#08a0e9',
                          linewidth=1.5)

        self.axes[8].text(0.01, 0.95, 'RSI(14) :' + str(round(self.plot_data['rsi'].iloc[-1], 2)),
                          transform=self.axes[8].transAxes, color='white', fontsize=8,
                          fontweight='bold', horizontalalignment='left', verticalalignment='top')

        x_date = [i for i in self.plot_data['Time']]

        def my_date(x, pos=None):
            try:
                t = x_date[int(x)].strftime('%H:%M')
                return x_date[int(x)].strftime('%H:%M')
            except IndexError:
                return ''

        self.axes[8].xaxis.set_major_formatter(mticker.FuncFormatter(my_date))
        self.axes[8].grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
        self.axes[8].tick_params(axis='x', which='major', labelsize=12)

    def plot_volume_bar(self, i):
        self.axes[7].axes.yaxis.set_visible(False)

        pos = self.plot_data['open'] - self.plot_data['close'] < 0
        neg = self.plot_data['open'] - self.plot_data['close'] > 0

        self.plot_data['x_axis'] = list(range(1, len(self.plot_data['volume_diff']) + 1))

        self.axes[7].bar(self.plot_data['x_axis'][pos], self.plot_data['volume_diff'][pos], color="#18b800", width=0.8,
                         align='center')
        self.axes[7].bar(self.plot_data['x_axis'][neg], self.plot_data['volume_diff'][neg], color="#ff3503", width=0.8,
                         align='center')

        y_max = self.plot_data['volume_diff'].max()
        y_std = self.plot_data['volume_diff'].std()
        vol = self.plot_data['volume_diff'].iloc[-1]
        if not math.isnan(y_max):
            self.axes[7].set_ylim([0, y_max + y_std * 3])

        self.axes[7].text(0.01, 0.95, 'Volume :' + '{:,}'.format((int(vol))),
                          transform=self.axes[8].transAxes, color='white', fontsize=8,
                          fontweight='bold', horizontalalignment='left', verticalalignment='top')

        self.axes[7].grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
        self.axes[7].set_xticklabels([])

    def main_plot(self, i):
        stock_name = 'NIFTY'
        candle_counter = range(i) #len(self.plot_data['open']) - 1)
        ohlc = []
        for candle in candle_counter:
            temp = candle_counter[candle], self.plot_data['open'][candle], \
                   self.plot_data['high'][candle], \
                   self.plot_data['low'][candle], \
                   self.plot_data['close'][candle]
            ohlc.append(temp)

        self.axes[0].clear()
        candlestick_ohlc(self.axes[0], ohlc, width=0.4, colorup='#18b800', colordown='#ff3503')

        self.axes[0].plot(self.plot_data['MA5'][0:i], color='pink', linestyle='-', linewidth=1, label='5 minutes SMA')
        self.axes[0].plot(self.plot_data['MA10'][0:i], color='orange', linestyle='-', linewidth=1, label='10 minutes SMA')
        self.axes[0].plot(self.plot_data['MA20'][0:i], color='#08a0e9', linestyle='-', linewidth=1, label='20 minutes SMA')

        leg = self.axes[0].legend(loc='upper left', facecolor='#121416', fontsize=10)
        for text in leg.get_texts():
            plt.setp(text, color='w')

        self.axes[0].text(0.005, 1.05, stock_name, transform=self.axes[0].transAxes, color='black', fontsize=18,
                          fontweight='bold', horizontalalignment='left', verticalalignment='center',
                          bbox=dict(facecolor='#FFBF00'))

        # self.axes[0].text(0.3, 1.05, latest_price, transform=self.axes[0].transAxes, color='white', fontsize=18,
        #                   fontweight='bold', horizontalalignment='center', verticalalignment='center')

        # if latest_change[0] == '+':
        #     color_code = '#18b800'
        # else:
        #     color_code = '#ff3503'

        # self.axes[0].text(0.4, 1.05, latest_change, transform=self.axes[0].transAxes, color=color_code, fontsize=18,
        #                   fontweight='bold', horizontalalignment='left', verticalalignment='center')

        # self.axes[0].text(0.6, 1.05, self.stock_data['target'][-1], transform =self.axes[0].transAxes, color='#08a0e9',
        #                  fontsize=18, fontweight='bold', horizontalalignment='left', verticalalignment='center',
        #                  bbox=dict(facecolor='#FFBF00'))
        time_stamp = datetime.datetime.now()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')

        self.axes[0].text(1.315, 1.05, time_stamp, transform=self.axes[0].transAxes, color='white', fontsize=12,
                          fontweight='bold', horizontalalignment='left', verticalalignment='center',
                          bbox=dict(facecolor='#FFBF00'))
        self.axes[0].grid('gridOn', color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
        self.axes[0].set_xticklabels([])

    def convert_string_to_number(self, column):
        if isinstance(self.stock_data.iloc[0, self.stock_data.columns.get_loc(column)], str):
            self.stock_data[column] = self.stock_data[column].str.replace(',', '')
            self.stock_data[column] = self.stock_data[column].astype(float)

    def read_data(self, file_name, stock_name, use_cols):
        self.stock_data = pd.read_csv(file_name, header=None, usecols=use_cols,
                                      names=['time', stock_name, 'change', 'volume', 'pattern', 'target'],
                                      index_col='time', parse_dates=['time'])

        self.stock_data.index = pd.DatetimeIndex(self.stock_data.index)
        self.convert_string_to_number(stock_name)
        self.convert_string_to_number('volume')
        self.convert_string_to_number('target')

        latest_info = self.stock_data.iloc[-1, :]
        latest_price = str(latest_info.iloc[0])
        latest_change = str(latest_info.iloc[1])

        df_vol = self.stock_data['volume'].resample('1Min').mean()
        data = self.stock_data[stock_name].resample('1Min').ohlc()
        data['time'] = data.index
        data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')

        data['MA5'] = data['close'].rolling(5).mean()
        data['MA10'] = data['close'].rolling(10).mean()
        data['MA20'] = data['close'].rolling(20).mean()

        data['volume_diff'] = df_vol.diff()
        data[data['volume_diff'] < 0] = None
        data.dropna(axis=0, inplace=True)

        return data, latest_price, latest_change

    def read_data_nifty(self, file_name="NIFTY_2008_2020.csv", stock_name="NIFTY"):
        self.stock_data = pd.read_csv(file_name, index_col='Time', parse_dates=['Time'])
        self.stock_data.drop(["Instrument"], axis=1, inplace=True)
        # self.stock_data = self.stock_data.iloc[-1000:, :]
        self.stock_data.dropna(axis=0, inplace=True)
        self.stock_data.index = pd.DatetimeIndex(self.stock_data.index)

        self.convert_string_to_number("Open")
        self.convert_string_to_number('High')
        self.convert_string_to_number('Low')
        self.convert_string_to_number('Close')
        self.convert_string_to_number('Volume')

        latest_info = self.stock_data.iloc[-1, :]
        latest_price = str(latest_info.iloc[2])

        df_vol = self.stock_data['Volume'].resample('1Min').mean()

        self.plot_data = self.stock_data["Close"].resample('1Min').ohlc()
        self.plot_data['Time'] = self.plot_data.index
        self.plot_data['Time'] = pd.to_datetime(self.plot_data['Time'], format='%Y-%m-%d %H:%M:%S')

        self.plot_data['MA5'] = self.plot_data['close'].rolling(5).mean()
        self.plot_data['MA10'] = self.plot_data['close'].rolling(10).mean()
        self.plot_data['MA20'] = self.plot_data['close'].rolling(20).mean()
        self.compute_rsi(14)

        self.plot_data['volume_diff'] = df_vol.diff()
        self.plot_data[self.plot_data['volume_diff'] < 0] = None
        self.plot_data.dropna(axis=0, inplace=True)
        self.plot_data.reset_index(drop=True, inplace=True)
        return self.plot_data

    def compute_rsi(self, time_window):
        diff = self.plot_data["close"].diff(1).dropna()

        up_change = 0 * diff
        down_change = 0 * diff

        up_change[diff > 0] = diff[diff > 0]
        down_change[diff < 0] = diff[diff < 0]

        up_change_avg = up_change.ewm(com=time_window - 1, min_periods=time_window).mean()
        down_change_avg = up_change.ewm(com=time_window - 1, min_periods=time_window).mean()

        rs = abs(up_change_avg / down_change_avg)
        rsi = 100 - 100 / (1 + rs)

        self.plot_data['rsi'] = rsi

    def animate_update(self, i):
        stock_name = "NIFTY"
        # time_stamp = datetime.datetime.now() - datetime.timedelta(hours=13)
        # time_stamp = time_stamp.strftime('%Y-%m-%d')
        # file_name = '2022-07-03 stock_data.csv'  # str(time_stamp) + 'stock_data.csv'

        # data, latest_price, latest_change = self.read_data(file_name, "RELIANCE.NS", [1, 2, 3, 4, 5, 6])
        # data = self.read_data_nifty("NIFTY_2008_2020.csv")
        ###
        self.main_plot(i)
        #####

        self.sub_plot(self.axes[1], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)
        self.sub_plot(self.axes[2], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)
        self.sub_plot(self.axes[3], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)
        self.sub_plot(self.axes[4], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)
        self.sub_plot(self.axes[5], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)
        self.sub_plot(self.axes[6], stock_name, self.plot_data.iloc[0:i,:], latest_price=0, latest_change="+5.5 (+ 1.0 %)",
                      pattern="Bullish",
                      target=0)

        self.plot_volume_bar(i)

        self.plot_rsi(i)

    def animate(self):
        self.animation = animation.FuncAnimation(self.fig, self.animate_update, frames=60, interval=1, blit=False)


# #
# x = Visualization()
# plt.show()

# x.animate()
# # x.animate()
# ani = animation.FuncAnimation(fig=x.fig, func=x.animate, interval=1)

# # data, p = x.read_data_nifty("NIFTY_2008_2020.csv")
# # print(data)
