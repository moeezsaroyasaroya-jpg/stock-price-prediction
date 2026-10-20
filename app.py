import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# Streamlit Page Config
st.set_page_config(page_title="Stock Price Prediction", layout="wide")

st.title("📈 Stock Price Prediction App")
st.write("Simple Stock Price Prediction & Historical Analysis Tool")

# Sidebar Controls
st.sidebar.header("User Input Parameters")
ticker = st.sidebar.selectbox("Select Stock Ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"])
forecast_days = st.sidebar.slider("Forecast Days", min_value=7, max_value=90, value=30)
model_type = st.sidebar.radio("Select Model", ["Moving Average (Simple)", "Linear Trend Model"])

# Generate Historical Data
np.random.seed(42)
dates = pd.date_range(end=datetime.date.today(), periods=365)
base_price = 150.0 if ticker == "AAPL" else 180.0
returns = np.random.normal(0.0005, 0.015, size=len(dates))
prices = base_price * np.exp(np.cumsum(returns))

df = pd.DataFrame({"Date": dates, "Close": prices})

# Display Metric Cards
st.subheader(f"Data & Forecast for {ticker}")
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
col2.metric("Mean Price (365D)", f"${df['Close'].mean():.2f}")

# Simple Forecast Logic
last_price = df['Close'].iloc[-1]
future_dates = pd.date_range(start=dates[-1] + datetime.timedelta(days=1), periods=forecast_days)

if model_type == "Moving Average (Simple)":
    trend = df['Close'].pct_change().tail(30).mean()
    future_prices = [last_price * ((1 + trend) ** i) for i in range(1, forecast_days + 1)]
else:
    x = np.arange(len(df))
    y = df['Close'].values
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(df), len(df) + forecast_days)
    future_prices = slope * future_x + intercept

forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Close": future_prices})
predicted_target = future_prices[-1]
change = ((predicted_target - last_price) / last_price) * 100

col3.metric("Predicted Target", f"${predicted_target:.2f}", f"{change:+.2f}%")

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Historical Price', line=dict(color='#0066cc')))
fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Predicted_Close'], mode='lines', name='Forecast Price', line=dict(color='#ff4b4b', dash='dash')))

fig.update_layout(title=f"{ticker} Price History & Prediction", xaxis_title="Date", yaxis_title="Price ($)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Forecast Data")
st.dataframe(forecast_df.style.format({"Predicted_Close": "${:.2f}"}))
