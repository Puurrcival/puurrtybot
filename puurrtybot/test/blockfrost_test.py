# Testing blockfrost api

import puurrtybot.api.blockfrostio as blockfrostio
from puurrtybot import POLICY_PCS

ADAHANDLE = "$puurrcival"
ADDRESS = "addr1qyqggc5f3dgyx6ulwl4uqf8gucxvdahgpatjx27hutsusg79nee6glazchetycv3uewpraf7tfe60t3kud5l0cdkl5wqyj5xhy"
STAKE_ADDRESS = "stake1u8zeuuay073vtu4jvxg7vhq375l95ua84cmwx60huxm068qc9h6ee"
ASSET = "f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e50757272426f74"
TX_HASH = "883d35e57d023e09523f129af4abb00fd6db2b43629f9a1fe695859a07d97e13"

def exists_not(function, arg, status_code=404):
    try:
        function(arg)
    except Exception as e:
        assert status_code == e.args[0][0]


def test_get_server_time():
    assert int == type(blockfrostio.get_server_time())


def test_address_exists():
    # exists
    assert blockfrostio.valid_address(ADDRESS)

    # exists not
    assert not blockfrostio.valid_address("")


def test_get_asset_list_by_policy():
    assert "f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e5a68757a69" == blockfrostio.get_asset_list_by_policy_id(POLICY_PCS, max_pages = 1, order='desc')[0]


def test_get_meta_by_asset():
    # exsists
    assert ASSET == blockfrostio.get_meta_by_asset(ASSET)['asset']

    # exists not
    blockfrostio.get_stake_address_by_address("") is None


def test_get_stake_address_by_address():
    # exists
    assert STAKE_ADDRESS == str(blockfrostio.get_stake_address_by_address(ADDRESS))

    # exists not
    blockfrostio.get_stake_address_by_address("") is None


def test_get_address_list_by_stake_address():
    # exists
    assert ADDRESS in blockfrostio.get_address_list_by_stake_address(STAKE_ADDRESS)

    # exists not
    exists_not(blockfrostio.get_address_list_by_stake_address, "", 400)


def test_get_tx_hash_list_by_address():
    # exists
    assert TX_HASH == blockfrostio.get_tx_hash_list_by_address(ADDRESS, past_time = 999_999_999, order = "asc")[0]

    # exists not

def test_get_utxo_list_by_tx_hash():
    # exists
    assert TX_HASH == blockfrostio.get_utxo_list_by_tx_hash(TX_HASH)['hash']

    # exists not
    exists_not(blockfrostio.get_utxo_list_by_tx_hash, "", 404)


def test_get_tx_by_tx_hash():
    # exists
    assert TX_HASH == blockfrostio.get_tx_by_tx_hash(TX_HASH)['hash']

    # exists not
    exists_not(blockfrostio.get_tx_by_tx_hash, "", 404)


def test_get_address_by_adahandle():
    # exists
    assert ADDRESS == blockfrostio.get_address_by_adahandle("$puurrcival")

    # exists not
    exists_not(blockfrostio.get_address_by_adahandle, "$012345678901234567890", 404)