from puurrtybot.database.create import Asset, Address, Listing, Role, Sale, Tweet, User
from puurrtybot.database import insert, query, update


def test_database():
    ##delete
    update.delete_object(Asset(asset_id='test'))

    test_asset = Asset(asset_id='f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e4a6f6b6572')
    test_asset = query.fetch_row(test_asset)
    assert test_asset is not None
    test_asset.asset_id = 'test'
    assert not query.fetch_row(test_asset)

    # test object exists
    insert.insert_row(test_asset)
    assert query.fetch_row(test_asset) is not None

    assert test_asset == query.fetch_row(test_asset)
 
    # test object doesn't exist
    update.delete_object(test_asset)
    assert not query.fetch_row(test_asset)

#test_database()

""""""
from concurrent.futures import ThreadPoolExecutor
import asyncio

user_id = 1
user = User(user_id)

def temp():
    user = [user for user in query.fetch_table(User) if user.user_id == 642352900357750787][0]
    print(user)
    user.balance = 11111
    print(user)
    update.update_object(user)
    #user = [user for user in query.fetch_table(User) if user.user_id == 642352900357750787][0]
    update.update_object(user)

async def looping():

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(ThreadPoolExecutor(), temp)
    
    user = [user for user in query.fetch_table(User) if user.user_id == 642352900357750787][0]
    print(user)
    
#asyncio.run(looping())

user = query.fetch_row(User(991345811462029392))
update.delete_object(user)