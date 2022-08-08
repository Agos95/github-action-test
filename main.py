# %%
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# %%

url = "https://www.playbasket.it/veneto/league.php?lt=2&lr=VE&lp=VE&lc=PM&season=2022&lf=M&lg=3&mod={mod}"
team = re.compile("arcella", re.IGNORECASE)

# %% Calendario

dfs = pd.read_html(url.format(mod="cl"), match=team)
df = pd.concat(dfs)
df.columns = ["data", "locali", "ospiti",
              "tabellini", "pt-locali", "pt-ospiti", "extra"]
df.drop(columns=["tabellini", "extra"], inplace=True)
mask = df["locali"].apply(lambda x: "arcella" in x.lower()) |\
    df["ospiti"].apply(lambda x: "arcella" in x.lower())
df = df[mask]

df.to_csv("data/calendario.csv", index=False)

# %% Classifica

r = requests.get(url.format(mod="st"))
soup = BeautifulSoup(r.content, "html5lib")
div = soup.find(id="classifica_general")
standing = div.find("table")
df = pd.read_html(str(standing))[0]
df.to_csv("data/classifica.csv", index=False)
