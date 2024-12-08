import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu
from screener import FinancialDashboard
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


st.set_page_config(page_title="Equity Dashboard", layout="wide")


st.markdown("""
    <style>
        .main {background-color: #F5F7FA;}
        h1 {font-family: 'Helvetica Neue', sans-serif; font-weight: 700; color: #333333;}
        .sidebar .sidebar-content {background-color: #F5F7FA;}
        .stSelectbox {font-family: 'Helvetica Neue', sans-serif;}
        .css-1q8dd3e {color: #007BFF; font-size: 24px;}
        .css-1d391kg {font-family: 'Roboto', sans-serif;}
        .stButton > button {background-color: #007BFF; color: white; border-radius: 8px; padding: 12px 16px;}
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("EquityInsights")
    choice = option_menu(
        "", 
        ["Stock Explorer", "Sector Insights", "Market Scanner"], 
        icons=["search", "bar-chart", "upc-scan"]
    )



df = pd.read_csv('./data/csv/EQUITY_L.csv')

best = pd.read_csv("./data/csv/screnned.csv")
best_stocks = list(best[best['Green Flags'] == 7]['Ticker'])
index_tickers = {
    "Bank Nifty": [
        "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "SBIN.NS", 
        "INDUSINDBK.NS", "BANDHANBNK.NS", "IDFCFIRSTB.NS", "FEDERALBNK.NS", 
        "BANKBARODA.NS", "AUBANK.NS", "PNB.NS"
    ],
    "Nifty 50": [
        "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS", 
        "KOTAKBANK.NS", "HINDUNILVR.NS", "AXISBANK.NS", "BAJFINANCE.NS", 
        "SBIN.NS", "LT.NS", "WIPRO.NS", "BHARTIARTL.NS"
    ],
    "Nifty Auto": [
        "MARUTI.NS", "M&M.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", 
        "HEROMOTOCO.NS", "TVSMOTOR.NS", "ASHOKLEY.NS", "BALKRISIND.NS", "BHARATFORG.NS"
    ],
    "Nifty FMCG": [
        "HINDUNILVR.NS", "ITC.NS", "BRITANNIA.NS", "DABUR.NS", "MARICO.NS", 
        "NESTLEIND.NS", "GODREJCP.NS", "TATACONSUM.NS", "MCDOWELL-N.NS", "COLPAL.NS"
    ],
    "Nifty IT": [
        "INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", 
        "LTIM.NS", "MINDTREE.NS", "MPHASIS.NS", "COFORGE.NS", "PERSISTENT.NS"
    ],
    "Nifty Pharma": [
        "SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "AUROPHARMA.NS", 
        "BIOCON.NS", "LUPIN.NS", "TORNTPHARM.NS", "ALKEM.NS", "GLENMARK.NS"
    ],
    "Nifty Metal": [
        "TATASTEEL.NS", "HINDALCO.NS", "JSWSTEEL.NS", "COALINDIA.NS", "VEDL.NS", 
        "NMDC.NS", "NATIONALUM.NS", "SAIL.NS", "MOIL.NS", "APLAPOLLO.NS"
    ],
    "Nifty Realty": [
        "DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PRESTIGE.NS", "PHOENIXLTD.NS", 
        "SOBHA.NS", "BRIGADE.NS", "LODHA.NS", "IBREALEST.NS", "INDIABULLRL.NS"
    ],
    "Nifty Energy": [
        "RELIANCE.NS", "ONGC.NS", "IOC.NS", "NTPC.NS", "POWERGRID.NS", 
        "BPCL.NS", "GAIL.NS", "TATAPOWER.NS", "ADANIGREEN.NS", "TORNTPOWER.NS"
    ],
    "Best Stocks": best_stocks
}



if choice == "Stock Explorer":
    tickers = list(df["Yahoo_Equivalent_Code"].apply(lambda x: x.split("'")[1])) + ["Other"]
    ticker = st.selectbox('Select Equity', tickers, index=None)
    if ticker == "Other":
        ticker = st.text_input("Ticker Name")
    if ticker:
        dashboard = FinancialDashboard(ticker)
        dashboard.display_dashboard()

elif choice == "Sector Insights":
    summary_data = []
    
    index_choice = st.selectbox('Select Index', list(index_tickers.keys()), index=None)
    if index_choice:
        selected_tickers = index_tickers[index_choice]

        green_flag = 0
        red_flag = 0
        for ticker in selected_tickers:
            dashboard = FinancialDashboard(ticker)
            dashboard.display_dashboard()
            green_flag += dashboard.green_flag
            red_flag += dashboard.red_flag
            summary_data.append({"Ticker": ticker, "Green Flags": dashboard.green_flag, "Red Flags": dashboard.red_flag})
            
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values(by="Green Flags", ascending=False)
        summary_df.reset_index(inplace=True, drop=True)

        st.subheader(f"{index_choice} Index - Stock Performance Summary")
        st.dataframe(summary_df, use_container_width=True)
        index_dashboard = FinancialDashboard(index_choice)
        index_dashboard.green_flag = green_flag
        index_dashboard.red_flag = red_flag
        index_dashboard.plot_performance_overview()

else:
    if st.button("Start The Scan", use_container_width=True):
        st.title("Market Scanner")

        all_tickers = df["Yahoo_Equivalent_Code"].apply(lambda x: x.split("'")[1]).tolist()
        
        summary_data = []
        for ticker in all_tickers:
            dashboard = FinancialDashboard(ticker, plot=False)
            dashboard.display_dashboard() 
            summary_data.append({"Ticker": ticker, "Green Flags": dashboard.green_flag, "Red Flags": dashboard.red_flag})
        
        summary_df = pd.DataFrame(summary_data)
        
        summary_df = summary_df.sort_values(by="Green Flags", ascending=False)
        
        st.subheader("Best Stocks List")
        st.dataframe(summary_df)