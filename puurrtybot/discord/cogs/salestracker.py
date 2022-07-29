from discord.ext import commands, tasks
import time, puurrtybot.twitter.twitter_functions as ttf, puurrtybot.markets.market_queries as mmq, puurrtybot, datetime
import puurrtybot.assets.get_functions as agf


class SalesTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('SalesTracker running')
        new_sales = mmq.get_untracked_sales_jpgstore()

        for sale in new_sales:
            display_name = puurrtybot.ASSETS[sale['asset']]['onchain_metadata']['name']

            asset_sales_history = agf.get_asset_sale_history(sale['asset'])
            print(asset_sales_history)
            if asset_sales_history['bought']:
                bought_mint = "🛒 Seller bought"
                bought_time = datetime.datetime.utcfromtimestamp(asset_sales_history['bought_time'])
            else:
                asset_sales_history['bought'] = puurrtybot.ASSETS[sale['asset']]['mint_price']
                bought_mint = "⚒️ Seller minted"
                bought_time = datetime.datetime.utcfromtimestamp(puurrtybot.ASSETS[sale['asset']]['mint_time'])

            diff = asset_sales_history['last'] - asset_sales_history['bought']

            last_time = datetime.datetime.utcfromtimestamp(asset_sales_history['last_time'])
            hodl = last_time - bought_time
            hours, minutes, _ = str(datetime.timedelta(seconds=hodl.seconds)).split(':')

            if int(hodl.days) != 0:
                days = f"""{hodl.days} days, """
            else:
                days = ""
            if int(hours) != 0:
                hours = f"""{int(hours)} hours and """
            else:
                hours = ""   
            diff = asset_sales_history['last'] - asset_sales_history['bought']
            if asset_sales_history['bought'] == 0:
                profit = f"""🎁 Seller took a profit of {diff}₳."""
            else:
                percentage = 100/asset_sales_history['bought']*asset_sales_history['last']
                if diff  < 0:
                    profit = f"""📉 Seller took a loss of {diff}₳ (-{round(100-percentage, 2)}%)."""
                else:
                    profit = f"""📈 Seller took a profit of {diff}₳ ({round(percentage-100, 2)}%)."""

            bought_string = f"""\n\n{bought_mint} for {asset_sales_history['bought']}₳."""
            hodl_string = f"""\n💰 Seller hodl for {days}{hours}{int(minutes)} minutes."""
            content_detail = f"""{bought_string}{hodl_string}\n{profit}\n"""

            content=f"""🐱 {display_name} just sold for {sale['amount']}₳!{content_detail}"""
            print(content)
            tweet_id = ttf.tweet_sale(content, sale['asset'])
            await self.channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
            print("sent sale tweet")
            time.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999002600013836340)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(SalesTracker(client))