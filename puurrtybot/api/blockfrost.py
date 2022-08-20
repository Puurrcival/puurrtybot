"""Functions for Blockrost.io
- https://blockfrost.io/
- 50,000 requests a day (resets midnight of UTC time)
- 10 requests per second
"""

from binascii import hexlify
from typing import Union, List

import requests
from requests.models import Response
from pycardano import Address, Network

from puurrtybot import BLOCKFROST_TOKEN


HEADERS = {'project_id': BLOCKFROST_TOKEN}
NETWORK = 'https://cardano-mainnet.blockfrost.io/api/v0'
BLOCKFROST_STATUS_CODES = {
    # https://docs.blockfrost.io/#section/Errors
    400: """The request is not valid.""",
    402: """The project exceeded their daily request limit.""",
    403: """The request is not authenticated.""",
    404: """The resource doesn't exist.""",
    418: """The user has been auto-banned for flooding too much after previously receiving error code 402 or 429.""",
    425: """The user has submitted a transaction when the mempool is already full, not accepting new txs straight away.""",
    429: """The user has sent too many requests in a given amount of time and therefore has been rate-limited.""",
    500: """Our endpoints are having a problem."""}


def query(query_string: str) -> Response:
    """Query blockfrost.io and check for valid response."""
    response = requests.get(f"""{NETWORK}{query_string}""", headers=HEADERS)
    if response.status_code != 200:
        raise Exception( (response.status_code, f"""{BLOCKFROST_STATUS_CODES[response.status_code]}""") )
    return response


def address_exists(address: str) -> bool:
    """Check if address has a valid form."""
    try:
        Address.from_primitive(address)
        return True
    except TypeError:
        return False


def get_server_time() -> int:
    """Get server time in seconds from blockrost.io."""
    return int(query(f"""/health/clock""").json()['server_time']/1000)


def get_asset_list_by_policy(policy: str,
                             order: str = 'asc',
                             max_pages: int = -1,
                             quantity: int = 1) -> list:
    """Get all assets of a policy."""
    page = 1
    asset_list = []
    while max_pages != page-1:
        response = query(f"""/assets/policy/{policy}?order={order}&page={page}""")
        query_result = response.json()
        if len(query_result) > 0:
            asset_list += query_result
            page += 1
        else:
            break
    return [asset['asset'] for asset in asset_list if int(asset['quantity']) == quantity]


def get_meta_by_asset(asset: str) -> dict:
    """Get metadata of an asset."""
    return query(f"""/assets/{asset}""").json()


def get_address_by_asset(asset: str) -> str:
    """Get the address of an asset."""
    return query(f"""/assets/{asset}/addresses""").json()[0]['address']


def get_stake_address_by_address(address: str) -> Union[str, None]:
    """Get the stake_address of a Cardano address."""
    try:
        address = Address.from_primitive(address)
        return str(Address(staking_part=address.staking_part, network=Network.MAINNET))
    except TypeError:
        return None


def get_address_list_by_stake_address(stake_address: str) -> List[str]:
    """Get a list of addresses belonging to a stake_address."""
    address_list = query(f"""/accounts/{stake_address}/addresses""").json()
    return [entry['address'] for entry in address_list]


def get_tx_hash_list_by_address(address: str,
                                order: str = 'desc',
                                max_pages: int = 0,
                                past_time: int = 1*1*60*60,
                                hash_only: bool = True) -> List[str]:
    """Get a list of tx_hashes used by a Cardano address.

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
        response = query(f"""/addresses/{address}/transactions?order={order}&page={page}""")
        query_result = response.json()
        if len(query_result) > 0 and query_result[0]['block_time'] > time_window:
            tx_hash_list += query_result
            page += 1
        else:
            break
    if hash_only:
        return [tx_hash['tx_hash'] for tx_hash in tx_hash_list]
    else:
        return [tx_hash for tx_hash in tx_hash_list]


def get_utxo_list_by_tx_hash(tx_hash: str) -> dict:
    """Get a list of UTXO of a tx_hash.

    Args:
        tx_hash (str): x_hash of a Cardano transaction.

    Returns:
        dict: Inputs and Outputs of a transaction.
    """
    return query(f"""/txs/{tx_hash}/utxos""").json()


def get_tx_by_tx_hash(tx_hash: str) -> str:
    """Get transaction of a tx_hash.

    Args:
        tx_hash (str): tx_hash of a Cardano transaction.

    Returns:
        str: Cardano transaction.
    """    
    return query(f"""/txs/{tx_hash}""").json()


def get_address_by_adahandle(address: str) -> str:
    """Get the Cardano address of an adahandle, see https://docs.adahandle.com/.

    Args:
        address (str): Cardano address or adahandle.

    Returns:
        str: Cardano address.
    """
    if not address_exists(address):
        adahandle = address.strip('$')
        policyID = "f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a"
        asset = f"""{policyID}{hexlify(bytes(adahandle, 'utf-8')).decode('utf-8')}"""
        address = get_address_by_asset(asset)
    return address