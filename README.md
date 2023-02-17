<p align="center"><img src="https://i.imgur.com/UjLoOG3.jpg" width=1000></p>

<p align="center">
    <a href="https://pypi.python.org/pypi/whykay/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/whykay?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/prefecthq/prefect/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/yasir-khalid/whykay?color=0052FF&labelColor=090422" /></a>
</p>

# WhyKay

The concept is to have a personal toolbar that contains all the handy functions that support efficient python software engineering workflows, connectivity to cloud, navigating file systems, parsing date/time formats and pushing notifications to different platforms.

`v0.1.0 is now available with the feature to calculate the stock exposure through your ETFs and stock portfolio`

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

### Investments (Stock exposure calculator)
*Available for use from v0.1.0*

```python
>>> from whykay.investments.portfolio_analyzer import calculate_exposure
╔═════=══════════════════════════════════════════════════════════════════════════════════╗
║                           WhyKay import successful                                     ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
Launching Portfolio Analyzer

 1 This only works on ETFs or Stocks (Individual shares) based portfolio
 2 Will ignore any other investment holdings that you pass
 3 It takes in input in form of a {ISIN: AMOUNT INVESTED, ...} where ISIN uniquely idenfies a holding

>>> calculate_exposure({"IE00B3XXRP09": 500, "US0378331005": 200})
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
