import configparser, tweepy, puurrtybot
from PIL import Image
import requests, puurrtybot, json
from io import BytesIO

def resize_image(img, basewidth=1200):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize), Image.ANTIALIAS)

# read config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = puurrtybot.TWITTER_KEY
api_secret = puurrtybot.TWITTER_KEY_SECRET
bearer_token = puurrtybot.TWITTER_BEARER_TOKEN
access_token = puurrtybot.TWITTER_ACCESS_TOKEN
access_token_secret = puurrtybot.TWITTER_ACCESS_TOKEN_SECRET

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Creating API instance. This is so we still have access to Twitter API V1 features
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)


def tweet(content):
    api.update_status(f"""{content}""")


def tweet_sale(content, asset):
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    with open(f"""{asset_dir}{asset}.json""", 'r') as openfile:
        asset = json.load(openfile)
        
    image_url = f"""https://cloudflare-ipfs.com/ipfs/{asset['onchain_metadata']['image'].split('/')[-1]}"""

    image = resize_image(Image.open(BytesIO(requests.get(image_url).content)))

    b = BytesIO()
    image.save(b, "PNG")
    b.seek(0)

    ret = api.media_upload(filename="dummy_string", file=b)

    temp = api.update_status(media_ids=[ret.media_id_string], status=content)
    return temp.id