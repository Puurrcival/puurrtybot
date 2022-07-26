import requests, puurrtybot, pandas as pd
import matplotlib, matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
plt.style.use('seaborn-dark-palette')
import puurrtybot.functions as pf
from io import BytesIO
from PIL import Image


def get_asset_name(asset: str):
    return puurrtybot.ASSETS[asset]['onchain_metadata']['name']


def get_asset_image_url(asset: str):
    return puurrtybot.ASSETS[asset]['onchain_metadata']['image']


def get_asset_image(asset: str, basewidth: int = 1200, stream: bool = True):
    image_url = f"""https://infura-ipfs.io/ipfs/{get_asset_image_url(asset).split('/')[-1]}"""
    image = Image.open(BytesIO(requests.get(image_url).content))
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    if stream:
        image_stream = BytesIO()
        image.save(image_stream, "PNG")
        image_stream.seek(0)
        return image_stream
    else:
        return image


def get_asset_sale_history(asset):
    try:
        sales = puurrtybot.ASSETS_SALES_HISTORY[asset]['amounts'][::-1]
        timestamps = puurrtybot.ASSETS_SALES_HISTORY[asset]['timestamps'][::-1]
        volume = sum(sales)
        highest = max(sales)
        lowest = min(sales)
        traded = len(sales)
        last = sales[0]
        last_time = timestamps[0]
        if len(sales)>1:
            bought = sales[1]
            bought_time = timestamps[1]
        else:
            bought = bought_time = None
    except (KeyError, IndexError):
        traded = volume = highest = lowest = 0
        last = bought = last_time = bought_time = None

    return {'traded':traded, 'volume':volume, 'last':last,'highest':highest, 'lowest':lowest, 'bought':bought, 'last_time':last_time, 'bought_time':bought_time}


def get_asset_sale_history_plot(asset):
    data = puurrtybot.ASSETS_SALES_HISTORY[asset]
    df = pd.DataFrame([pf.get_formatted_date(timestamp).split(' at')[0] for timestamp in data['timestamps']], columns=['time'])
    df['sell'] = data['amounts']
    df = df.set_index('time')
    ax = df.plot(style='.-' , yticks=[i*100 for i in range(max(int(df['sell'].min()/100)-2,0),int(df['sell'].max()/100)+2)],alpha=0.75, rot=0, legend=False, markersize=20,  markerfacecolor='darkblue')
    ax.set(xlabel="", ylabel="")
    for idx, row in enumerate(df.iterrows()): 
        d = row[0]
        value = row[1][0]
        ax.get_figure().patch.set_alpha(0)
        ax.annotate(value, (idx, value), xytext=(-10, -20), textcoords='offset points',color='darkblue')

    stream = BytesIO()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.get_figure().patch.set_alpha(0)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(stream, format='png')
    stream.seek(0)
    return stream
