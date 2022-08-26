from dataclasses import dataclass, field
from typing import Union, Tuple
from enum import Enum

from puurrtybot.pcs import metadata

ID_2_ROLE = {}


@dataclass
class Role:
    ix: int = field(init=False)
    role_id: int = None
    user_id: int = None
    requirement: Union[tuple, int, bool] = None
    updated_on: int = None

    def __post_init__(self):
        self.ix = f"""{self.role_id}_{self.user_id}"""


class AssetRole(Enum):
    @property
    def requirement(self) -> Tuple[metadata.Trait, int]:
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
    ANGEL: Role = Role(role_id=1002193337408835605, requirement=(metadata.Hat.HALO, metadata.Wings.ANGEL_WINGS,))
    CRYSTAL: Role = Role(role_id=100219322797525005, requirement=(metadata.Fur.CRYSTAL,))
    CYBORG: Role = Role(role_id=1002193140452692068, requirement=(metadata.Fur.CYBORG,))
    DEVIL: Role = Role(role_id=1002193053576085534, requirement=(metadata.Hat.DEVIL, metadata.Eyes.FIRE_EYES, metadata.Tail.DEVIL_TAIL,))
    EDUCATED: Role = Role(role_id=1002563315509248110, requirement=(metadata.Prefix_name.PROFESSOR, metadata.Prefix_name.DR, metadata.Suffix_name.PHD,))
    GOLD: Role = Role(role_id=1002192993589133402, requirement=(metadata.Fur.GOLD,))
    JASON: Role = Role(role_id=1002192909107482765, requirement=(metadata.Mask.JASON,))
    KITSUNE: Role = Role(role_id=1001838062667579456, requirement=(metadata.Mask.KITSUNE,))
    LASER: Role = Role(role_id=1001982288042655825, requirement=(metadata.Eyes.LASER_EYES,))
    PIRATE: Role = Role(role_id=1002195354051166270, requirement=(metadata.Hat.PIRATE_HAT, metadata.Outfit.PIRATE_JACKET))
    ROYAL: Role = Role(role_id=1002192837066117150, requirement=(metadata.Hat.CROWN, metadata.Hat.PHARAOH_HEADDRESS, metadata.Outfit.ROYAL_CLOAK,))
    SKELETON: Role = Role(role_id=1002192551081693226, requirement=(metadata.Fur.SKELETON,))
    UNIQUE: Role = Role(role_id=1002192667410710639, requirement=(metadata.Unique.YES,))
    WIZARD: Role = Role(role_id=1001838343216181258, requirement=(metadata.Hat.WIZARD_HAT, metadata.Outfit.WIZARD_ROBE, metadata.Hands.WAND,))
    ZOMBIE: Role = Role(role_id=1001838223263281152, requirement=(metadata.Fur.ZOMBIE,))


class Trait(AssetRole):
    """Discord roles based on traits."""
    HANDS__CARDANO_COIN: Role = Role(role_id=1003995315935912056, requirement=(metadata.Hands.CARDANO_COIN,))
    HAT__CROWN: Role = Role(role_id=1003994809385635840, requirement=(metadata.Hat.CROWN,))
    FUR__CYBORG: Role = Role(role_id=1002948740396634142, requirement=(metadata.Fur.CYBORG,))
    HAT__DEVIL: Role = Role(role_id=1003995192514330715, requirement=(metadata.Hat.DEVIL,))
    EYES__FIRE_EYES: Role = Role(role_id=1003995806434603059, requirement=(metadata.Eyes.FIRE_EYES,))
    MOUTH__GAS_MASK: Role = Role(role_id=1003995087560249464, requirement=(metadata.Mouth.GAS_MASK,))
    MASK__JASON: Role = Role(role_id=1002939280714371092, requirement=(metadata.Mask.JASON,))
    MASK__KITSUNE: Role = Role(role_id=1002939378068365362, requirement=(metadata.Mask.KITSUNE,))
    EYES__LASER_EYES: Role = Role(role_id=1002948874064908401, requirement=(metadata.Eyes.LASER_EYES,))
    FUR__SKELETON: Role = Role(role_id=1002938967806705775, requirement=(metadata.Fur.SKELETON,))
    UNIQUE__YES: Role = Role(role_id=1003995578188963901, requirement=(metadata.Unique.YES,))
    WINGS__ANGEL_WINGS: Role = Role(role_id=1003995148205707314, requirement=(metadata.Wings.ANGEL_WINGS,))
    FUR__ZOMBIE: Role = Role(role_id=1002939170626482257, requirement=(metadata.Fur.ZOMBIE,))


for role_type in [Amount, Family, Trait]:
    ID_2_ROLE.update({e.value.role_id:e for e in role_type})