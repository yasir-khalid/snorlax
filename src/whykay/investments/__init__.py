from rich.console import Console
from rich.markdown import Markdown

text = """
Launching *Portfolio Analyzer*
1. This only works on ETFs or Stocks (Individual shares) based portfolio
2. Will ignore any other investment holdings that you pass
3. It takes in input in form of a {ISIN: AMOUNT INVESTED, ...} where ISIN uniquely idenfies a holding
"""

console = Console()
ms = Markdown(text)
console.print(ms)