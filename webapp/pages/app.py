#---PIP PACKAGES---#
import streamlit as st
from streamlit_option_menu import option_menu
from isoweek import Week

from utils import get_holdings_metadata
#---BUILT-IN PYTHON MODULES
from pprint import pprint
from streamlit_echarts import st_echarts

import itertools
#---IMPORT PYTHON FILE IN SAME DIR---#
import db as db
import utils as utils

import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.switch_page_button import switch_page

# Checking user login; else redirecting to login page
if 'uuid' not in st.session_state:
    switch_page("hello")

# Page specific settings: title/description/icons etc 
page_title = "Portfolio Exposure Calculator"
layout = "wide"
st.set_page_config(page_title=page_title, layout=layout, initial_sidebar_state="collapsed")
st.title(f"{page_title}")

st.subheader('This webapp helps estimate your portfolio exposure towards different sectors and stocks')
st.markdown("""
    ##### Supported by data from `Yahoo Finance`
    Reach out to **Yasir Khalid** for more questions: [![Linkedin](https://badgen.net/badge/icon/Linkedin?icon=linkedin&label)](https://linkedin.com/in/yasir-khalid)"""
    )

st.info(f'Logged in as: **{st.session_state["uuid"]}**')

# generic streamlit configuration to hide brandings
hide_st_style = """<style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """
hide_sidebar_hamburger =  """
                        <style>
                            [data-testid="collapsedControl"] {
                                display: none
                            }
                        </style>
                        """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(hide_sidebar_hamburger,unsafe_allow_html=True,)

# Page level customisations (global settings)
style_metric_cards(border_left_color="#1E1E1E")

input_area, portfolio_area, industry_analysis = st.columns([5,5,5], gap = "medium")

with input_area:
    st.subheader("1. Add to portfolio")
    st.markdown("###### Enter your **Stock/ETF** information")
    with st.form("entry_form", clear_on_submit=True):
        ticker_input, securities_category_input = st.columns([3,4])
        ticker_input.text_input("**Ticker symbol:** `required`", key="ticker")
        # securities_category_input.radio(
        #         "Is this an ETF?  :green[disabled]",
        #         key="etf_check",
        #         options=["No", "Yes"],
        #         disabled=True
        #     )
        etf_provider = st.selectbox(
                "Which ETF provider does this belong? :green[feature disabled]",
                ("iShares", "Vanguard", "HSBC", "JP Morgan", "Morningstar"),
                disabled=True
            )
        st.number_input("**Investment amount ($):** `required`", key = "investment")

        
        submitted = st.form_submit_button("Add to portfolio", type = "primary")
        
    if submitted:
        if st.session_state["investment"] >= 0:
            metadata, holdings = get_holdings_metadata(st.session_state["ticker"].upper())
            if metadata is not None:
                ticker = st.session_state["ticker"]
                # etf_check = st.session_state["etf_check"]
                etf_check = True if metadata.get("quoteType") == "ETF" else False
                investment = st.session_state["investment"]

                db.add_to_portfolio(ticker.upper(), etf_check, etf_provider, investment, metadata, holdings, uuid = st.session_state['uuid'])
            else:
                st.warning('Unsupported Stock/ETF in the current v0.4.0 release')
        else:
            st.error("Investment amount cannot be less than zero.")

with portfolio_area:
    st.subheader("2. Edit/Verify portfolio assets")
    
    st.markdown("###### Click on an investment to see detailed information. Verify asset information, or remove before running analysis")

    if len(db.get_portfolio(st.session_state['uuid'])[0]) > 0:
        for holdings in db.get_portfolio(st.session_state['uuid'])[0]:
            with st.expander(f"""**{holdings.get("metadata").get("longName", f'Ticker: {holdings["ticker"]}')}**"""):
                st.write(f'Ticker symbol: {holdings["ticker"]}')
                st.write(f'Asset sector: **:blue[{utils.fetch_stock_industry(holdings["ticker"])}]**')
                st.write(f'Inferred as asset class: **:blue[{"ETF" if holdings.get("etf_check") else "Stock/Equity"}]**')
                # st.write(f'Traded in currency: **:blue[{utils.fetch_price(holdings["ticker"]).get("currency")}]**')
                st.write(f'Investment Amount: {holdings["investment"]}')
                st.button(label = "Remove investment",key = f'{holdings["key"]}t', on_click=db.delete_from_portfolio, args=(holdings["key"],))
        
        button_analysis = st.button(label = "Click here for Analysis", use_container_width = True, key = "run_analysis_button")

