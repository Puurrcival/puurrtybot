import tqdm, puurrtybot
from puurrtybot.pcs.config import POLICY_ID
from puurrtybot.pcs.metadata import Name
from puurrtybot.database.create import Asset, Role, SESSION, sql_commit_list
from puurrtybot.api import jpgstore, twitter
from puurrtybot.pcs import TWITTER_ID
import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.databases.database_queries as ddq
from puurrtybot.pcs import role
from puurrtybot.database import temp


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

        address = blockfrost.get_address_by_asset(asset['asset'])
        stake_address = blockfrost.get_stake_address_by_address(address)

        SESSION.add(Asset(
            asset_id = asset['asset'],
            address = address,
            address_type = blockfrost.get_address_type(address),
            stake_address = stake_address,
            stake_address_type = blockfrost.get_address_type(stake_address),
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


@sql_commit_list
def initialize_sales():
    return [sale for sale in jpgstore.get_sales(POLICY_ID, 100_000)]

@sql_commit_list
def initialize_listings():
    return [listing for listing in jpgstore.get_listings(POLICY_ID, 10_000)]

@sql_commit_list
def initialize_tweets():
    return [tweet for tweet in twitter.get_mentions_by_twitter_id(TWITTER_ID)]

@sql_commit_list
def initialize_users():
    return [user for user in temp.get_init_users()]

@sql_commit_list
def initialize_addresses():
    return [address for address in temp.get_init_address()]

@sql_commit_list
def initialize_roles():
    roles = []
    for user in temp.get_init_users():
        for role_id, role_object in role.ID_2_ROLE.items():
            value = ddq.check_role_qualify(role_object, user.user_id)
            value = True if value > 0 else False
            roles.append(Role(role_id=role_id, requirement=value, user_id= user.user_id))
    return roles


#initialize_assets()
#initialize_sales()
#initialize_listings()
#initialize_tweets()
#initialize_users()
#initialize_addresses()
#initialize_roles()