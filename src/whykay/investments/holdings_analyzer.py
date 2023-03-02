import investpy
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from yahoo_fin import stock_info as si

from whykay.helpers.logs import init_logger
from whykay.investments.models.data_models import Investment

logging = init_logger(name=__name__)


def validate_investment(data: Dict) -> Investment:
    """compares the input data against the defined pydantic model for input"""
    return Investment(investments=data)


def parse_holdings_input(holdings) -> pd.DataFrame:
    """takes the input raw data, validates against pydantic model and returns a pandas dataframe with enriched values"""
    # create a dataframe to store the holdings and weights of all ETFs
    combined_df = pd.DataFrame()

    # TODO: PERFORM VALIDATION AGAINST PYDANTIC AND TEST THIS

    # iterate through each ETF and its investment
    for isin, investment in holdings.items():
        # get the holdings data for the current ETF
        ticker = yf.Ticker(isin)
        try:
            legalType = ticker.info.get("legalType", "undefined")

            if legalType == "Exchange Traded Fund":
                logging.info(f"{isin} is ISIN for ETF: {ticker.info['longName']}")
                holdings_data = pd.DataFrame.from_records(ticker.info["holdings"])

                # add the holdings and weights to the combined dataframe, using the investment amount as a weight
                holdings_data["investment_allocation"] = (
                    holdings_data["holdingPercent"] * investment
                )
            else:
                logging.warning(
                    f"{isin} is not an ETF, belongs to other legal types. Name: {ticker.info['longName']}"
                )
                if "holdings" in ticker.info.keys():
                    logging.warning(
                        f"Unsupported ISIN {isin}, potentially belong to bond market/REITs etc"
                    )
                    pass
                else:
                    logging.info(
                        f"ISIN {isin} correponds to an individual equity share. Incorporting into analysis"
                    )
                    stock_data_adjustments = [
                        {
                            "symbol": investpy.stocks.search_stocks(
                                by="isin", value=isin
                            ).iloc[0, 5],
                            "holdingName": ticker.info["longName"],
                            "holdingPercent": 1.0,  # whole investment gets allotted to the individual share
                            "investment_allocation": investment,
                        }
                    ]
                    holdings_data = pd.DataFrame.from_dict(stock_data_adjustments)

            combined_df = pd.concat([combined_df, holdings_data])
        except:
            logging.error(
                f"{isin} seems incorrect, please try again and reference Yahoo Finance for accurate ISIN"
            )

    return combined_df


def calculate_exposure(holdings):
    combined_df = parse_holdings_input(holdings=holdings)
    ticker_name = combined_df[["symbol"]].drop_duplicates()
    stock_exposure = pd.DataFrame(
        combined_df.groupby("symbol").sum()["investment_allocation"]
    )
    stock_exposure["Overall Exposure"] = stock_exposure * 100 / sum(holdings.values())
    final_output = stock_exposure.merge(ticker_name, on="symbol", how="left").fillna(0)

    final_output = final_output.rename(
        columns={
            "name": "first_name",
            "investment_allocation": "Amount Invested ($)",
            "holdingName": "Holding Name",
        }
    )

    analysis = final_output.sort_values(
        by="Overall Exposure", ascending=False
    ).reset_index(drop=True)
    analysis["Amount Invested ($)"] = analysis["Amount Invested ($)"].apply(
        standardize_zeroes
    )
    analysis["Overall Exposure"] = analysis["Overall Exposure"].apply(
        standardize_zeroes
    )

    print(tabulate(analysis, headers="keys", tablefmt="psql", floatfmt=".4f"))


def standardize_zeroes(val, length=3):
    val_str = str(val)
    return val_str.zfill(length)


# Define a function to format a number with a fixed number of zeroes and decimal places
def format_number(num):
    return "{:,.3f}".format(num)


if __name__ == "__main__":
    logging.info(f"Module {__name__} cannot be run directly")
