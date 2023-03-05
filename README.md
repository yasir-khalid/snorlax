<p align="center"><img src="https://i.imgur.com/gPf0GQF.jpg" width=1000></p>

# WhyKay

[![PyPI][pypi_badge]][pypi_link] [![GitHub][github_badge]][github_link] [![commit-activity][pulse_badge]][pulse_link] 

The concept is to have a personal toolbar that contains all the handy functions that support efficient python software engineering workflows, connectivity to cloud, navigating file systems, parsing date/time formats and pushing notifications to different platforms.

🚩 v0.4.0 is now available with the feature to calculate the stock exposure through your ETFs and stock portfolio

---

## Installation
To run the code successfully, all the dependencies can either be installed using **pip**:

```bash
pip install whykay
```
## Cloning repository for contributions

To run the code successfully, all the dependencies can either be installed using **pip**:

```bash
pip install -r requirements.txt
```
**or** use the pre-define Makefile targets
 
```bash
make setup
``` 

## Features (Usage/Examples)

### Investments (Stock/ETF exposure calculator)
*Available for use from v0.1.0*

#### Limitations (in-scope features)
- This only works on ETFs or Stocks (Individual shares) based portfolio
- Will ignore any other investment holdings that you pass
- It takes in input in form of a JSON structure:
    ```bash
    [
        {
            "isin": "US30303M1027",
            "investment":  185.22,
            "category": "stock" # Optional field
        },
        {
            "isin": "IE00BQQP9H09",
            "investment":  298.22,
            "category": "ETF" # Optional field
        }
    ]
    
    ```
    where `isin` uniquely idenfies a holding, can get it from **Yahoo Finance**/**Trading 212** (personal choice)
- Returns the output in a JSON format 

```python
>>> from whykay.investments.stocks_analyzer import calculate_exposure
╔══════════════════════════════════════════════════════════════════════════╗
║                     Investment Analyzer Imported                         ║
╚══════════════════════════════════════════════════════════════════════════╝
>>> data = [
                {
                    "isin": "US30303M1027",
                    "investment":  185.22
                },
                {
                    "isin": "IE00BQQP9H09",
                    "investment":  298.22
                }
            ]
>>> calculate_exposure(
        holdings = data, display = True
    )
    
+----+----------+-----------------------+--------------------+
|    | symbol   |   Amount Invested ($) |   Overall Exposure |
|----+----------+-----------------------+--------------------|
|  0 | AAPL     |              229.5500 |            32.7929 |
|  1 | MSFT     |               28.1000 |             4.0143 |
|  2 | AMZN     |               20.3000 |             2.9000 |
|  3 | FB       |               11.4500 |             1.6357 |
|  4 | GOOGL    |               10.1000 |             1.4429 |
|  5 | GOOG     |                9.8500 |             1.4071 |
|  6 | BRK.B    |                7.2500 |             1.0357 |
|  7 | TSLA     |                7.2000 |             1.0286 |
|  8 | NVDA     |                6.8500 |             0.9786 |
|  9 | JPM      |                6.5000 |             0.9286 |
+----+----------+-----------------------+--------------------+
```

## Changelog

v0.4.0
- Breaks previous functionality, as output is now typically returned in a json structure
- Import reverted back to `whykay.investments.stock_analyzer` for future use cases
- Takes in new parameter: `display` which returns the tabular display of results on screen
- data is now inputted in form of API convention JSON structures for API endpoint developments

v0.3.0
- Breaks previous functionality, as output is now typically returned in a json structure
- Import changes from `whykay.investments.stock_analyzer` to `whykay.investments.holdings_analyzer`
- Takes in new parameter: `display` which returns the tabular display of results on screen

v0.2.0
- fixes to `.gitignore` file which was preventing the requirements.txt file upload
- does not break functionality changes in v0.1.0

v0.1.0
- Minor release that supports the stock exposure feature calculator
- `from whykay.investments.portfolio_analyzer import calculate_exposure` 

v0.0.x
- previous versions were experimental and don't provide much functionality
- will be discarded on `pypi.org`

## Authors

- [Yasir Khalid](www.linkedin.com/in/yasir-khalid)

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=47b778&label
[github_link]: https://github.com/yasir-khalid/whykay

[pypi_badge]: https://badgen.net/pypi/v/whykay?icon=pypi&color=47b778&labelColor=090422
[pypi_link]: https://www.pypi.org/project/whykay/

[pulse_badge]: https://img.shields.io/github/commit-activity/m/yasir-khalid/whykay?color=47b778&labelColor=090422
[pulse_link]: https://github.com/yasir-khalid/whykay/pulse