import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px


def plot_serials(url, reduce='all', min_price=None, max_price=None, min_ser=None, max_ser=None):
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


    if min_price or max_price:
        min_price, max_price = parse_numbers((min_price, max_price))
        df = filter_price(df, min_price, max_price)

    if min_ser or max_ser:
        min_ser, max_ser = parse_numbers((min_ser, max_ser))
        df = filter_serial(df, min_ser, max_ser)

    if reduce == 'lowest':
        df = lowest_per_price(df)

    title = soup.title.text
    fig = px.scatter(df, x='Price', y='Serial Nr')
    return title, fig


def parse_numbers(numbers):
    res = []
    for num in numbers:
        if num and "k" in num:
            stem = num.split("k")[0]
            res.append(int(stem+"000"))
        else:
            res.append(num)
    return tuple(res)


def filter_price(df, min, maxi):
    if not min:
        min = 0
    if not maxi:
        maxi = max(df.Price)
    df = df[df.Price > float(min)]
    df = df[df.Price < float(maxi)]
    return df


def filter_serial(df, min, maxi):
    if not min:
        min = 0
    if not maxi:
        maxi = max(df['Serial Nr'])
    df = df[df['Serial Nr'] > float(min)]
    df = df[df['Serial Nr'] < float(maxi)]
    return df


def lowest_per_price(df):
    df = df.groupby(by=['Price']).min('Serial Nr')
    df['Price'] = df.index
    return df