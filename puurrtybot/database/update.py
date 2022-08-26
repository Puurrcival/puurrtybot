import tqdm

import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.database.query as dq
import puurrtybot.database.insert as di

from puurrtybot.database.create import sql_update, User, Asset
import puurrtybot.helper.functions as func

@sql_update
def update_balance_by_user_id(user_id: int, amount: int, session=None):
    session.query(User).filter(User.user_id == user_id).update({'balance': User.balance + amount})


@sql_update
def update_twitter_by_user_id(user_id, twitter_id, twitter_handle, session=None):
    session.query(User).filter(User.user_id == user_id).update({'twitter_id': twitter_id, 'twitter_handle': twitter_handle})


@sql_update
def update_address_by_asset_id(asset_id, address, session=None):
    address_type = blockfrost.get_address_type(address)
    stake_address = blockfrost.get_stake_address_by_address(address)
    stake_address_type = blockfrost.get_address_type(stake_address)
    session.query(Asset).filter(Asset.asset_id == asset_id).update(
        {'address': address,
         'address_type': address_type.name if address_type else None,
         'stake_address': stake_address,
         'stake_address_type': stake_address_type.name if stake_address_type else None,
         'updated_on':func.get_utc_time()})


def update_asset_address_all():
    for asset_id in tqdm.tqdm([asset.asset_id for asset in dq.get_asset_all()]):
        address = blockfrost.get_address_by_asset(asset_id)
        di.asset_change_address(asset_id, address)