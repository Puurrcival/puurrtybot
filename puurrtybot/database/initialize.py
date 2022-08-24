import tqdm, puurrtybot
from puurrtybot.pcs.metadata import Name
from puurrtybot.database.create import Asset, Session
from puurrtybot.api import jpgstore, twitter
from puurrtybot import TWITTER_ID

def none_string_to_none(string: str):
    return None if string == 'None' else string


def initialize_assets():
    for asset in tqdm.tqdm(puurrtybot.ASSETS.values()):
        name = asset['onchain_metadata'].get('name')
        if asset['onchain_metadata'].get('unique'):
            prefix_name = first_name = last_name = suffix_name = None
        else:
            name_parts = Name(name)
            prefix_name = name_parts.prefix
            first_name = name_parts.firstname
            last_name = name_parts.lastname
            suffix_name = name_parts.suffix

        Session.add(Asset(
            asset_id = asset['asset'],
            address = None,
            address_type = None,
            stake_address = None,
            stake_address_type = None,
            policy_id = asset.get('policy_id'),
            asset_fingerprint = asset['fingerprint'],
            initial_mint_tx_hash = asset.get('initial_mint_tx_hash'),
            quantity = int(asset.get('quantity')),
            asset_name = asset.get('asset_name'),         
            name = asset['onchain_metadata'].get('name'),
            unique = none_string_to_none(asset['onchain_metadata'].get('unique')),
            prefix_name = none_string_to_none(prefix_name),
            first_name = none_string_to_none(first_name),
            last_name = none_string_to_none(last_name),
            suffix_name = none_string_to_none(suffix_name),
            img_url = asset['onchain_metadata'].get('image'),                       
            fur = none_string_to_none(asset['onchain_metadata'].get('fur')), 
            hat = none_string_to_none(asset['onchain_metadata'].get('hat')), 
            eyes = none_string_to_none(asset['onchain_metadata'].get('eyes')),  
            mask = none_string_to_none(asset['onchain_metadata'].get('mask')), 
            tail = none_string_to_none(asset['onchain_metadata'].get('tail')), 
            hands = none_string_to_none(asset['onchain_metadata'].get('hands')),  
            mouth = none_string_to_none(asset['onchain_metadata'].get('mouth')),  
            wings = none_string_to_none(asset['onchain_metadata'].get('wings')),  
            outfit = none_string_to_none(asset['onchain_metadata'].get('outfit')),  
            background = none_string_to_none(asset['onchain_metadata'].get('background')), 
            collection = asset['onchain_metadata'].get('collection'),
            mint_price = int(1_000_000*float(asset.get('mint_price'))), 
            mint_time = asset.get('mint_time'), 
            ))


def initialize_sales():
    for sale in jpgstore.get_sales(100_000):
        Session.add(sale)
    Session.commit()

def initialize_listings():
    for listing in jpgstore.get_listings(10_000):
        Session.add(listing)
    Session.commit()

def initialize_tweets():
    for tweet in twitter.get_mentions_by_twitter_id(TWITTER_ID):
        Session.add(tweet)
    Session.commit()

initialize_assets()
initialize_sales()
initialize_listings()
initialize_tweets()