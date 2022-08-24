from discord.ext import commands, tasks
import time, puurrtybot.twitter.twitter_functions as ttf
import datetime
import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi
from puurrtybot.api import jpgstore
from puurrtybot.database.create import Session

class SaleTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('SaleTracker running')
        sales = sorted(jpgstore.get_sales_untracked())
        confirmed_sales = [sale for sale in sales if sale.action in ['BUY','ACCEPT_OFFER'] and sale.confirmed_at]
        confirmed_sales.sort(key=lambda x: x.confirmed_at, reverse=True)

        for sale in confirmed_sales:        
            Session.add(sale)
            Session.commit()
            asset = ddq.get_asset_by_id(sale.asset_id)
            display_name = asset.name
            asset.sales.sort(key=lambda x: x.confirmed_at, reverse=False)
            sales_history = [sale for sale in asset.sales if sale.tracked]

            if not sales_history:
                bought = asset.mint_price
                bought_mint = "⚒️ Seller minted"
                bought_time = datetime.datetime.utcfromtimestamp(asset.mint_time)
            else:
                bought = sales_history[-1].amount_lovelace
                bought_mint = "🛒 Seller bought"
                bought_time = datetime.datetime.utcfromtimestamp(sales_history[-1].confirmed_at)
            diff = sale.amount_lovelace - bought
            last_time = datetime.datetime.utcfromtimestamp(sale.confirmed_at)
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
                
            
            diff = diff/1_000_000
            bought = bought/1_000_000
            saleamount = sale.amount_lovelace/1_000_000
            if bought != 0:
                percentage = 100/bought*saleamount
                if diff  < 0:
                    profit = f"""📉 Seller took a loss of {diff}₳ (-{round(100-percentage, 2)}%)."""
                else:
                    profit = f"""📈 Seller took a profit of {diff}₳ ({round(percentage-100, 2)}%)."""
            else:
                profit = f"""📈 Seller took a profit of {diff}₳."""
                
            bought_string = f"""\n\n{bought_mint} for {bought}₳."""
            hodl_string = f"""\n💰 Seller hodl for {days}{hours}{int(minutes)} minutes."""
            content_detail = f"""{bought_string}{hodl_string}\n{profit}\n"""

            content=f"""🐱 {display_name} just sold for {saleamount}₳!{content_detail}"""
            tweet_id = ttf.tweet_sale(content, sale.asset_id)
            ddi.sale_tracked(sale.tx_hash)
            await self.channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
            print("sent sale tweet")
            time.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999002600013836340)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(SaleTracker(client))