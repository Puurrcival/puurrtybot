import requests, pandas as pd
import matplotlib, matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
plt.style.use('seaborn-dark-palette')
import puurrtybot.helper.functions as pf
from io import BytesIO
from PIL import Image
import puurrtybot.database.query as dq


def get_asset_name(asset: str):
    return dq.get_asset_by_asset_id(asset).name


def get_asset_image_url(asset: str):
    return dq.get_asset_by_asset_id(asset).img_url


def get_asset_image(asset: str, basewidth: int = 1200, stream: bool = True):
    image_url = f"""https://ipfs.io/ipfs/{get_asset_image_url(asset).split('/')[-1]}"""
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
        sh = dq.get_asset_by_asset_id(asset)
        sh.sales.sort(key=lambda x: x.timestamp, reverse=True)
        sales = [sale.amount/1_000_000 for sale in sh.sales]
        timestamps = [sale.timestamp for sale in sh.sales]
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
    except (KeyError, IndexError, ValueError):
        traded = volume = highest = lowest = 0
        last = bought = last_time = bought_time = None

    return {'traded':traded, 'volume':volume, 'last':last,'highest':highest, 'lowest':lowest, 'bought':bought, 'last_time':last_time, 'bought_time':bought_time}


def get_asset_sale_history_plot(asset):
    sh = dq.get_asset_by_asset_id(asset)
    sh.sales.sort(key=lambda x: x.timestamp, reverse=False)
    df = pd.DataFrame([(sale.amount/1_000_000, pf.timestamp_to_formatted_date_with_time(sale.timestamp).split(' at')[0]) for sale in sh.sales], columns=['sell','time'])
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