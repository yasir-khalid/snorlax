from rich.console import Console
from rich.markdown import Markdown

text = """
# WhyKay import successful
"""

console = Console()
ms = Markdown(text)
console.print(ms)
