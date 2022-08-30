"""A module that creates a profile for an asset."""
from dataclasses import dataclass
from typing import List, Tuple
from io import BytesIO

import pandas as pd
import matplotlib, matplotlib.pyplot as plt
from discord import Embed, File

from puurrtybot.database.create import Sale, User
from puurrtybot.database import query as dq
from puurrtybot.helper.functions import timestamp_to_formatted_date
from puurrtybot.helper import image_handle as im

matplotlib.style.use('ggplot')
plt.style.use('seaborn-dark-palette')


@dataclass
class AssetProfile:
    asset_id: str = None
    asset_name: str = None
    mint_time: int = None
    mint_price: int = None
    amount_traded: int = None
    sale_history: List[Sale] = None
    sale_lowest: int = None
    sale_highest: int = None
    sale_volume: int = None

    @property
    def sale_plot(self) -> BytesIO:
        return get_asset_sale_history_plot(self.sale_history) if self.sale_history else None

    @property
    def asset_img(self) -> BytesIO:
        return im.get_asset_image(self.asset_id)

    @property
    def owner(self) -> User:
        return dq.get_user_by_asset_id(self.asset_id)

    @property
    def owner_name(self) -> User:
        owner = dq.get_user_by_asset_id(self.asset_id)
        return owner.username if owner else 'Unknown'

    @property
    def embed(self) -> Tuple[Embed, List[File]]:
        return create_embed(self)    

    @property
    def embed_short(self) -> Tuple[Embed, List[File]]:
        return create_embed(self, saleplot=False)

    def __post_init__(self):
        asset_data = dq.get_asset_by_asset_id(self.asset_id)
        self.sale_history = sale_history = dq.get_sale_history(self.asset_id)
        sale_history = [sale.amount_lovelace/1_000_000 for sale in sale_history]
        self.asset_name = asset_data.name
        self.mint_time = asset_data.mint_time
        self.mint_price = asset_data.mint_price/1_000_000
        self.amount_traded = len(sale_history)
        self.sale_lowest = min(sale_history) if sale_history else None
        self.sale_highest = max(sale_history) if sale_history else None
        self.sale_volume = sum(sale_history)


def get_asset_sale_history_plot(sale_history: List[Sale]) -> BytesIO:
    df = pd.DataFrame([(sale.amount_lovelace/1_000_000, timestamp_to_formatted_date(sale.confirmed_at)) for sale in sale_history], columns=['sale','time'])
    df = df.set_index('time')
    ax = df.plot(style='.-' , yticks=[i*100 for i in range(max(int(df['sale'].min()/100)-2,0),int(df['sale'].max()/100)+2)],alpha=0.75, rot=0, legend=False, markersize=20,  markerfacecolor='darkblue')
    ax.set(xlabel="", ylabel="")
    for idx, row in enumerate(df.iterrows()): 
        d = row[0]
        value = row[1][0]
        ax.get_figure().patch.set_alpha(0)
        ax.annotate(value, (idx, value), xytext=(-10, -20), textcoords='offset points',color='darkblue')

    stream = BytesIO()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.get_figure().patch.set_alpha(0)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(stream, format='png')
    stream.seek(0)
    return stream


def create_embed(asset: AssetProfile, saleplot: bool = True) -> Tuple[Embed, List[File]]:
        image_files: List[File] = []
        embed: Embed = Embed(  title=f"""**{asset.asset_name}**""",
                        url=f"""https://www.jpg.store/asset/{asset.asset_id}""",
                        description="",
                        color=0x109319)

        image_files.append(File(asset.asset_img, filename="thumbnail.png"))
        embed.set_thumbnail(url=f"""attachment://thumbnail.png""")
        embed.add_field(name=f"""Owner""", value=f"""{asset.owner_name}""" )
        embed.add_field(name=f"""Minted""", value=f"""For {asset.mint_price}₳ on {timestamp_to_formatted_date(asset.mint_time)}.""", inline=False)
        embed.add_field(name=f"""Times traded""", value=f"""{asset.amount_traded}""", inline=False) 
        embed.add_field(name="Lowest", value=f"""{asset.sale_lowest} ₳""", inline=True)
        embed.add_field(name="Highest", value=f"""{asset.sale_highest} ₳""", inline=True)
        embed.add_field(name="Volume", value=f"""{asset.sale_volume} ₳""", inline=True)
        embed.set_footer(text="")
        if saleplot and asset.amount_traded > 1:
            image_files.append(File(asset.sale_plot, filename="sale_plot.png"))
            embed.add_field(name=f"""\u200b""", value=f"""**Sale History**""", inline=False) 
            embed.set_image(url="attachment://sale_plot.png")

        return (embed, image_files)