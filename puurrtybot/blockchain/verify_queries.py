import requests, puurrtybot, datetime, json
import puurrtybot.blockchain.blockchain_queries as pbq
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
    for tx in pbq.get_tx_list_by_address(address):
        if tx['block_time'] - int(datetime.datetime.now().timestamp()) + time_limit > 0:
            quantities += pbq.get_quantities_by_tx_hash(tx['tx_hash'], address)
    return quantities


def verify_wallet(address: str, quantitiy):
    address = get_address_by_adahandle(address)
    quantities = get_quantities_by_address(address)
    if str(quantitiy).replace('.','') in quantities:
        return True
    else:
        return False

def add_verified_wallet(userid, address):
    with open(f"""{puurrtybot.PATH}/puurrtybot/databases/users/{userid}.json""", 'r') as f:
        j = json.load(f)

    j['verified_wallets'] = list(j['verified_wallets']) + address
    with open(f"""{puurrtybot.PATH}/puurrtybot/databases/users/{userid}.json""", "w") as f:
        json.dump(j, f)


def wallet_verify_status(userid, address):
    try:
        with open(f"""{puurrtybot.PATH}/puurrtybot/databases/users/{userid}.json""", 'r') as f:
            j = json.load(f)
    except FileNotFoundError:
        with open(f"""{puurrtybot.PATH}/puurrtybot/databases/users/{userid}.json""", "w") as f:
            j = {"userid":f"{userid}","verified_wallets":""}
            json.dump(j, f)

    if address in j['verified_wallets']:
        return True
    else:
        return False


def verify_wallet_stats(userid, address, quantity, status="False"):
    with open(f"""{puurrtybot.PATH}/puurrtybot/databases/verify_wallet/{address}.json""", "w") as f:
            json.dump({"userid":f"{userid}","quantity":f"{quantity}","verified":status}, f)