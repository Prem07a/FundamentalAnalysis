import yfinance as yf
import streamlit as st
import plotly.express as px
import numpy as np

class FinancialDashboard:
    def __init__(self, ticker, plot=True):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        try:
            self.financials = self.stock.financials
            self.balance_sheet = self.stock.balance_sheet
            self.cashflow = self.stock.cashflow
        except:
            pass
        self.green_flag = 0
        self.red_flag = 0
        self.plot = plot 
    
    def plot_revenue_growth(self):
        revenue_growth = self.financials.loc['Total Revenue']
        revenue_growth.dropna(inplace=True)
        revenue_cagr = (revenue_growth.pct_change(periods=-1) * 100).mean()
        
        if self.plot:
            fig_revenue = px.bar(x=revenue_growth.index, y=revenue_growth,
                                title=f"{self.ticker} Revenue Growth",
                                labels={'x': 'Date', 'y': 'Revenue'},
                                color_discrete_sequence=["#4CAF50"],
                                template="plotly_dark")
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        if revenue_cagr < 15:
            st.error(f'Revenue CAGR: {round(revenue_cagr, 2)}%')
            self.red_flag += 1
        else:
            st.success(f'Revenue CAGR: {round(revenue_cagr, 2)}%')
            self.green_flag += 1
    
    def plot_income_growth(self):
        income_growth = self.financials.loc['Net Income']
        income_growth.dropna(inplace=True)
        income_cagr = (income_growth.pct_change(periods=-1) * 100).mean()

        if self.plot:
            fig_income = px.bar(x=income_growth.index, y=income_growth,
                                title=f"{self.ticker} Net Income Growth",
                                labels={'x': 'Date', 'y': 'Net Income'},
                                color_discrete_sequence=["#FF9800"],
                                template="plotly_dark")
            st.plotly_chart(fig_income, use_container_width=True)
        
        if income_cagr < 15:
            st.error(f'PAT CAGR: {round(income_cagr, 2)}%')
            self.red_flag += 1
        else:
            st.success(f'PAT CAGR: {round(income_cagr, 2)}%')
            self.green_flag += 1
    
    def plot_eps(self):
        net_income = self.financials.loc['Net Income']
        eps = self.financials.loc['Diluted EPS']
        eps.dropna(inplace=True)
        
        if self.plot:
            fig_eps = px.line(x=eps.index, y=eps, title=f"{self.ticker} EPS Over Time",
                            labels={'x': 'Date', 'y': 'EPS'},
                            color_discrete_sequence=["#42A5F5"],
                            template="plotly_dark")
            st.plotly_chart(fig_eps, use_container_width=True)
        
        if (eps / net_income).mean() <= 1:
            st.success("EPS Is Consistent")
            self.green_flag += 1
        else:
            st.error("EPS Is Not Consistent")
            self.red_flag += 1

    def plot_debt_to_ebit(self):
        try:
            ebit = self.financials.loc['EBIT']
            debt_to_ebit = self.balance_sheet.loc['Total Debt'] / ebit
        except:
            debt_to_ebit = self.balance_sheet.loc['Total Debt'] 
        
        
        debt_to_ebit.dropna(inplace=True)
        debt_to_ebit.sort_index(inplace=True)
        if self.plot:
            fig_debt_ebit = px.bar(x=debt_to_ebit.index, y=debt_to_ebit,
                                title=f"Debt/EBIT Over Time",
                                labels={'x': 'Date', 'y': 'Debt/EBIT'},
                                color_discrete_sequence=["#FF5252"],
                                template="plotly_dark")
            st.plotly_chart(fig_debt_ebit, use_container_width=True)
        
        debt_changes = np.diff(debt_to_ebit)
        up = np.sum(debt_changes > 0)
        down = np.sum(debt_changes < 0)
        
        if down > up or debt_to_ebit[0] > debt_to_ebit[-1]:
            st.success("Debt is Decreasing")
            self.green_flag += 1
        else:
            st.error("Debt is Increasing")
            self.red_flag += 1
    
    def plot_cash_flow(self):
        cash_flow_operations = self.cashflow.loc['Operating Cash Flow']
        cash_flow_operations.dropna(inplace=True)
        
        if self.plot and not cash_flow_operations.empty:
            fig_cash_flow = px.bar(x=cash_flow_operations.index, y=cash_flow_operations,
                                title="Operating Cash Flow",
                                color_discrete_sequence=["#00C853"],
                                labels={'x': 'Date', 'y': 'Operating Cash Flow'},
                                template="plotly_dark")
            st.plotly_chart(fig_cash_flow, use_container_width=True)
        
        cash_flow_positive = all(cash_flow_operations > 0)
        if cash_flow_positive:
            st.success("Cash Flow from Operations is consistently positive.")
            self.green_flag += 1
        else:
            st.error("Cash Flow from Operations is not consistently positive.")
            self.red_flag += 1
    
    def plot_roe(self):
        net_income = self.financials.loc['Net Income']
        shareholders_equity = self.balance_sheet.loc['Stockholders Equity']
        roe = (net_income / shareholders_equity) * 100
        roe.dropna(inplace=True)
        roe.sort_index(inplace=True)
        if self.plot:
            fig_roe = px.line(x=roe.index, y=roe, title=f"ROE Over Time",
                            labels={'x': 'Date', 'y': 'Return on Equity (%)'},
                            color_discrete_sequence=["#AB47BC"],
                            template="plotly_dark")
            st.plotly_chart(fig_roe, use_container_width=True)
        
        roe_value = roe[-1]
        if roe_value > 20:
            st.success(f"ROE of {round(roe_value, 2)}% is excellent!")
            self.green_flag += 1
        else:
            st.error(f"ROE of {round(roe_value, 2)}% is below the threshold of 20%")
            self.red_flag += 1

    def plot_gpm(self):
        gpm = (self.financials.loc['Gross Profit'] / self.financials.loc['Total Revenue']) * 100
        gpm.dropna(inplace=True)
        gpm.sort_index(inplace=True)
        if self.plot:
            fig_gpm = px.line(x=gpm.index, y=gpm, title=f"{self.ticker} Gross Profit Margin Over Time",
                            labels={'x': 'Date', 'y': 'Gross Profit Margin (%)'},
                            color_discrete_sequence=["#66BB6A"],
                            template="plotly_dark")
            st.plotly_chart(fig_gpm, use_container_width=True)
        
        if gpm[-1] > 20:
            st.success(f"GPM ({round(gpm[-1], 2)}%) is above the threshold!")
            self.green_flag += 1
        else:
            st.error(f"GPM ({round(gpm[-1], 2)}%) is below the threshold of 20%.")
            self.red_flag += 1
    
    def plot_performance_overview(self):
        st.markdown("### Overall Performance")
        
        if self.plot:
            fig_pie = px.pie(values=[self.green_flag, self.red_flag],
                            names=['Green Flags', 'Red Flags'],
                            title='Performance Overview',
                            color_discrete_sequence=['#00C853', '#FF5252'],
                            template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True, key = self.ticker)

    def display_dashboard(self):
        st.markdown(f"<h1 style='text-align: center; color: #007BFF;'>{self.ticker.split('.')[0]} Financial Dashboard</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            try:
                self.plot_revenue_growth()
            except:
                st.warning("Data Not Available")

        with col2:
            try:
                self.plot_income_growth()
            except:
                st.warning("Data Not Available")

        col3, col4 = st.columns(2)
        with col3:
            try:
                self.plot_eps()
            except:
                st.warning("Data Not Available")

        with col4:
            try:
                self.plot_debt_to_ebit()
            except:
                st.warning("Data Not Available")

        col5, col6 = st.columns(2)
        with col5:
            try: 
                self.plot_cash_flow()
            except:
                st.warning("Data Not Available")

        with col6:
            try: 
                self.plot_roe()
            except:
                st.warning("Data Not Available")

        try:
            self.plot_gpm()
        except:
            st.warning("Data Not Available")
        if self.plot:
            self.plot_performance_overview()

