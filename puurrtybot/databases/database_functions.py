import puurrtybot, tqdm, os, json, requests
import puurrtybot.blockfrost.blockfrost_queries as blockfrost
import puurrtybot.assets.meta as meta
import puurrtybot.twitter.twitter_queries as tvt
headers = {'project_id': puurrtybot.BLOCKFROST_TOKEN}

def update_asset_address(asset):
    headers = {'project_id': puurrtybot.BLOCKFROST_TOKEN}
    address = blockfrost.get_address_by_asset(asset)
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    with open(f"""{asset_dir}{asset}.json""", 'r') as openfile:
        asset = json.load(openfile)
        asset['address'] = address

    with open(f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/{asset['asset']}.json""", 'w') as f:
        json.dump(asset, f)


def update_assets_addresses():
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    assets = [asset.split('.',1)[0] for asset in os.listdir(asset_dir)]
    for asset in tqdm.tqdm(assets):
        update_asset_address(asset)


def update_addresses_assets():
    addresses = {}
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    for asset in os.listdir(asset_dir):
        asset = asset.split('.')[0]
        address = blockfrost.get_address_by_asset(asset)
        try:
            addresses[address]+=[asset]
        except KeyError:
            addresses[address]=[asset]

    address_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_address/"""
    for address in os.listdir(address_dir):
        address = address.split('.')[0]
        try:
            assets = addresses[address]
            with open(f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_address/{address}.json""", 'w') as f:
                json.dump({address:assets}, f)
        except KeyError:
            os.unlink(f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_address/{address}.json""")


def assets_by_name():
    for asset in tqdm.tqdm(blockfrost.get_assets_by_policy(puurrtybot.POLICY)):
        asset = blockfrost.get_meta_by_asset(asset)
        asset['address'] = blockfrost.get_address_by_asset(asset['asset'])
        try:
            asset['onchain_metadata']["unique"]
        except KeyError:
            asset['onchain_metadata']['prefix'] = meta.name_has_prefix(asset['onchain_metadata']['name'])
            lastname = meta.name_has_lastname(asset['onchain_metadata']['name'])
            suffix = meta.name_has_suffix(asset['onchain_metadata']['name'])
            asset['onchain_metadata']['firstname'] = asset['onchain_metadata']['name'].replace(asset['onchain_metadata']['prefix'],'').replace(lastname,'').replace(suffix,'').strip()
            asset['onchain_metadata']['lastname'] = lastname
            asset['onchain_metadata']['suffix'] = suffix
        with open(f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/{asset['asset']}.json""", 'w') as f:
            json.dump(asset, f)


def asset_by_name_2_asset_by_address():
    assets = {}
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    for asset in tqdm.tqdm(os.listdir(asset_dir)):
        with open(f"""{asset_dir}{asset}""", 'r') as openfile:
            asset = json.load(openfile)
            try:
                assets[asset['address']]+= [asset['asset']]
            except KeyError:
                assets[asset['address']] = [asset['asset']]

    for asset in assets.items():
        with open(f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_address/{asset[0]}.json""", 'w') as f:
            json.dump({asset[0]:asset[1]}, f)


def update_database():
    assets_by_name()
    asset_by_name_2_asset_by_address()


def create_new_user(userid):
    path_to_file = f"""{puurrtybot.PATH}/puurrtybot/databases/users/{userid}.json"""
    if not os.path.exists(path_to_file):
        with open(path_to_file, 'w') as f:
            json.dump({"userid": f"""{userid}""", "wallets": [], "stakes":[], "assets":[]}, f)


def user_update_wallets(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""

    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)

    check_wallets = user['wallets']
    checked_wallets = []

    for wallet in check_wallets:
        if wallet not in checked_wallets:
            checked_wallets += blockfrost.get_addresses_by_address(wallet).keys()

    check_wallets = []
    stakes = []
    for wallet in checked_wallets:
        if wallet not in check_wallets:
            stake_address = bvw.get_stake_by_address(wallet)
            stakes.append(stake_address)
            check_wallets += [entry['address'] for entry in requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/accounts/{stake_address}/addresses', headers=headers).json()]

    user['wallets'] = list(set(check_wallets + checked_wallets))
    user['stakes'] = stakes
    with open(f"""{user_dir}{userid}.json""", 'w') as f:
        json.dump(user, f)


def user_update_assets(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
        wallets = user['wallets']
        
        wallet_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_address/"""
        for address in wallets:
            try:
                with open(f"""{wallet_dir}{address}.json""", 'r') as openfile:
                    assets = json.load(openfile)[address]
                    user['assets'] = list(set(user['assets'] + assets))
                    with open(f"""{user_dir}{userid}.json""", 'w') as f:
                        json.dump(user, f)
            except FileNotFoundError:
                pass


def user_add_wallet(userid, address):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
        user['wallets'] = list(set(user['wallets'] + [address]))

    with open(f"""{user_dir}{userid}.json""", 'w') as f:
        json.dump(user, f)


def user_set_twitter(userid, twitter_handle):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
        user['twitter'] = {twitter_handle:f"""{tvt.get_id_by_user(twitter_handle)}"""}

    with open(f"""{user_dir}{userid}.json""", 'w') as f:
        json.dump(user, f)


def user_check_wallet_exists(userid, address):
    puurrtybot.USERS[str(userid)]['addresses']
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
        if address in user['wallets']:
            return True
        else:
            return False


def user_update_traits(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)

    traits = {}
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    for asset in user['assets']:
        with open(f"""{asset_dir}{asset}.json""", 'r') as openfile:
             asset = json.load(openfile)
        for k,v in asset['onchain_metadata'].items():
            k = k.strip()
            v = v.strip()
            if k not in ['name', 'image', 'mediaType', 'collection'] and v!='':
                try:
                    traits[k]
                except KeyError:
                    traits[k] = {}

                try:
                    traits[k][v]+=1
                except KeyError:
                    traits[k][v] =1


    user['assets_n'] = len(user['assets'])
    user['traits']=traits

    with open(f"""{user_dir}{userid}.json""", 'w') as f:
        json.dump(user, f)



###### new
def save_assets():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets.json""", 'w') as json_file:
            json.dump(puurrtybot.ASSETS, json_file)


def save_assets_addresses():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets_addresses.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS_ADDRESSES ,json_file)


def save_market_sales():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_sales.json""", 'w') as json_file:
            json.dump(puurrtybot.MARKET_SALES, json_file)


def save_market_sales_tx_hash():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_sales_tx_hash.json""", 'w') as json_file:
            json.dump(puurrtybot.MARKET_SALES_TX_HASH, json_file)


def save_market_listings():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_listings.json""", 'w') as json_file:
            json.dump(puurrtybot.MARKET_LISTINGS, json_file)


def save_market_listings_ids():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_listings_ids.json""", 'w') as json_file:
            json.dump(puurrtybot.MARKET_LISTINGS_IDS, json_file)


def save_asset_sales_history():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets_sales_history.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS_SALES_HISTORY, json_file)


def save_twitter_mentions():
    with open(f"""{puurrtybot.DATABASES_DIR}/twitter_mentions.json""", 'w') as json_file:
        json.dump(puurrtybot.TWITTER_MENTIONS ,json_file)


def save_users():
    with open(f"""{puurrtybot.DATABASES_DIR}/users.json""", 'w') as json_file:
        json.dump(puurrtybot.USERS ,json_file)