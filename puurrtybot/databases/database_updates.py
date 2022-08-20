import tqdm
import puurrtybot.databases.database_queries as ddq
import puurrtybot.api.blockfrost as bbq
import puurrtybot.databases.database_inserts as ddi


def update_asset_address_all():
    for asset_id in tqdm.tqdm([asset.asset_id for asset in ddq.get_asset_all()]):
        address = bbq.get_address_by_asset(asset_id)
        ddi.asset_change_address(asset_id, address)