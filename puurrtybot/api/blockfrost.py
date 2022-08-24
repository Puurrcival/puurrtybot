"""Functions for Blockrost.io
- https://blockfrost.io/
- 50,000 requests a day (resets midnight of UTC time)
- 10 requests per second
"""

import binascii
from typing import List, Optional

import requests
from requests.models import Response
from pycardano import Address, Network, AddressType
from pycardano.crypto.bech32 import decode
from pycardano.exception import InvalidAddressInputException

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
        raise Exception( (response.status_code, BLOCKFROST_STATUS_CODES[response.status_code]) )
    return response


def get_server_time() -> int:
    """Get server time in seconds from blockrost.io."""
    return int(query(f"""/health/clock""").json()['server_time']/1000)


def get_asset_list_by_policy_id(policy_id: str,
                             order: str = 'asc',
                             max_pages: int = -1,
                             quantity: int = 1) -> List[str]:
    """Get assets of a policy_id."""
    page = 1
    asset_list = []
    while max_pages != page-1:
        response = query(f"""/assets/policy/{policy_id}?order={order}&page={page}""")
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


def get_address_type(address: str) -> AddressType:
    try:
        return AddressType((bytes(decode(address))[0] & 0xF0) >> 4)
    except TypeError:
        return None


def valid_address(address: str) -> bool:
    """Check if address has a valid form."""
    if address:
        try:
            Address.from_primitive(address)
            return True
        except TypeError:
            pass
    return False

        
def get_stake_address_by_address(address: str) -> Optional[str]:
    """Get the stake_address of a Cardano address."""
    if address:
        try:
            address = Address.from_primitive(address)
            return str(Address(staking_part=address.staking_part, network=Network.MAINNET))
        except (TypeError, InvalidAddressInputException):
            pass
    return None


def get_address_list_by_stake_address(stake_address: str) -> List[str]:
    """Get a list of addresses belonging to a stake_address."""
    return [entry['address'] for entry in query(f"""/accounts/{stake_address}/addresses""").json()]


def get_tx_hash_list_by_address(address: str,
                                order: str = 'desc',
                                max_pages: int = 0,
                                past_time: int = 1*1*60*60,
                                hash_only: bool = True) -> List[str]:
    """Get a list of tx_hashes used by a Cardano address."""
    time_window = get_server_time() - past_time
    tx_hash_list = []
    page = 1
    while max_pages != page:
        query_result = query(f"""/addresses/{address}/transactions?order={order}&page={page}""").json()
        if len(query_result) > 0 and query_result[0]['block_time'] > time_window:
            tx_hash_list += query_result
            page += 1
        else:
            break
    if hash_only:
        return [tx_hash['tx_hash'] for tx_hash in tx_hash_list]
    return [tx_hash for tx_hash in tx_hash_list]


def get_utxo_list_by_tx_hash(tx_hash: str) -> List[dict]:
    """Get a list of UTXO of a tx_hash."""
    return query(f"""/txs/{tx_hash}/utxos""").json()


def get_tx_by_tx_hash(tx_hash: str) -> dict:
    """Get transaction of a tx_hash."""    
    return query(f"""/txs/{tx_hash}""").json()


def get_address_by_adahandle(adahandle: str) -> str:
    """Get the Cardano address of an adahandle, see https://docs.adahandle.com/."""
    if not valid_address(adahandle):
        adahandle = adahandle.strip('$')
        adahandle_policyID = "f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a"
        asset = f"""{adahandle_policyID}{binascii.hexlify(bytes(adahandle, 'utf-8')).decode('utf-8')}"""
        adahandle = get_address_by_asset(asset)
    return adahandle