"""Analayzes Stock/ETF invesments for their holdings exposure using data parsed from Yahoo finance on holding"""

import investpy
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from yahoo_fin import stock_info as si

from whykay.helpers.logs import init_logger
from whykay.investments.models.data_models import Portfolio
from whykay.investments.models.validation import input_validator
import json
from typing import Dict, List

logging = init_logger(name=__name__)

def parse_holdings_input(list_of_holdings: List[Portfolio]) -> pd.DataFrame:
    """takes the input raw data, validates against pydantic model and returns a pandas dataframe with enriched values"""
    # create a dataframe to store the holdings and weights of all ETFs
    weighted_holdings = pd.DataFrame()

    # iterate through each ETF and its investment
    for holding in list_of_holdings:
        # get the holdings data for the current ETF
        try:
            ticker = yf.Ticker(holding.isin)
            logging.info(f"{ticker} for {holding.isin} found on Yahoo Finance")
            ticker_data = ticker.info
            logging.info(f"{holding.isin} information successfully extracted from Yahoo Finance")
        except:
            logging.error(f"Cannot extract data from Yahoo Finance for {holding.isin}")
            continue

        legalType = ticker_data.get("legalType", "undefined")

        if legalType == "Exchange Traded Fund":
            logging.info(f"{holding.isin} is ISIN for ETF: {ticker_data['longName']}")
            holdings_data = pd.DataFrame.from_records(ticker_data["holdings"])

            # add the holdings and weights to the combined dataframe, using the investment amount as a weight
            holdings_data["investment_allocation"] = (
                holdings_data["holdingPercent"] * holding.investment
            )
        else:
            logging.warning(
                f"{holding.isin} is not an ETF, belongs to other legal types. Name: {ticker_data['longName']}"
            )
            if "holdings" in ticker_data.keys():
                logging.warning(
                    f"Unsupported ISIN {holding.isin}, potentially belong to bond market/REITs etc"
                )
                pass
            else:
                logging.info(
                    f"ISIN {holding.isin} correponds to an individual equity share. Incorporting into analysis"
                )
                stock_data_adjustments = [
                    {
                        "symbol": investpy.stocks.search_stocks(
                            by="isin", value = holding.isin
                        ).iloc[0, 5],
                        "holdingName": ticker_data["longName"],
                        "holdingPercent": 1.0,  # whole investment gets allotted to the individual share
                        "investment_allocation": holding.investment,
                    }
                ]
                holdings_data = pd.DataFrame.from_dict(stock_data_adjustments)

        weighted_holdings = pd.concat([weighted_holdings, holdings_data])

    return weighted_holdings

def retouching_outputs_for_display(final_output: pd.DataFrame) -> pd.DataFrame:
    analysis: pd.DataFrame = final_output.sort_values(
        by="Overall Exposure", ascending=False
    ).reset_index(drop=True)
    analysis["Amount Invested ($)"] = analysis["Amount Invested ($)"].apply(
        standardize_zeroes
    )
    analysis["Overall Exposure"] = analysis["Overall Exposure"].apply(
        standardize_zeroes
    )

    return analysis

def calculate_exposure(holdings):
    """calculates stock/ETF exposure against individual holdings data from Yahoo Finance"""
    validated_data: Portfolio = input_validator(data = holdings)
    weighted_holdings: pd.DataFrame = parse_holdings_input(list_of_holdings= validated_data)

    ticker_names: pd.DataFrame = weighted_holdings[["symbol"]].drop_duplicates()
    stock_exposure: pd.DataFrame = pd.DataFrame(
        weighted_holdings.groupby("symbol").sum()["investment_allocation"]
    )
    stock_exposure["Overall Exposure"]: pd.DataFrame = stock_exposure * 100 / sum(holdings.values())
    results: pd.DataFrame = stock_exposure.merge(ticker_names, on="symbol", how="left").fillna(0)

    final_output: pd.DataFrame = results.rename(
        columns={
            "name": "first_name",
            "investment_allocation": "Amount Invested ($)",
            "holdingName": "Holding Name",
        }
    )

    analysis: pd.DataFrame = retouching_outputs_for_display(final_output)
    print(tabulate(analysis, headers="keys", tablefmt="psql", floatfmt=".4f"))


def standardize_zeroes(val, length=3):
    val_str = str(val)
    return val_str.zfill(length)


# Define a function to format a number with a fixed number of zeroes and decimal places
def format_number(num):
    return "{:,.3f}".format(num)


if __name__ == "__main__":
    logging.warn("Running the model validator on sample data, not real data")
    logging.warn("To run on real data; import the module from WhyKay libaray")
    try:
        logging.info("Reading sample dataset from: datasets/stock_portfolio_modelling.json ...")
        with open('datasets/stock_portfolio_modelling.json') as holdings_dummy_data:
            sample_holdings_data = json.loads(
                            holdings_dummy_data.read()
                        )
        logging.info("Sample dataset read successful")
    except:
        logging.error("Sample data read unsuccessful. Check path")

    calculate_exposure(holdings = sample_holdings_data)