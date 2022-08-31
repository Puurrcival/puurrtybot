import tqdm

import puurrtybot.api.blockfrostio as blockfrostio
import puurrtybot.database.query as dq

from puurrtybot.database.create import sql_update, User, Asset
from puurrtybot.database.table import Table
import puurrtybot.helper.functions as func


@sql_update
def update_object(sql_object: Table, session = None) -> None:
    session.query(  sql_object.__class__).filter(
                    getattr(sql_object.__class__, sql_object.primary_key) == getattr(sql_object, sql_object.primary_key)
                    ).update(sql_object.dictionary)
 

@sql_update
def delete_object(sql_object: Table, session = None) -> None:
    session.query(
                    sql_object.__class__).filter(
                    getattr(sql_object.__class__, sql_object.primary_key) == getattr(sql_object, sql_object.primary_key)
                    ).delete()


#@sql_update
#def update_twitter_by_user_id(user_id, twitter_id, twitter_handle, session=None):
#    session.query(User).filter(User.user_id == user_id).update({'twitter_id': twitter_id, 'twitter_handle': twitter_handle})


@sql_update
def update_address_by_asset_id(asset_id, address, session=None):
    address_type = blockfrostio.get_address_type(address)
    stake_address = blockfrostio.get_stake_address_by_address(address)
    stake_address_type = blockfrostio.get_address_type(stake_address)
    session.query(Asset).filter(Asset.asset_id == asset_id).update(
        {'address': address,
         'address_type': address_type.name if address_type else None,
         'stake_address': stake_address,
         'stake_address_type': stake_address_type.name if stake_address_type else None,
         'updated_on':func.get_utc_time()})


def update_asset_address_all():
    for asset in tqdm.tqdm(dq.get_asset_all()):
        address = blockfrostio.get_address_by_asset(asset.asset_id)
        update_address_by_asset_id(asset.asset_id, address)