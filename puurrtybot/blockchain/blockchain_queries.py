import puurrtybot, requests
headers = {'project_id': puurrtybot.BLOCKFROST_TOKEN}


def get_address_by_adahandle(adahandle: str):
    adahandle = f"""${adahandle.strip('$')}""".strip()
    try:
        return requests.get(f"""https://pool.pm/wallet/{adahandle}""").json()['addr']
    except KeyError:
        try:
            if requests.get(f"""https://pool.pm/wallet/{adahandle.strip('$')}""").json()['addr'][:4] in ['stak', 'addr']:
                    return adahandle.strip('$')
        except KeyError:
            return False


def get_assets_by_policy(policy):
    page=1
    assets=[]
    while True:
        r = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy}?page={page}', headers=headers)
        if len(r.json())==0:
            break;
        else:
            assets+=r.json()
            page+=1

    return [asset['asset'] for asset in assets if asset['quantity']=='1']


def get_meta_by_asset(asset):
    return requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset}', headers=headers).json()


def get_addr_by_asset(asset):
    return  requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset}/addresses', headers=headers).json()[0]['address']


def get_stake_by_address(address):
    try:
        return requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}', headers=headers).json()['stake_address']
    except KeyError:
        return address


def get_tx_list_by_address(address: str):
    tx_list = []
    page = 1
    while True:
        r = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}/transactions?page={page}', headers=headers).json()
        if r:
            tx_list += r
            page += 1
        else:
            break;
    return tx_list


def get_quantities_by_tx_hash(tx_hash: str, address: str):
    r = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/txs/{tx_hash}/utxos', headers = headers)
    tx_addresses = list(set(list(out['address'] for out in r.json()['outputs']) + list(inp['address'] for inp in r.json()['inputs'])))
    if len(tx_addresses) == 1 and tx_addresses[0] == address:
        return [amount[0]['quantity'] for amount in list(output['amount'] for output in r.json()['outputs'])]
    else:
        return [0]
        