def calculate_industry_exposure():
    portfolio = db.get_portfolio(st.session_state['uuid'])[0]
    st.json(portfolio)

if 'run_analysis_button' in st.session_state and st.session_state.run_analysis_button is True:
    with industry_analysis:
        st.subheader("Market movers")
        st.markdown("###### highest asset's % change in a trading day, from your portfolio")
        st.info("Information is correct, as of the timestamp asscociated with the label", icon="ℹ️")

        market_data = utils.compute_market_movers()
        if len(market_data["symbol"]) >= 2:
            metric1, metric2 = st.columns([2,2])
            metric1.metric(label= market_data["market_time"][0], value=market_data["symbol"][0], delta=market_data["price_change"][0])
            metric2.metric(label= market_data["market_time"][1], value=market_data["symbol"][1], delta=market_data["price_change"][1])

    radar_plot, bar_plot = st.columns([3,4], gap = "medium")
    with radar_plot:
        sector_exposure_analysis = utils.calculate_sector_exposure()
        sector_exposure_analysis = dict(itertools.islice(sector_exposure_analysis.items(), 5))
        MAX_VALUE = list(sector_exposure_analysis.values())[0]
        _indicator, _values = [], []
        for sector, weightings in sector_exposure_analysis.items():
            _indicator.append({"name": sector, "max": MAX_VALUE})
            _values.append(weightings)

        st.subheader("Sector exposure")
        st.markdown("###### Estimates portfolio exposure towards different sectors")
        st.info("The sectors associated to assets have been determined by the listed labels from Yahoo Finance", icon="ℹ️")

        option = {
            "title": {"text": "Industry Exposure (relative %) - Top 5 sectors"},
            "color": "red",
            "radar": {
                "indicator": _indicator
            },
            "series": [
                {
                    "name": "Sector weightings",
                    "type": "radar",
                    "data": [
                        {
                            "value": _values,
                        }
                    ]
                }
            ]
        }
        st_echarts(option, height="500px")

    with bar_plot:
        st.subheader("Equity Stock exposure")
        st.markdown("###### Tells you the orientation of your portfolio towards individual equity stocks")
        st.info("This is an estimate, based on Top 10 holdings extracted from ETFs database", icon="ℹ️")
        stock_exposure = utils.calculate_stock_exposure()
        stock_exposure = dict(itertools.islice(stock_exposure.items(), 10))
        _x_axis, _y_axis = [], []
        for symbol, weightings in stock_exposure.items():
            _x_axis.append(str(symbol))
            _y_axis.append(weightings)
        options = {
            "title": {"text": "Stock Exposure (%) - Restricted to Top 10"},
            "xAxis": {
                "type": "category",
                "data": _x_axis,
            },
            "yAxis": {"type": "value"},
            "series": [{"data": _y_axis, "type": "bar", "label": {"show": True, "position": "top"}}],
        }
        st_echarts(options=options, height="500px")


    with st.expander(f"""Current limitations"""):
        st.markdown("""
        ###### Supported by data from `Yahoo Finance`, therefore as accurate as the data supplier
        - Currency conversion does not happen; and all asset investments are treated as investments in USD
        - Doesn't support any asset class beyond Equity (Stocks) and ETFs
        - ETF data provided by `Yahoo Finance` only gives information on top 10 holdings within the ETF
        - Might not support all ETF providers (not tested for all ETF providers like: JP Morgan, HSBC etc.)
        """
        )
