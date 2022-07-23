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
            if asset_sales_history['bought']:
                diff = asset_sales_history['last'] - asset_sales_history['bought']
                
                last_time = datetime.datetime.utcfromtimestamp(asset_sales_history['last_time'])
                bought_time = datetime.datetime.utcfromtimestamp(asset_sales_history['bought_time'])
                hodl = last_time - bought_time
                minutes, seconds, _ = str(datetime.timedelta(seconds=hodl.seconds)).split(':')

                if int(hodl.days) != 0:
                    days = f"""{hodl.days} days, """
                else:
                    days = ""
                if int(minutes) != 0:
                    minutes = f"""{minutes} minutes and """
                else:
                    minutes = ""   
                diff = asset_sales_history['last'] - asset_sales_history['bought']
                percentage = 100/asset_sales_history['bought']*asset_sales_history['last']
                if diff  < 0:
                    profit = f"""📉 Seller took a loss of {diff}₳ (-{round(100-percentage, 2)}%)."""
                else:
                    profit = f"""📈 Seller took a profit of {diff}₳ ({round(percentage-100, 2)}%)."""

                bought_string = f"""\n\n🛒 Seller bought for {asset_sales_history['bought']}₳."""
                hodl_string = f"""\n💰 Seller hodl for {days}{minutes}{seconds} seconds."""
                content_detail = f"""{bought_string}{hodl_string}\n{profit}\n"""
            else:
                content_detail = ""
            content=f"""🐱 {display_name} just sold for {sale['amount']}₳!{content_detail}"""
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