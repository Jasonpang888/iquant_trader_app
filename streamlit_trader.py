
import streamlit as st
import time
import requests
from ib_insync import *
import plotly.graph_objects as go

# 初始化 API
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Telegram 设置
BOT_TOKEN = '7715862737:AAFcTb78ZI_UzoTXXbBufodg1501TlqhPgk'
CHAT_ID = '6128137477'

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': msg}
    requests.post(url, data=data)

# UI 布局
st.set_page_config(page_title="iQuant 控制面板", layout="wide")
st.title("📈 iQuant A.I. 自动交易系统")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ 策略控制")
    start = st.button("开始交易")
    stop = st.button("停止交易")
    pnl_display = st.empty()

with col2:
    st.subheader("📊 实时图表")

    # 模拟价格数据
    bars = ib.reqHistoricalData(
        Stock('TSLA', 'SMART', 'USD'),
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='5 mins',
        whatToShow='TRADES',
        useRTH=True
    )
    df = util.df(bars)

    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(title='TSLA 实时价格走势图', xaxis_title='时间', yaxis_title='价格')
    st.plotly_chart(fig, use_container_width=True)

# 模拟策略逻辑（用户自行替换）
if start:
    send_alert("🟢 策略已启动")
    pnl = 0
    for i in range(10):
        pnl += 1.5  # 模拟盈利
        pnl_display.metric(label="当前累计收益", value=f"${pnl:.2f}")
        time.sleep(1)
    send_alert(f"✅ 策略结束，总收益：${pnl:.2f}")

if stop:
    send_alert("⛔ 策略已手动停止")