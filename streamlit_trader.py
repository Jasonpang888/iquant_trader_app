# streamlit_trader.py
import streamlit as st
from ib_insync import *
import requests, time, threading
import plotly.graph_objects as go

# --- 初始化 IB API ---
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# --- Telegram 设置 ---
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': msg}
    requests.post(url, data=data)

# --- 获取 TSLA 实时数据 ---
contract = Stock('TSLA', 'SMART', 'USD')
ib.qualifyContracts(contract)

bars = []

def fetch_data():
    global bars
    while True:
        bar = ib.reqMktData(contract, '', False, False)
        time.sleep(1)
        ticker = ib.ticker(contract)
        if ticker.last:
            bars.append({
                'time': time.strftime('%H:%M:%S'),
                'open': float(ticker.open or 0),
                'high': float(ticker.high or 0),
                'low': float(ticker.low or 0),
                'close': float(ticker.last)
            })
            if len(bars) > 50:
                bars = bars[-50:]
        ib.sleep(1)

threading.Thread(target=fetch_data, daemon=True).start()

# --- 前端 UI ---
st.set_page_config(page_title="iQuant TSLA Trader", layout="wide")
st.title("📈 iQuant - TSLA 实时图表")

col1, col2 = st.columns([1, 2])
col1.success("系统已启动。监听 TSLA 实时价格...")

fig = go.Figure(data=go.Candlestick(
    x=[b['time'] for b in bars],
    open=[b['open'] for b in bars],
    high=[b['high'] for b in bars],
    low=[b['low'] for b in bars],
    close=[b['close'] for b in bars]
))
fig.update_layout(title='TSLA 实时价格趋势', xaxis_title='时间', yaxis_title='价格')
col2.plotly_chart(fig, use_container_width=True)
