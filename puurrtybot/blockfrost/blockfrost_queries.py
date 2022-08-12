import puurrtybot, requests, binascii
headers = {'project_id': puurrtybot.BLOCKFROST_TOKEN}
network = 'https://cardano-mainnet.blockfrost.io/api/v0'

# https://blockfrost.io/
# 50,000 requests a day (resets midnight of UTC time)
# 10 requests per second


# https://docs.blockfrost.io/#section/Errors
blockfrost_http_codes = { 
    400: """The request is not valid.""",
    402: """The project exceeded their daily request limit.""",
    403: """The request is not authenticated.""",
    404: """The resource doesn't exist.""",
    418: """The user has been auto-banned for flooding too much after previously receiving error code 402 or 429.""",
    425: """The user has submitted a transaction when the mempool is already full, not accepting new txs straight away.""",
    429: """The user has sent too many requests in a given amount of time and therefore has been rate-limited.""",
    500: """Our endpoints are having a problem."""}


def blockfrost_check_response(status_code):
    if status_code != 200:
        raise Exception(f"""{blockfrost_http_codes[status_code]}""")


# https://docs.blockfrost.io/#tag/Health/paths/~1health~1clock/get
def get_server_time() -> int:
    response = requests.get(f"""{network}/health/clock""", headers = headers)
    blockfrost_check_response(response.status_code)
    return int(response.json()['server_time']/1000)


# https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1policy~1{policy_id}/get
def get_asset_list_by_policy(policy: str, order: str = 'asc', max_pages: int = -1, quantity: int = 1) -> list:
    page = 1 
    asset_list = []
    while max_pages != page-1:
        response = requests.get(f"""{network}/assets/policy/{policy}?order={order}&page={page}""", headers=headers)
        blockfrost_check_response(response.status_code)
        query_result = response.json()
        if len(query_result) > 0:
            asset_list += query_result
            page += 1
        else:
            break;
    return [asset['asset'] for asset in asset_list if int(asset['quantity'])==quantity]


# https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1{asset}/get
def get_meta_by_asset(asset: str) -> dict:
    response = requests.get(f"""{network}/assets/{asset}""", headers=headers)
    blockfrost_check_response(response.status_code)
    return response.json()


# https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1{asset}~1addresses/get
def get_address_by_asset(asset: str) -> str:
    response = requests.get(f"""{network}/assets/{asset}/addresses""", headers=headers)
    blockfrost_check_response(response.status_code)
    return response.json()[0]['address']


# https://docs.blockfrost.io/#tag/Cardano-Accounts/paths/~1accounts~1{stake_address}~1addresses/get
def get_stake_address_by_address(address: str) -> str:
    try:
        response = requests.get(f"""{network}/addresses/{address}""", headers=headers)
        blockfrost_check_response(response.status_code)
        return response.json()['stake_address']
    except KeyError:
        return None


# https://docs.blockfrost.io/#tag/Cardano-Accounts/paths/~1accounts~1{stake_address}~1addresses/get
def get_address_list_by_stake_address(stake_address: str) -> list:
    response = requests.get(f"""{network}/accounts/{stake_address}/addresses""", headers = headers)
    blockfrost_check_response(response.status_code)
    query_result = response.json()
    if len(query_result)==0:
        return None
    else:
        return [entry['address'] for entry in query_result]


# https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1transactions/get
def get_tx_hash_list_by_address(address: str, order: str = 'desc', max_pages: int = 0, past_time: int = 1*1*60*60, hash_only: bool = True) -> list:
    time_window = get_server_time() - past_time
    tx_hash_list = []
    page = 1
    while max_pages != page:
        response = requests.get(f"""{network}/addresses/{address}/transactions?order={order}&page={page}""", headers=headers)
        blockfrost_check_response(response.status_code)
        query_result = response.json()
        if len(query_result) > 0 and query_result[0]['block_time'] > time_window:
            tx_hash_list += query_result
            page += 1
        else:
            break;
    if hash_only:
        return [tx_hash['tx_hash'] for tx_hash in tx_hash_list]
    else:
        return [tx_hash for tx_hash in tx_hash_list]


# https://docs.blockfrost.io/#tag/Cardano-Transactions/paths/~1txs~1{hash}~1utxos/get
def get_utxo_list_by_tx_hash(tx_hash: str) -> dict:
    response = requests.get(f"""{network}/txs/{tx_hash}/utxos""", headers = headers)
    blockfrost_check_response(response.status_code)
    return response.json()


# https://docs.blockfrost.io/#tag/Cardano-Transactions/paths/~1txs~1{hash}/get
def get_tx_by_tx_hash(tx_hash: str) -> str:
    response = requests.get(f"""{network}/txs/{tx_hash}""", headers=headers)
    blockfrost_check_response(response.status_code)
    return response.json()


# https://docs.adahandle.com/
def get_address_by_adahandle(address: str) -> str:
    if len(address) < 20:
        adahandle = address.strip('$')
        asset = f"""f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a{binascii.hexlify(bytes(adahandle, 'utf-8')).decode('utf-8')}"""
        address = get_address_by_asset(asset)
    return address.strip()


# in future this workaround-function could be replaced with a bech32 implementation
def check_address_exists(address: str) -> bool:
    if 200 == requests.get(f"""https://pool.pm/wallet/{address}""", headers=headers).status_code:
        return True
    else:
        return False