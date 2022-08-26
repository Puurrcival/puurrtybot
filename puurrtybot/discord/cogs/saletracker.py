import datetime

from discord.ext import commands, tasks
import puurrtybot.twitter.twitter_functions as ttf
import puurrtybot.database.query as dq
from puurrtybot.api import jpgstore
from puurrtybot.pcs import POLICY_ID
from puurrtybot.helper.asset_profile import AssetProfile
from puurrtybot.database.insert import insert_object


class SaleTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('SaleTracker running')
        if not dq.get_sale_by_tx_hash(jpgstore.get_sale_last(POLICY_ID).tx_hash):        
            sales = jpgstore.get_sales_untracked(POLICY_ID)
            confirmed_sales = [sale for sale in sales if sale.action in ['BUY','ACCEPT_OFFER'] and sale.confirmed_at]
            confirmed_sales.sort(key=lambda x: x.confirmed_at, reverse=True)

            for sale in confirmed_sales:        
                ap = AssetProfile(sale.asset_id)
                sales_history = ap.sale_history

                if not sales_history:
                    bought = ap.mint_price
                    bought_mint = "⚒️ Seller minted"
                    bought_time = ap.mint_time
                else:
                    bought = sales_history[-1].amount_lovelace/1_000_000
                    bought_mint = "🛒 Seller bought"
                    bought_time = datetime.datetime.utcfromtimestamp(sales_history[-1].confirmed_at)
                sold = sale.amount_lovelace/1_000_000
                diff = sold - bought
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
                    
                if bought != 0:
                    percentage = 100/bought*sold
                    if diff  < 0:
                        profit = f"""📉 Seller took a loss of {diff}₳ (-{round(100-percentage, 2)}%)."""
                    else:
                        profit = f"""📈 Seller took a profit of {diff}₳ ({round(percentage-100, 2)}%)."""
                else:
                    profit = f"""📈 Seller took a profit of {diff}₳."""
                    
                bought_string = f"""\n\n{bought_mint} for {bought}₳."""
                hodl_string = f"""\n💰 Seller hodl for {days}{hours}{int(minutes)} minutes."""
                content_detail = f"""{bought_string}{hodl_string}\n{profit}\n"""

                content=f"""🐱 {ap.asset_name} just sold for {sold}₳!{content_detail}"""
                tweet_id = ttf.tweet_sale(content, sale.asset_id)
                await self.channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
                insert_object(sale)
                print("sent sale tweet")

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999002600013836340)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(SaleTracker(client))