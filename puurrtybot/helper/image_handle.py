import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from puurrtybot import IMAGES_DIR, DATABASES_DIR
from puurrtybot.database import query as dq
from puurrtybot.database.create import Asset

def get_asset_image(asset: str, basewidth: int = 1200, stream: bool = True):
    image = Image.open(f"{IMAGES_DIR}/{asset}.png")
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


def puurrdo():
    puurrdo = "f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e5075757272646f"
    assets = random.sample([asset.asset_id for asset in dq.fetch_table(Asset) if asset.name!="Puurrdo"], 25)
    assets = {ix:asset for ix, asset in enumerate(assets)}
    im = Image.new(mode="RGB", size=(1060, 1060))

    counter = 0
    x = y = 210
    answer = random.choice(range(25))
    assets[answer] = puurrdo
    for row in range(5):
        for col in range(5):
            asset_im = get_asset_image(assets[counter], stream=False).resize((200, 200))
            im.paste(asset_im, (col*x+10, row*x+10))
            counter+=1

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(f"{DATABASES_DIR}/pcs.ttf", 50)        
    for row in range(5):
        for col in range(5):
            draw.text((col*x+15, row*y+10), f"""{row*5+col+1}""", font=font, fill =(47, 79, 79))

    image = draw._image
    image_stream = BytesIO()
    image.save(image_stream, "PNG")
    image_stream.seek(0)
    return (image_stream, answer+1)