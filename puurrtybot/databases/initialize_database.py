import puurrtybot, tqdm, json
import puurrtybot.blockchain.blockchain_queries as blockfrost
import puurrtybot.blockchain.meta as meta


def initialize_assets():
    for asset in tqdm.tqdm(blockfrost.get_assets_by_policy(puurrtybot.POLICY)):
        asset = blockfrost.get_meta_by_asset(asset)
        asset['address'] = blockfrost.get_addr_by_asset(asset['asset'])
        try:
            asset['onchain_metadata']["unique"]
        except KeyError:
            asset['onchain_metadata']['prefix'] = meta.name_has_prefix(asset['onchain_metadata']['name'])
            lastname = meta.name_has_lastname(asset['onchain_metadata']['name'])
            suffix = meta.name_has_suffix(asset['onchain_metadata']['name'])
            asset['onchain_metadata']['firstname'] = asset['onchain_metadata']['name'].replace(asset['onchain_metadata']['prefix'],'').replace(lastname,'').replace(suffix,'').strip()
            asset['onchain_metadata']['lastname'] = lastname
            asset['onchain_metadata']['suffix'] = suffix
        with open(f"""{puurrtybot.PATH}/puurrtybot/databases/assets/{asset['asset']}.json""", 'w') as f:
            json.dump(asset, f)



def initial_setup():
    initialize_assets()
    pass

initial_setup()