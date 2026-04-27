from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

INPUT_PATH = "data/books/pride_and_prejudice.html"   #change to your html filename
OUTPUT_PATH = "data/books/pride_and_prejudice.md"    #output name

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

#convert to markdown
markdown_content = md(html_content, heading_style="ATX")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Converted successfully : {OUTPUT_PATH}")