import db
from yahooquery import Ticker
import pandas as pd
import streamlit as st

_supported_securities  = ["ETF", "EQUITY"]

def fetch_price_change(ticker):
    price_metadata = Ticker(ticker).price
    return price_metadata.get(ticker).get("regularMarketChange", None), price_metadata.get(ticker).get("regularMarketTime", None)

def fetch_price(ticker):
    price_metadata = Ticker(ticker).price
    return price_metadata.get(ticker)


def fetch_asset_name(symbol):
    ticker = Ticker(symbol)
    return ticker.quote_type.get(symbol).get("longName")

def fetch_stock_industry(ticker: str):
    asset_profile_metadata = Ticker(ticker).asset_profile
    return asset_profile_metadata.get(ticker).get("sector", None)
 
def fetch_etf_industry(ticker: str):
    return Ticker(ticker)\
        .fund_sector_weightings\
        .to_dict()\
        .get(ticker)

def fetch_asset_sector_exposure():
    sector_weightings = pd.DataFrame()
    portfolio = db.get_portfolio(st.session_state['uuid'])[0]
    for asset in portfolio:
        if asset["etf_check"] is False:
            stock_data_adjustments = [
                {
                    "symbol": asset["ticker"],
                    "sector": fetch_stock_industry(asset["ticker"]),
                    "weight": 1.0,
                    "weighted_investment_amount": asset["investment"]
                }
            ]
            holdings_data = pd.DataFrame.from_dict(stock_data_adjustments)

        else:
            etf_sectors = fetch_etf_industry(asset['ticker'])
            holdings_data = pd.DataFrame()
            for sector, weights in etf_sectors.items():
                stock_data_adjustments = [
                    {
                        "symbol": asset["ticker"],
                        "sector": sector,
                        "weight": weights,
                        "weighted_investment_amount": asset["investment"] * weights
                    }
                ]
                holdings_data = pd.concat([
                    holdings_data, 
                    pd.DataFrame.from_dict(stock_data_adjustments)
                    ])

        sector_weightings = pd.concat([sector_weightings, holdings_data])
    
    return sector_weightings

def transform_sector_labels(label):
    cleaned_label = label.strip().upper().replace("_", " ")
    return cleaned_label


def transform_aggregated_sector_weightings(asset_sector_exposure_raw):
    sector_names: pd.DataFrame = asset_sector_exposure_raw[["sector"]].drop_duplicates()
    sector_exposure: pd.DataFrame = pd.DataFrame(
        asset_sector_exposure_raw.groupby("sector")["weighted_investment_amount"].sum()
    )
    total_portfolio_invstments = db.get_portfolio_total(st.session_state['uuid'])
    sector_exposure[
        "net_exposure"
    ]: pd.DataFrame = sector_exposure["weighted_investment_amount"] * 100 / total_portfolio_invstments

    sector_exposure = sector_exposure.sort_values(by=['net_exposure'], ascending=False)
    return sector_exposure["net_exposure"].to_dict()

def calculate_sector_exposure():
    asset_sector_exposure_raw = fetch_asset_sector_exposure()
    asset_sector_exposure_raw["sector"] = asset_sector_exposure_raw['sector'].apply(transform_sector_labels)
    x = transform_aggregated_sector_weightings(asset_sector_exposure_raw)
    return x

def compute_market_movers():
    portfolio = db.get_portfolio(st.session_state['uuid'])[0]
    price_data = pd.DataFrame()
    for asset in portfolio:
        price_change, market_time = fetch_price_change(asset['ticker'])
        price_point = [
            {
                "symbol": asset["ticker"],
                "price_change": price_change,
                "market_time": market_time
            }
        ]
        price_data = pd.concat([
            price_data, 
            pd.DataFrame.from_dict(price_point)
            ])
        
    
    price_data["absolute_change"] = price_data["price_change"].apply(lambda x: abs(x))
    return price_data.sort_values(by=["absolute_change"], ascending=False).to_dict("list")


def fetch_assets_holdings() -> pd.DataFrame:
    """takes the input raw data, validates against pydantic model and returns a pandas dataframe with enriched values"""
    # create a dataframe to store the holdings and weights of all ETFs
    portfolio = db.get_portfolio(st.session_state['uuid'])[0]
    weighted_holdings = pd.DataFrame()

    # iterate through each ETF and its investment
    for asset in portfolio:
        # get the holdings data for the current ETF
        if asset["etf_check"] is True:
            holdings_data = pd.DataFrame.from_records(
                asset["holdings"]
            )

            # add the holdings and weights to the combined dataframe, using the investment amount as a weight
            holdings_data["weighted_investment_amount"] = (
                holdings_data["holdingPercent"] * asset["investment"]
            )
        else: # Stock/Equity as the UI filters out other asset classes
            stock_data_adjustments = [
                {
                    "symbol": asset["ticker"],
                    "holdingPercent": 1.0,  # whole investment gets allotted to the individual share
                    "weighted_investment_amount": asset["investment"]
                }
            ]
            holdings_data = pd.DataFrame.from_dict(stock_data_adjustments)

        weighted_holdings = pd.concat([weighted_holdings, holdings_data])

    return weighted_holdings

def calculate_stock_exposure():
    """Takes the weighted asset class investments; and aggregated them for a final exposure result"""
    assets_weights = fetch_assets_holdings()
    stock_exposure: pd.DataFrame = pd.DataFrame(
        assets_weights.groupby("symbol")["weighted_investment_amount"].sum()
    )
    total_portfolio_invstments = db.get_portfolio_total(st.session_state['uuid'])
    stock_exposure[
        "net_exposure"
    ]: pd.DataFrame = stock_exposure["weighted_investment_amount"] * 100 / total_portfolio_invstments

    stock_exposure = stock_exposure.sort_values(by=['net_exposure'], ascending=False)
    stock_exposure["net_exposure"] = stock_exposure["net_exposure"].apply(lambda x: round(x, 2))
    return stock_exposure["net_exposure"].to_dict()

def get_holdings_metadata(symbol: str):
    try:
        ticker = Ticker(symbol)
        _ticker_quote_type = ticker.quote_type.get(symbol)
        if _ticker_quote_type.get("quoteType") in _supported_securities:
            if _ticker_quote_type.get("quoteType") == "ETF":
                _holding_information = ticker.fund_holding_info.get(symbol).get("holdings")
                return _ticker_quote_type, _holding_information
            return _ticker_quote_type, None
        else:
            return None, None
    except:
        return None, None