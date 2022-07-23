import requests, puurrtybot
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
        sales = puurrtybot.ASSETS_SALES_HISTORY[asset]['amounts']
        timestamps = puurrtybot.ASSETS_SALES_HISTORY[asset]['timestamps']
        volume = sum(sales)
        highest = max(sales)
        lowest = min(sales)
        traded = len(sales)
        last = sales[-1]
        last_time = timestamps[-1]
        if len(sales)>1:
            bought = sales[-2]
            bought_time = timestamps[-2]
        else:
            bought = bought_time = None
    except (KeyError, IndexError):
        traded = volume = highest = lowest = 0
        last = bought = last_time = bought_time = None

    return {'traded':traded, 'volume':volume, 'last':last,'highest':highest, 'lowest':lowest, 'bought':bought, 'last_time':last_time, 'bought_time':bought_time}


def get_asset_sale_histoy_old(asset):
    sale_history = requests.get(f"""https://server.jpgstoreapis.com/token/{asset}/price-history""").json()
    try:
        sales = [sale['min_sale_price'] for sale in sale_history]
    except KeyError:
        sales = [0]
    if sales:
        volume = sum(sales)
        highest = max(sales)
        lowest = min(sales)
        traded = len(sales)
    else:
        traded = volume = highest = lowest = 0
    try:
        last = sales[-1]
    except IndexError:
        last = None
    try:
        previous = sale_history[-2]['min_sale_price']
    except (IndexError, KeyError):
        previous = None
    return {'traded':traded, 'volume':volume, 'last':last, 'previous':previous, 'highest':highest, 'lowest':lowest}