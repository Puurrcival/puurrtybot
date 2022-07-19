import binascii, requests, puurrtybot, datetime
headers = {'project_id': puurrtybot.BLOCKFROST_TOKEN}


def get_stake_by_address(address):
    try:
        return requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}', headers=headers).json()['stake_address']
    except KeyError:
        return False


def get_address_by_adahandle(address):
    address = address.strip()
    temp = address
    #https://docs.adahandle.com/
    policyID_adahandle = 'f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a'
    adahandle = address.strip('$')
    adahandle =  bytes(adahandle, 'utf-8')
    asset = f"""{policyID_adahandle}{binascii.hexlify(adahandle).decode('utf-8')}"""
    try:
        address = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset}/addresses', headers=headers).json()[0]['address']
    except KeyError:
        address = temp
    if 200 == requests.get(f"""https://pool.pm/wallet/{address}""", headers=headers).status_code:
        return address
    else:
        return False


def get_addresses_by_address(address):
    address = address.strip()
    if 200 != requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}', headers=headers).status_code:
        #https://docs.adahandle.com/
        policyID_adahandle = 'f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a'
        adahandle = address.strip('$')
        adahandle =  bytes(adahandle, 'utf-8')
        asset = f"""{policyID_adahandle}{binascii.hexlify(adahandle).decode('utf-8')}"""
        try:
            address = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset}/addresses', headers=headers).json()[0]['address']
        except KeyError:
            address = adahandle

    if 200 == requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}', headers=headers).status_code:
        stake_address = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}', headers=headers).json()['stake_address']
        if stake_address:
            addresses = {address['address']:True for address in requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/accounts/{stake_address}/addresses', headers=headers).json()}
            return addresses
        else:
            return False
    return False


def check_if_quantity_in_tx(tx_hash, quantity, addresses):
    r = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/txs/{tx_hash}/utxos', headers = headers).json()
    if [True for inp in r['outputs'] if addresses.get(inp['address'], False) and inp['amount'][0]['quantity']==quantity] and [True for inp in r['inputs'] if addresses.get(inp['address'], False)]:
        return True
    return False


def check_transaction_of_address(address, quantity, addresses):
    time_limit = 70*60
    page = 1
    while True:
        r = requests.get(f'https://cardano-mainnet.blockfrost.io/api/v0/addresses/{address}/transactions?order=desc&page={page}', headers=headers).json()
        if r and r[0]['block_time'] - int(datetime.datetime.utcnow().timestamp()) + time_limit > 0:
            for tx in r:
                if check_if_quantity_in_tx(tx_hash=tx['tx_hash'], quantity=quantity, addresses=addresses):
                    return True
            page += 1
        else:
            break;
    return False


def verify_wallet(address, quantity):
    try:
        addresses = get_addresses_by_address(address)
    except KeyError:
        return False
    if addresses:
        try:
            return check_transaction_of_address(address, quantity, addresses)
        except KeyError:
            return False
    else:
        return False