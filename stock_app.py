import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import pandas as pd

# Web App Title
st.title("Stock Chart Analysis with Resistance Lines")

# Input Section
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):")

if st.button("Generate Chart"):
    if ticker:
        try:
            # Fetch stock data
            stock_data = yf.download(ticker, period='7d', interval='1h')
            stock_data.reset_index(inplace=True)
            stock_data['Date'] = stock_data['Datetime'].map(mdates.date2num)

            # Prepare candlestick chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ohlc = stock_data[['Date', 'Open', 'High', 'Low', 'Close']].values
            candlestick_ohlc(ax, ohlc, width=0.6, colorup='green', colordown='red')

            # Calculate resistance line using linear regression
            highs = stock_data[['Date', 'High']].dropna()
            X = highs['Date'].values.reshape(-1, 1)
            y = highs['High'].values
            model = LinearRegression().fit(X, y)
            predicted_resistance = model.predict(X)
            ax.plot(stock_data['Date'], predicted_resistance, color='blue', label='Resistance Line')

            # Chart formatting
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.set_title(f"{ticker} Stock Chart with Resistance Line")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()
            plt.grid()

            # Display chart in Streamlit
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid stock ticker.")
