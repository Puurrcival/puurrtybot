from discord.ext import commands, tasks
import puurrtybot, requests, os, time

headers = {"Authorization": "Bearer {}".format(puurrtybot.TWITTER_BEARER_TOKEN)}
url =f"""https://api.twitter.com/2/users/1479912806866694149/mentions?tweet.fields=in_reply_to_user_id,author_id"""

class TwitterTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('TwitterTracker running')
        r = requests.request("GET", url, headers=headers).json()

        buy_path = puurrtybot.PATH/"puurrtybot/databases/twitter_mentions"
        past_buys = os.listdir(buy_path)


        for tweet in r['data'][::-1]:
            try:
                tweet['in_reply_to_user_id']
            except KeyError:
                if tweet['id'] not in past_buys:
                    author = tweet['author_id']
                    
                    await self.channel.send(f"""https://twitter.com/{author}/status/{tweet['id']}""")
                    with open(f"""{buy_path}/{tweet['id']}""", 'w') as f:
                        f.write('')

                    print("tracked tweet")
                    time.sleep(5)
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999043361983955116)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(TwitterTracker(client))