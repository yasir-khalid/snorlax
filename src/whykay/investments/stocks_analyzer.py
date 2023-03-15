"""Analayzes Stock/ETF invesments for their holdings exposure using data parsed from Yahoo finance on holding"""

import json
from typing import Dict, List

import pandas as pd
from tabulate import tabulate
from yahooquery import Ticker

from whykay.helpers.logs import init_logger
from whykay.investments.models.data_models import Portfolio, WeightedInvestments
from whykay.investments.models.validation import input_validator

logging = init_logger(name=__name__)


def parse_holdings_input(list_of_holdings: List[Portfolio]) -> pd.DataFrame:
    """takes the input raw data, validates against pydantic model and returns a pandas dataframe with enriched values"""
    # create a dataframe to store the holdings and weights of all ETFs
    weighted_holdings = pd.DataFrame()

    # iterate through each ETF and its investment
    for holding in list_of_holdings:
        # get the holdings data for the current ETF
        try:
            ticker = Ticker(holding.ticker)
            ticker_data = ticker.quote_type.get(holding.ticker)
            if not isinstance(ticker_data, str):
                logging.info(
                    f"Ticker metadata: {ticker} for {holding.ticker} found on YahooQuery"
                )
            else:
                logging.info(
                    f"Ticker: {holding.ticker} metadata not found. Skipping holding"
                )
                continue

        except:
            logging.error(
                f"Cannot extract detailed information from YahooQuery for {holding.ticker}"
            )
            continue

        legalType = ticker_data.get("quoteType", "undefined")

        if legalType == "ETF":
            logging.info(
                f"{holding.ticker} is symbol for ETF: {ticker_data.get('longName', '<Name not specified on Yahoo finance>')}"
            )
            holdings_data = pd.DataFrame.from_records(
                ticker.fund_holding_info.get(holding.ticker).get("holdings")
            )

            # add the holdings and weights to the combined dataframe, using the investment amount as a weight
            holdings_data["investment_allocation"] = (
                holdings_data["holdingPercent"] * holding.investment
            )
        elif legalType == "EQUITY":
            logging.info(
                f"{holding.ticker} correponds to an individual equity share. Incorporting into analysis"
            )
            logging.info(
                f"{holding.ticker} is symbol for stock: {ticker_data.get('longName', '<Name not specified on Yahoo finance>')}"
            )
            stock_data_adjustments = [
                {
                    "symbol": holding.ticker,
                    "holdingName": ticker_data["longName"],
                    "holdingPercent": 1.0,  # whole investment gets allotted to the individual share
                    "investment_allocation": holding.investment,
                }
            ]
            holdings_data = pd.DataFrame.from_dict(stock_data_adjustments)
        else:
            logging.warning(
                f"Unsupported ISIN {holding.isin}, potentially belong to bond market/REITs etc"
            )
            continue

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


def calculate_exposure(holdings, display = False):
    """calculates stock/ETF exposure against individual holdings data from Yahoo Finance"""
    validated_data: Portfolio = input_validator(data=holdings)
    weighted_holdings: pd.DataFrame = parse_holdings_input(
        list_of_holdings=validated_data
    )

    ticker_names: pd.DataFrame = weighted_holdings[["symbol"]].drop_duplicates()
    stock_exposure: pd.DataFrame = pd.DataFrame(
        weighted_holdings.groupby("symbol").sum()["investment_allocation"]
    )

    total_portfolio_invstments = sum([float(x.investment) for x in validated_data])
    stock_exposure[
        "Overall Exposure"
    ]: pd.DataFrame = stock_exposure * 100 / total_portfolio_invstments
    results: pd.DataFrame = stock_exposure.merge(
        ticker_names, on="symbol", how="left"
    ).fillna(0)

    final_output: pd.DataFrame = results.rename(
        columns={
            "name": "first_name",
            "investment_allocation": "Amount Invested ($)",
            "holdingName": "Holding Name",
        }
    )

    analysis: pd.DataFrame = retouching_outputs_for_display(final_output)
    if display:
        print(tabulate(analysis, headers="keys", tablefmt="psql", floatfmt=".4f"))
    else: 
        return


def standardize_zeroes(val, length=3):
    val_str = str(val)
    return val_str.zfill(length)


# Define a function to format a number with a fixed number of zeroes and decimal places
def format_number(num):
    return "{:,.3f}".format(num)


if __name__ == "__main__":
    logging.warning("Running the model validator on sample data, not real data")
    logging.warning("To run on real data; import the module from WhyKay libaray")
    try:
        logging.info(
            "Reading sample dataset from: datasets/stock_portfolio_modelling.json ..."
        )
        with open("datasets/stock_portfolio_modelling.json") as holdings_dummy_data:
            sample_holdings_data = json.loads(holdings_dummy_data.read())
        logging.info("Sample dataset read successful")
    except:
        logging.error("Sample data read unsuccessful. Check path")

    calculate_exposure(holdings=sample_holdings_data)
