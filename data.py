import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px


def plot_serials(url):
    if not url:
        url = "https://www.nbatopshot.com/listings/p2p/12a8288a-addc-4e5c-8af7-b3ba6e5161d4+9c0cd57c-8203-4ec1-9a0c-9b7e7a6f0635"

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    next_data = soup.find("script", id="__NEXT_DATA__")
    j = json.loads(next_data.contents[0])
    moment = j['props']['pageProps']['moment']
    listings = [l['moment'] for l in moment['momentListings']]

    df = pd.DataFrame(listings)
    df['Serial Nr'] = df.flowSerialNumber.astype(int)
    df['Price'] = df.price.astype(float)

    title = soup.title.text
    fig = px.scatter(df, x='Price', y='Serial Nr')
    return title, fig