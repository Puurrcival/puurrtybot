from binascii import hexlify
from typing import Union

import requests

import puurrtybot

HEADERS = {'project_id': puurrtybot.BLOCKFROST_TOKEN}
NETWORK = 'https://cardano-mainnet.blockfrost.io/api/v0'

# https://blockfrost.io/
# 50,000 requests a day (resets midnight of UTC time)
# 10 requests per second


# https://docs.blockfrost.io/#section/Errors
BLOCKFROST_HHTP_CODES = {
    400: """The request is not valid.""",
    402: """The project exceeded their daily request limit.""",
    403: """The request is not authenticated.""",
    404: """The resource doesn't exist.""",
    418: """The user has been auto-banned for flooding too much after previously receiving error code 402 or 429.""",
    425: """The user has submitted a transaction when the mempool is already full, not accepting new txs straight away.""",
    429: """The user has sent too many requests in a given amount of time and therefore has been rate-limited.""",
    500: """Our endpoints are having a problem."""}


def blockfrost_check_response(status_code: int):
    """Check for valid connection to blockfrost.io.

    Args:
        status_code (INT): _description_

    Raises:
        Exception: 200 is the only legal status code.
    """
    if status_code != 200:
        raise Exception(f"""{BLOCKFROST_HHTP_CODES[status_code]}""")


def get_server_time() -> int:
    """Get server time from blockrost.io, \
        see https://docs.blockfrost.io/#tag/Health/paths/~1health~1clock/get.

    Returns:
        int: timestamp in seconds
    """
    response = requests.get(f"""{NETWORK}/health/clock""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    return int(response.json()['server_time']/1000)


def get_asset_list_by_policy(policy: str,
                             order: str = 'asc',
                             max_pages: int = -1,
                             quantity: int = 1) -> list:
    """Get all assets of a policy, see \
        https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1policy~1{policy_id}/get.

    Args:
        policy (str): The Policy.
        order (str, optional): Order 'asc' or 'desc' for descending. \
            Defaults to 'asc'.
        max_pages (int, optional): -1 will get all pages. Defaults to -1.
        quantity (int, optional): Quantity of a token. Defaults to 1.

    Returns:
        list: A list of assets.
    """
    page = 1
    asset_list = []
    while max_pages != page-1:
        response = requests.get(f"""{NETWORK}/assets/policy/{policy}?order={order}&page={page}""",
                                headers=HEADERS)
        blockfrost_check_response(response.status_code)
        query_result = response.json()
        if len(query_result) > 0:
            asset_list += query_result
            page += 1
        else:
            break
    return [asset['asset'] for asset in asset_list
            if int(asset['quantity']) == quantity]


def get_meta_by_asset(asset: str) -> dict:
    """Get metadata of an asset, see \
        https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1{asset}/get.

    Args:
        asset (str): The asset = {policy id}{asset_name}.

    Returns:
        dict: The metadata as a dictionarys.
    """
    response = requests.get(f"""{NETWORK}/assets/{asset}""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    return response.json()


def get_address_by_asset(asset: str) -> str:
    """Get the address of an asset, see \
        https://docs.blockfrost.io/#tag/Cardano-Assets/paths/~1assets~1{asset}~1addresses/get.

    Args:
        asset (str): The asset = {policy id}{asset_name}.

    Returns:
        str: The address.
    """
    response = requests.get(f"""{NETWORK}/assets/{asset}/addresses""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    return response.json()[0]['address']


def get_stake_address_by_address(address: str) -> Union[str, None]:
    """Get the stake_address of a Cardano address, see \
        https://docs.blockfrost.io/#tag/Cardano-Accounts/paths/~1accounts~1{stake_address}~1addresses/get.

    Args:
        address (str): The Cardano address.

    Returns:
        str | None: If available the stake_address, else None.
    """
    try:
        response = requests.get(f"""{NETWORK}/addresses/{address}""",
                                headers=HEADERS)
        blockfrost_check_response(response.status_code)
        return response.json()['stake_address']
    except KeyError:
        return None


def get_address_list_by_stake_address(stake_address: str) -> Union[list, None]:
    """Get a list of Cardano addresses belonging to a stake_address, see \
        https://docs.blockfrost.io/#tag/Cardano-Accounts/paths/~1accounts~1{stake_address}~1addresses/get.

    Args:
        stake_address (str): Cardano stake_address.

    Returns:
        list | None: If addresses exist return List else None.
    """
    response = requests.get(f"""{NETWORK}/accounts/{stake_address}/addresses""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    query_result = response.json()
    if len(query_result) == 0:
        return None
    else:
        return [entry['address'] for entry in query_result]


def get_tx_hash_list_by_address(address: str,
                                order: str = 'desc',
                                max_pages: int = 0,
                                past_time: int = 1*1*60*60,
                                hash_only: bool = True) -> list:
    """Get a list of tx_hashes used by a Cardano address, see \
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1transactions/get.

    Args:
        address (str): Cardano address.
        order (str, optional): 'asc' for ascending order and 'desc' for descending. Defaults to 'asc'.
        max_pages (int, optional): -1 will get all pages. Defaults to -1.
        past_time (int, optional): The time window. Defaults to 1*1*60*60.
        hash_only (bool, optional): If True return only the tx_hash values, else full information. Defaults to True.

    Returns:
        list: A list of tx_hashes.
    """
    time_window = get_server_time() - past_time
    tx_hash_list = []
    page = 1
    while max_pages != page:
        response = requests.get(f"""{NETWORK}/addresses/{address}/transactions?order={order}&page={page}""",
                                headers=HEADERS)
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


def get_utxo_list_by_tx_hash(tx_hash: str) -> dict:
    """Get a list of UTXO of a tx_hash, see https://docs.blockfrost.io/#tag/Cardano-Transactions/paths/~1txs~1{hash}~1utxos/get.

    Args:
        tx_hash (str): x_hash of a Cardano transaction.

    Returns:
        dict: Inputs and Outputs of a transaction.
    """
    response = requests.get(f"""{NETWORK}/txs/{tx_hash}/utxos""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    return response.json()


def get_tx_by_tx_hash(tx_hash: str) -> str:
    """Get transaction of a tx_hash, see https://docs.blockfrost.io/#tag/Cardano-Transactions/paths/~1txs~1{hash}/get.

    Args:
        tx_hash (str): tx_hash of a Cardano transaction.

    Returns:
        str: Cardano transaction.
    """    
    response = requests.get(f"""{NETWORK}/txs/{tx_hash}""",
                            headers=HEADERS)
    blockfrost_check_response(response.status_code)
    return response.json()


def get_address_by_adahandle(address: str) -> str:
    """Get the Cardano address of an adahandle, see https://docs.adahandle.com/.

    Args:
        address (str): Cardano address or adahandle.

    Returns:
        str: Cardano address.
    """
    if len(address) < 20:
        adahandle = address.strip('$')
        asset = f"""f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a{hexlify(bytes(adahandle, 'utf-8')).decode('utf-8')}"""
        address = get_address_by_asset(asset)
    return address.strip()


def check_address_exists(address: str) -> bool:
    """User pool.pm to check if a Cardano address exists. In future this workaround-function could be replaced with a bech32 implementation.

    Args:
        address (str): _description_

    Returns:
        bool: _description_
    """
    if 200 == requests.get(f"""https://pool.pm/wallet/{address}""", headers=HEADERS).status_code:
        return True
    else:
        return False