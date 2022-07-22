from discord.ext import commands, tasks
import puurrtybot.twitter.twitter_functions as ttf
import datetime, requests, puurrtybot, os, time
import puurrtybot.functions as pf


class SalesTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('SalesTracker running')
        market_last_100 = requests.get("""https://server.jpgstoreapis.com/collection/f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e/transactions?page=1&count=50""").json()
        buy_path = puurrtybot.PATH/"puurrtybot/databases/market_buys"
        past_buys = os.listdir(buy_path)


        for move in market_last_100['transactions'][::-1]:
            if move['tx_hash'] not in past_buys:
                if move['action'] in ['BUY','ACCEPT_OFFER'] and move['confirmed_at']:
                    timestamp = int(pf.time_to_timestamp(move['confirmed_at'].replace('T',' ').split('+',1)[0].split('.',1)[0]))
                    if timestamp - pf.get_utc_time() + 1*60*60 > 0:
                        ada = move['amount_lovelace']/1_000_000
                        asset = move['asset_id']
                        meta_name = move['display_name']
                        with open(f"""{buy_path}/{move['tx_hash']}""", 'w') as f:
                            f.write('')
                        #await channel.send(f"""{meta_name} sold for {ada}₳ at <t:{timestamp}:f>.""")
                        content=f"""{meta_name} just sold for {ada}₳!"""
                        tweet_id = ttf.tweet_sale(content, asset)
                        await self.channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
                        print("sent sale tweet")
                        time.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999002600013836340)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(SalesTracker(client))