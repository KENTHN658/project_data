import numpy as np
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import requests

resource = "https://www.worlddata.info/america/brazil/inflation-rates.php"
res = requests.get(resource)
soup = BeautifulSoup(res.text, "html.parser")
# print(soup)
# topic = soup.find(id="firstHeading").get_text()

datatable = soup.find("table", {"class": "std100 hover sticky"})
print(datatable)

df = pd.read_html(str(datatable))
df = pd.DataFrame(df[0])
df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]

print(df)
# df = pd.read_html(str(datatable))
# df = pd.DataFrame(df[0])
# df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
