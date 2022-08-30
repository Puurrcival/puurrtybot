from typing import Tuple
from enum import Enum

import puurrtybot.pcs.metadata as md
from puurrtybot.database.create import Role

ID_2_ROLE = {}


class AssetRole(Enum):
    @property
    def requirement(self) -> Tuple[md.Trait, int]:
        return self.value.requirement


class Amount(AssetRole):
    """Discord roles based on amount of assets."""
    PCS_0: Role = Role(role_id=998190425275904000, requirement=(0,0))
    PCS_1: Role = Role(role_id=998571659382505492, requirement=(1,1))
    PCS_2: Role = Role(role_id=1001479213062299709, requirement=(2,4))
    PCS_5: Role = Role(role_id=1001479154555953202, requirement=(5,9))
    PCS_10: Role = Role(role_id=1001479010167038043, requirement=(10,24))
    PCS_25: Role = Role(role_id=1001478933528723506, requirement=(25,49))
    PCS_50: Role = Role(role_id=1001478852020797521, requirement=(50,79))
    PCS_80: Role = Role(role_id=1001478797595517018, requirement=(80,124))
    PCS_125: Role = Role(role_id=1001478314013229208, requirement=(125,174))
    PCS_175: Role = Role(role_id=1001478244752699482, requirement=(175,349))
    PCS_350: Role = Role(role_id=1001478112602763335, requirement=(350,699))
    PCS_700: Role = Role(role_id=1001477747866075216, requirement=(700,7000))


class Family(AssetRole):
    """Discord roles based on family."""
    ANGEL: Role = Role(role_id=1002193337408835605, requirement=(md.Hat.HALO, md.Wings.ANGEL_WINGS,))
    CRYSTAL: Role = Role(role_id=1002193140452692068, requirement=(md.Fur.CRYSTAL,))
    CYBORG: Role = Role(role_id=1002193140452692068, requirement=(md.Fur.CYBORG,))
    DEVIL: Role = Role(role_id=1002193053576085534, requirement=(md.Hat.DEVIL, md.Eyes.FIRE_EYES, md.Tail.DEVIL_TAIL,))
    EDUCATED: Role = Role(role_id=1002563315509248110, requirement=(md.Prefix_name.PROFESSOR, md.Prefix_name.DR, md.Suffix_name.PHD,))
    GOLD: Role = Role(role_id=1002192993589133402, requirement=(md.Fur.GOLD,))
    JASON: Role = Role(role_id=1002192909107482765, requirement=(md.Mask.JASON,))
    KITSUNE: Role = Role(role_id=1001838062667579456, requirement=(md.Mask.KITSUNE,))
    LASER: Role = Role(role_id=1001982288042655825, requirement=(md.Eyes.LASER_EYES,))
    PIRATE: Role = Role(role_id=1002195354051166270, requirement=(md.Hat.PIRATE_HAT, md.Outfit.PIRATE_JACKET))
    ROYAL: Role = Role(role_id=1002192837066117150, requirement=(md.Hat.CROWN, md.Hat.PHARAOH_HEADDRESS, md.Outfit.ROYAL_CLOAK,))
    SKELETON: Role = Role(role_id=1002192551081693226, requirement=(md.Fur.SKELETON,))
    UNIQUE: Role = Role(role_id=1002192667410710639, requirement=(md.Unique.YES,))
    WIZARD: Role = Role(role_id=1001838343216181258, requirement=(md.Hat.WIZARD_HAT, md.Outfit.WIZARD_ROBE, md.Hands.WAND,))
    ZOMBIE: Role = Role(role_id=1001838223263281152, requirement=(md.Fur.ZOMBIE,))


class Trait(AssetRole):
    """Discord roles based on traits."""
    HANDS__CARDANO_COIN: Role = Role(role_id=1003995315935912056, requirement=(md.Hands.CARDANO_COIN,))
    HAT__CROWN: Role = Role(role_id=1003994809385635840, requirement=(md.Hat.CROWN,))
    FUR__CYBORG: Role = Role(role_id=1002948740396634142, requirement=(md.Fur.CYBORG,))
    HAT__DEVIL: Role = Role(role_id=1003995192514330715, requirement=(md.Hat.DEVIL,))
    EYES__FIRE_EYES: Role = Role(role_id=1003995806434603059, requirement=(md.Eyes.FIRE_EYES,))
    MOUTH__GAS_MASK: Role = Role(role_id=1003995087560249464, requirement=(md.Mouth.GAS_MASK,))
    MASK__JASON: Role = Role(role_id=1002939280714371092, requirement=(md.Mask.JASON,))
    MASK__KITSUNE: Role = Role(role_id=1002939378068365362, requirement=(md.Mask.KITSUNE,))
    EYES__LASER_EYES: Role = Role(role_id=1002948874064908401, requirement=(md.Eyes.LASER_EYES,))
    FUR__SKELETON: Role = Role(role_id=1002938967806705775, requirement=(md.Fur.SKELETON,))
    UNIQUE__YES: Role = Role(role_id=1003995578188963901, requirement=(md.Unique.YES,))
    WINGS__ANGEL_WINGS: Role = Role(role_id=1003995148205707314, requirement=(md.Wings.ANGEL_WINGS,))
    FUR__ZOMBIE: Role = Role(role_id=1002939170626482257, requirement=(md.Fur.ZOMBIE,))


class Status(Enum):
    """Discord roles based on status."""
    VERIFIED: Role = Role(role_id=1001480465259175947, requirement=False)


for role_type in [Amount, Family, Trait]:
    ID_2_ROLE.update({e.value.role_id:e for e in role_type})