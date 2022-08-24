from puurrtybot.pcs import metadata
import puurrtybot.databases.database_queries as ddq


class PuurrtyCat():
    def __init__(self, asset_id) -> None:
        asset = self.asset = ddq.get_asset_by_id(asset_id)
        self.background = metadata.Background(str(asset.background))
        self.eyes = metadata.Eyes(asset.eyes)
        self.fur = metadata.Fur(asset.fur)
        self.hands = metadata.Hands(asset.hands)
        self.hat = metadata.Hat(asset.hat)
        self.mask = metadata.Mask(asset.mask)
        self.mouth = metadata.Mouth(asset.mouth)
        self.outfit = metadata.Outfit(asset.outfit)
        self.tail = metadata.Tail(asset.tail)
        self.wings = metadata.Wings(asset.wings)

        self.prefix = metadata.Prefix(asset.prefix_name)
        self.firstname = metadata.Prefix(asset.first_name)
        self.lastname = metadata.Prefix(asset.last_name)
        self.suffix = metadata.Suffix(asset.suffix_name)
cat = PuurrtyCat("f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e4d724c656f6e617264")

print(cat.background)