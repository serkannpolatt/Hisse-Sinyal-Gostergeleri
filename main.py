import numpy as np
import pandas as pd
import pandas_ta as ta
from tvDatafeed import TvDatafeed, Interval
import streamlit as st
import ssl
from urllib import request


# Function to retrieve stock fundamental data
def Hisse_Temel_Veriler():
    url1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
    context = ssl._create_unverified_context()
    response = request.urlopen(url1, context=context)
    url1 = response.read()
    df = pd.read_html(url1, decimal=',', thousands='.')
    df1 = df[2]  # Summary table of all stocks
    return df1

tv = TvDatafeed()

# Tillson T3 calculation function
def TillsonT3(Close, high, low, vf, length):
    ema_first_input = (high + low + 2 * Close) / 4
    e1 = ta.ema(ema_first_input, length)
    e2 = ta.ema(e1, length)
    e3 = ta.ema(e2, length)
    e4 = ta.ema(e3, length)
    e5 = ta.ema(e4, length)
    e6 = ta.ema(e5, length)

    c1 = -1 * vf * vf * vf
    c2 = 3 * vf * vf + 3 * vf * vf * vf
    c3 = -6 * vf * vf - 3 * vf - 3 * vf * vf * vf
    c4 = 1 + 3 * vf + vf * vf * vf + 3 * vf * vf
    T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3
    return T3

# OTT calculation function
def OTT(df, prt, prc):
    pds = prt
    percent = prc
    alpha = 2 / (pds + 1)

    df['ud1'] = np.where(df['Close'] > df['Close'].shift(1), (df['Close'] - df['Close'].shift()), 0)
    df['dd1'] = np.where(df['Close'] < df['Close'].shift(1), (df['Close'].shift() - df['Close']), 0)
    df['UD'] = df['ud1'].rolling(9).sum()
    df['DD'] = df['dd1'].rolling(9).sum()
    df['CMO'] = ((df['UD'] - df['DD']) / (df['UD'] + df['DD'])).fillna(0).abs()

    df['Var'] = 0.0
    for i in range(pds, len(df)):
        df.loc[df.index[i], 'Var'] = (alpha * df.loc[df.index[i], 'CMO'] * df.loc[df.index[i], 'Close']) + (1 - alpha * df.loc[df.index[i], 'CMO']) * df.loc[df.index[i - 1], 'Var']

    df['fark'] = df['Var'] * percent * 0.01
    df['newlongstop'] = df['Var'] - df['fark']
    df['newshortstop'] = df['Var'] + df['fark']
    df['longstop'] = 0.0
    df['shortstop'] = 999999999999999999

    df['longstop'] = np.where(df['newlongstop'] > df['longstop'].shift(1), df['newlongstop'], df['longstop'].shift(1))
    df['shortstop'] = np.where(df['newshortstop'] < df['shortstop'].shift(1), df['newshortstop'], df['shortstop'].shift(1))

    df['xlongstop'] = np.where((df['Var'].shift(1) > df['longstop'].shift(1)) & (df['Var'] < df['longstop'].shift(1)), 1, 0)
    df['xshortstop'] = np.where((df['Var'].shift(1) < df['shortstop'].shift(1)) & (df['Var'] > df['shortstop'].shift(1)), 1, 0)

    df['trend'] = 0
    df['dir'] = 0

    df['trend'] = np.where(df['xshortstop'] == 1, 1, np.where(df['xlongstop'] == 1, -1, df['trend'].shift(1)))
    df['dir'] = np.where(df['xshortstop'] == 1, 1, np.where(df['xlongstop'] == 1, -1, df['dir'].shift(1).fillna(1)))

    df['MT'] = np.where(df['dir'] == 1, df['longstop'], df['shortstop'])
    df['OTT'] = np.where(df['Var'] > df['MT'], df['MT'] * (200 + percent) / 200, df['MT'] * (200 - percent) / 200)

    df['OTT2'] = df['OTT'].shift(2)
    df['OTT3'] = df['OTT'].shift(3)

    return df

# Function to generate indicator signals
def indicator_Signals(Hisse_Adı, Lenght_1, vf, prt, prc):
    data = tv.get_hist(symbol=Hisse_Adı, exchange='BIST', interval=Interval.in_daily, n_bars=500)
    data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

    OTT_Signal = OTT(data.copy(deep=True), prt, prc)
    Tillson = TillsonT3(data['Close'], data['High'], data['Low'], vf, Lenght_1)
    Zscore = ta.zscore(data['Close'], 21, 1)
    Zsma = ta.sma(Zscore)

    data['OTT'] = OTT_Signal['OTT3']
    data['Var'] = OTT_Signal['Var']
    data['Tillson'] = Tillson
    data['Zscore'] = Zscore
    data['ZSMA'] = Zsma

    data['OTT_Signal'] = data['Var'] > OTT_Signal['OTT3']
    data['Zscore_Signal'] = data['Zscore'] > 0.85

    data['Entry'] = data['OTT_Signal'] & data['Zscore_Signal']
    data['Exit'] = False
    for i in range(1, len(data) - 1):
        if data['Tillson'].iloc[i-1] > data['Tillson'].iloc[i-2] and data['Tillson'].iloc[i-1] < data['Tillson'].iloc[i]:
            data.at[data.index[i], 'Exit'] = True

    return data

st.set_page_config(
    page_title="Hisse Sinyalleri",
    layout="wide",
    initial_sidebar_state="expanded",
    theme={"base": "light"}  # Set the base theme to "light"
)

with st.sidebar:
    Hisse_Ozet = Hisse_Temel_Veriler()
    st.header('Hisse Arama')
    Hisse_Adı = st.selectbox('Hisse Adı', Hisse_Ozet['Kod'])
    Lenght_1 = 6
    vf = 0.8
    prt = 2
    prc = 1.2
    data = indicator_Signals(Hisse_Adı, Lenght_1, vf, prt, prc)

Son_Durum = data.tail(1)
col1, col2, col3, col4, col5 = st.columns(5)
Close = Son_Durum['Close'].iloc[0]
OTT_Signal = 'Alınabilir' if Son_Durum['OTT_Signal'].iloc[0] else 'Bekle'
Zscore_Signal = 'Alınabilir' if Son_Durum['Zscore_Signal'].iloc[0] else 'Bekle'
Tillson_Sinyal = 'Satılabilir' if Son_Durum['Exit'].iloc[0] else 'Bekle'

col2.metric('Kapanış Fiyatı', str(Close))
col3.metric('OTT Sinyal', str(OTT_Signal))
col4.metric('Z Skor Sinyal', str(Zscore_Signal))
col5.metric('Tillson Sinyal', str(Tillson_Sinyal))

st.dataframe(data.iloc[::-1], use_container_width=True)
