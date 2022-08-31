import tqdm, requests, time

import puurrtybot
from puurrtybot.pcs.config import POLICY_ID
from puurrtybot.pcs.metadata import Name
from puurrtybot.database.create import Asset, Role, session, sql_insert
from puurrtybot.api import blockfrostio, jpgstore, twitter
from puurrtybot.pcs import TWITTER_ID
from puurrtybot.database import query as dq
from puurrtybot.pcs.role import ID_2_ROLE
from puurrtybot.data import init_data


def none_string_to_none(string: str):
    return None if string == 'None' else string


def get_mint_price(amount):
    amount = int(int(amount)/1_000_000)
    if amount%52==0:
        return 52
    if amount%62==0:
        return 62
    if amount%72==0:
        return 72
    if amount%82==0:
        return 82
    if amount%92==0:
        return 92
    if amount%100==0:
        return 100
    if amount==5:
        return 1
    return amount


def initialize_mint_prices(mint_address: str = 'addr1vxk4szdzv6qxqne5k3m0wr4m5cewh2pnt23tn3tx2x28zsq7ml8dm'):
    mint_tx_hash_list = blockfrostio.get_tx_hash_list_by_address(mint_address, order="asc", past_time = blockfrostio.get_server_time(), hash_only=False)
    quantity_inputs = {}
    for tx in tqdm.tqdm(mint_tx_hash_list):
        block_time = tx['block_time']
        utxo_list = blockfrostio.get_utxo_list_by_tx_hash(tx['tx_hash'])
        inputs = [utxo['address'] for utxo in utxo_list['inputs']]
        outputs = [utxo['amount'][0]['quantity'] for utxo in utxo_list['outputs'] if utxo['address']==mint_address]
        if outputs:
            quantity_inputs[tx['tx_hash']] = {'block_time':block_time, 'input_addresses': inputs, 'quantities': outputs}

    mint_matches = {}
    for asset in tqdm.tqdm(dq.get_asset_all()):
        utxo_list = blockfrostio.get_utxo_list_by_tx_hash(asset.initial_mint_tx_hash)
        mint_address = [utxo['address']  for utxo in utxo_list['outputs'] if [amount for amount in utxo['amount'] if asset == amount['unit']]][0]
        mint_block_time = blockfrostio.get_tx_by_tx_hash(asset.initial_mint_tx_hash)['block_time']
        for _ , data in quantity_inputs.items():
            if data['block_time'] < mint_block_time and mint_address in data['input_addresses']:
                try:
                    mint_matches[asset] += [{'mint_block_time': mint_block_time,'block_time': data['block_time'], 'address': mint_address, 'quantity':data['quantities']}]
                except KeyError:
                    mint_matches[asset] = [{'mint_block_time': mint_block_time,'block_time': data['block_time'], 'address': mint_address, 'quantity':data['quantities']}]
        try:
            mint_matches[asset.asset_id]
        except KeyError:
            mint_matches[asset.asset_id] = mint_block_time

    assets_mint = {}
    for asset, data in mint_matches.items():
        if type(data) != int:
            asset.mint_price = [get_mint_price(d['quantity'][0]) for d in data][-1]
            asset.mint_time = data[0]['mint_block_time']
        else:
            asset.mint_price = 0
            asset.mint_time = data
    

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

        try:
            address = blockfrostio.get_address_by_asset(asset['asset'])
        except requests.ConnectionError:
            time.sleep(5)
            address = blockfrostio.get_address_by_asset(asset['asset'])
        stake_address = blockfrostio.get_stake_address_by_address(address)

        session.add(Asset(
            asset_id = asset['asset'],
            address = address,
            address_type = blockfrostio.get_address_type(address),
            stake_address = stake_address,
            stake_address_type = blockfrostio.get_address_type(stake_address),
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


@sql_insert
def initialize_sales():
    return [sale for sale in jpgstore.get_sales(POLICY_ID, 100_000)]

@sql_insert
def initialize_listings():
    return [listing for listing in jpgstore.get_listings(POLICY_ID, 10_000)]

@sql_insert
def initialize_tweets():
    return [tweet for tweet in twitter.get_mentions_by_twitter_id(TWITTER_ID)]

@sql_insert
def initialize_users():
    return [user for user in init_data.get_init_users()]

@sql_insert
def initialize_addresses():
    return [address for address in init_data.get_init_address()]

@sql_insert
def initialize_roles():
    roles = []
    for user in init_data.get_init_users():
        for role_id, role_object in ID_2_ROLE.items():
            value = dq.qualify_role(role_object, user.user_id)
            value = True if value > 0 else False
            roles.append(Role(role_id=role_id, requirement=value, user_id= user.user_id))
    return roles


initialize_assets()
initialize_sales()
initialize_listings()
initialize_tweets()
initialize_users()
initialize_addresses()
initialize_roles()