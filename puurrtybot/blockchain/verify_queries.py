import requests, puurrtybot, datetime
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


def get_quantities_by_address(address: str, time_limit = 70*60):
    quantities = []
    for tx in get_tx_list_by_address(address):
        if tx['block_time'] - int(datetime.datetime.now().timestamp()) + time_limit > 0:
            quantities += get_quantities_by_tx_hash(tx['tx_hash'], address)
    return quantities


def verify_wallet(address: str, quantitiy):
    address = get_address_by_adahandle(address)
    quantities = get_quantities_by_address(address)
    if str(quantitiy).replace('.','') in quantities:
        return True
    else:
        return False