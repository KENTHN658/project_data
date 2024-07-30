import numpy as np
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import requests

resource = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
res = requests.get(resource)
soup = BeautifulSoup(res.text, "html.parser")

topic = soup.find(id="firstHeading").get_text()

datatable = soup.find("table", {"class": "wikitable"})
print(datatable)

df = pd.read_html(str(datatable))
df = pd.DataFrame(df[0])
df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]

print(df)
# df = pd.read_html(str(datatable))
# df = pd.DataFrame(df[0])
# df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
