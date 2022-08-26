from io import BytesIO

from PIL import Image

from puurrtybot import IMAGES_DIR


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