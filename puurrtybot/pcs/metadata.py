"""A module that maps the metadata from string to enum."""

from enum import Enum

class Trait(Enum):
    @property
    def class_name(self) -> str:
        return self.__class__.__name__.lower()


class Background(Trait):
    NONE = None
    BLUE = 'Blue'
    GREEN = 'Green'
    ORANGE = 'Orange'
    PURPLE = 'Purple'
    RED = 'Red'
    YELLOW = 'Yellow'


class Eyes(Trait):
    NONE = None
    BLUE_EYES = 'Blue Eyes'
    BLUE_AND_YELLOW = 'Blue and Yellow'
    CLOSED = 'Closed'
    CUTE_EYES = 'Cute Eyes'
    DOLLAR_EYES = 'Dollar Eyes'
    EYE_PATCH = 'Eye Patch'
    FIRE_EYES = 'Fire Eyes'
    GLOWING_YELLOW = 'Glowing Yellow'
    GREEN_EYES = 'Green Eyes'
    HIDDEN = 'Hidden'
    LASER_EYES = 'Laser Eyes'
    SCAR_CRYSTAL_EYES = 'Scar Crystal Eye'
    SMALL_PUPILS = 'Small Pupils'
    STAR_GLASSES = 'Star Glasses'
    VERY_ANGRY = 'Very Angry'
    WHITE_EYES = 'White Eyes'
    YELLOW_EYES = 'Yellow Eyes'


class Fur(Trait):
    NONE = None
    BICOLOR = 'Bicolor'
    BLACK = 'Black'
    CRYSTAL = 'Crystal'
    CYBORG = 'Cyborg'
    DARK_GRAY_STRIPED = 'Dark Gray Striped'
    GOLD = 'Gold'
    GRAY_STRIPED = 'Gray Striped'
    ORANGE_STRIPED = 'Orange Striped'
    PINK = 'Pink'
    SIAMESE = 'Siamese'
    SKELETON = 'Skeleton'
    STRIPED = 'Striped'
    TRICOLOR = 'Tricolor'
    WHITE = 'White'
    ZOMBIE = 'Zombie'


class Hands(Trait):
    NONE = None
    BEER = 'Beer'
    CARDANO_COIN = 'Cardano Coin'
    CHICKEN = 'Chicken'
    DARUMA = 'Daruma'
    FISH_BOWL = 'Fish Bowl'
    GAME_BOY = 'Game Boy'
    KNIFE_AND_FORK = 'Knife and Fork'
    MACHETE = 'Machete'
    MILK = 'Milk'
    NERF_GUNS = 'Nerf Guns'
    ONIGIRI = 'Onigiri'
    PIZZA = 'Pizza'
    SKATEBOARD = 'Skateboard'
    TAIYAKI = 'Taiyaki'
    WAND = 'Wand'


class Hat(Trait):
    NONE = None
    BEANIE = 'Beanie'
    CAP = 'Cap'
    CHEF_HAT = 'Chef Hat'
    CROWN = 'Crown'
    DEVIL = 'Devil'
    FIRE_BUCKET = 'Fire Bucket'
    HALO = 'Halo'
    HEADPHONES = 'Headphones'
    PARTY_HAT = 'Party Hat'
    PHARAOH_HEADDRESS = 'Pharaoh Headdress'
    PIRATE_HAT = 'Pirate Hat'
    SOMBRERO = 'Sombrero'
    STRAW_HAT = 'Straw Hat'
    UNICRON_TIARA = 'Unicorn Tiara'
    WIZARD_HAT = 'Wizard Hat'


class Mask(Trait):
    NONE = None
    CLOWN = 'Clown'
    DIVER = 'Diver'
    GROUCHO = 'Groucho'
    JASON = 'Jason'
    KITSUNE = 'Kitsune'


class Mouth(Trait):
    NONE = None
    ANGRY = 'Angry'
    BEARD = 'Beard'
    BUBBLE_GUM = 'Bubble Gum'
    CIGAR = 'Cigar'
    CLOWN = 'Clown'
    DROOLING = 'Drooling'
    FANGS = 'Fangs'
    GAS_MASK = 'Gas Mask'
    GROWLING = 'Growling'
    HAPPY = 'Happy'
    HIDDEN = 'Hidden'
    MUSTACHE = 'Mustache'
    NORMAL = 'Normal'
    SERIOUS = 'Serious'
    SMILING = 'Smiling'
    SNORKEL = 'Snorkel'
    TONGUE_OUT = 'Tongue Out'
    VERY_ANGRY = 'Very Angry'


class Outfit(Trait):
    NONE = None
    CARDANO_TSHIRT = 'Cardano Tshirt'
    CHEF = 'Chef'
    COLLAR = 'Collar'
    HAWAIIAN = 'Hawaiian'
    HAWAIIAN_SHIRT = 'Hawaiian Shirt'
    HOODIE = 'Hoodie'
    LOBSTER_BIB = 'Lobster Bib'
    NEKKID = 'Nekkid'
    PIRATE_JACKET = 'Pirate Jacket'
    ROYAL_CLOAK = 'Royal Cloak'
    SCUBA_SUIT = 'Scuba Suit'
    SUIT = 'Suit'
    WIZARD_ROBE = 'Wizard Robe'


class Tail(Trait):
    NONE = None
    DEVIL_TAIL = 'Devil Tail'


class Wings(Trait):
    NONE = None
    ANGEL_WINGS = 'Angel Wings'


class Unique(Trait):
    NO = None
    YES = 'Yes'


class Prefix_name(Trait):    
    NONE = None
    CHAIRMAN = 'Chairman'
    CHAIRWOMAN = 'Chairwoman'
    DR = 'Dr.'
    KING = 'King'
    LADY = 'Lady'
    LIL_MISS = "Lil' Miss"
    LORD = 'Lord'
    MADAM = 'Madam'
    MR = 'Mr.'
    MRS = 'Mrs.'
    OL = "Ol'"
    PRINCE = 'Prince'
    PRINCESS = 'Princess'
    PROFESSOR = 'Professor'
    QUEEN = 'Queen'
    SIR = 'Sir'
    

class First_name(Trait):
    NONE = None
    ABBY = 'Abby'
    ADA = 'Ada'
    ADAM = 'Adam'
    ALAN = 'Alan'
    ALBERT = 'Albert'
    ALEX = 'Alex'
    AMBER = 'Amber'
    AMELIA = 'Amelia'
    ARCHIE = 'Archie'
    ARIEL = 'Ariel'
    ASHLEY = 'Ashley'
    ASIA = 'Asia'
    ATHENA = 'Athena'
    AUGUSTINE = 'Augustine'
    AUSTIN = 'Austin'
    AUTUMN = 'Autumn'
    AVA = 'Ava'
    BEATRIX = 'Beatrix'
    BELLA = 'Bella'
    BENJI = 'Benji'
    BERNARD = 'Bernard'
    BERT = 'Bert'
    BINGO = 'Bingo'
    BISCUIT = 'Biscuit'
    BLAZE = 'Blaze'
    BOO = 'Boo'
    BOOTS = 'Boots'
    BUZZ = 'Buzz'
    CAESAR = 'Caesar'
    CALI = 'Cali'
    CANDY = 'Candy'
    CARLOS = 'Carlos'
    CASEY = 'Casey'
    CATMAN = 'Catman'
    CHARLES = 'Charles'
    CHESHIRE = 'Cheshire'
    CHLOE = 'Chloe'
    CINNAMON = 'Cinnamon'
    CLEO = 'Cleo'
    CLIFFORD = 'Clifford'
    COCO = 'Coco'
    COLA = 'Cola'
    CUTIE_PIE = 'Cutie Pie'
    CYNTHIA = 'Cynthia'
    DAISY = 'Daisy'
    DAMION = 'Damion'
    DANTE = 'Dante'
    DEEZY = 'Deezy'
    DELLA = 'Della'
    DIEGO = 'Diego'
    DIMITRI = 'Dimitri'
    DOLPH = 'Dolph'
    DUCHESS = 'Duchess'
    EDNA = 'Edna'
    EDSON = 'Edson'
    EGOR = 'Egor'
    ELIZABETH = 'Elizabeth'
    ELLIE = 'Ellie'
    EMERY = 'Emery'
    EMMA = 'Emma'
    ERNIE = 'Ernie'
    ETHEL = 'Ethel'
    EVA = 'Eva'
    FARRAH = 'Farrah'
    FELIX = 'Felix'
    FERNANDO = 'Fernando'
    FIGARO = 'Figaro'
    FIONA = 'Fiona'
    FLUFFY = 'Fluffy'
    GARFIELD = 'Garfield'
    GEORGIE = 'Georgie'
    GERMAINE = 'Germaine'
    GINGER = 'Ginger'
    GIZMO = 'Gizmo'
    GIZZABELLE = 'Gizzabelle'
    GREGORY = 'Gregory'
    HERCULES = 'Hercules'
    HILLARY = 'Hillary'
    ISIS = 'Isis'
    ISRA = 'Isra'
    JAMES = 'James'
    JASMINE = 'Jasmine'
    JELLYBEAN = 'Jellybean'
    JESSE = 'Jesse'
    JIMBO = 'Jimbo'
    JOE = 'Joe'
    JOEY = 'Joey'
    JOY = 'Joy'
    JULIE = 'Julie'
    JUNO = 'Juno'
    KASSY = 'Kassy'
    KIKI = 'Kiki'
    KIMMY = 'Kimmy'
    LARRY = 'Larry'
    LAURIELLE = 'Laurielle'
    LAYLA = 'Layla'
    LEONARD = 'Leonard'
    LIGHTNING = 'Lightning'
    LILLY = 'Lilly'
    LOKI = 'Loki'
    LOLA = 'Lola'
    LOLO = 'Lolo'
    LOU = 'Lou'
    LUCILLE = 'Lucille'
    LUCY = 'Lucy'
    LULU = 'Lulu'
    LUNA = 'Luna'
    MANUEL = 'Manuel'
    MARIA = 'Maria'
    MARSHMALLOW = 'Marshmallow'
    MAXIMUS = 'Maximus'
    MELLOW = 'Mellow'
    MIA = 'Mia'
    MIDNIGHT = 'Midnight'
    MILTON = 'Milton'
    MISTY = 'Misty'
    MOLLY = 'Molly'
    NALA = 'Nala'
    NOODLE = 'Noodle'
    NORA = 'Nora'
    NUGGET = 'Nugget'
    OLIVER = 'Oliver'
    OLIVIA = 'Olivia'
    OREO = 'Oreo'
    PAMELA = 'Pamela'
    PARIS = 'Paris'
    PATRICK = 'Patrick'
    PEANUT = 'Peanut'
    PEARL = 'Pearl'
    PENELOPE = 'Penelope'
    PENNY = 'Penny'
    PETEY = 'Petey'
    PIERRE = 'Pierre'
    PIPPA = 'Pippa'
    POPPY = 'Poppy'
    PRETTY = 'Pretty'
    QUEENIE = 'Queenie'
    RACHELLE = 'Rachelle'
    RAVEN = 'Raven'
    RICARDO = 'Ricardo'
    RONNY = 'Ronny'
    ROSANNE = 'Rosanne'
    ROSEY = 'Rosey'
    SADIE = 'Sadie'
    SALLY = 'Sally'
    SAM = 'Sam'
    SAPPHIRE = 'Sapphire'
    SASHA = 'Sasha'
    SHADOW = 'Shadow'
    SIMBA = 'Simba'
    SIMON = 'Simon'
    SKITTLES = 'Skittles'
    SMOKEY = 'Smokey'
    SNOWBALL = 'Snowball'
    SOFIA = 'Sofia'
    SOLOMON = 'Solomon'
    SOPHIE = 'Sophie'
    SPRINKLES = 'Sprinkles'
    STELLA = 'Stella'
    STEPHAN = 'Stephan'
    SYLVESTER = 'Sylvester'
    TABBY = 'Tabby'
    TEDDY = 'Teddy'
    THANOS = 'Thanos'
    THEODORE = 'Theodore'
    THOR = 'Thor'
    TIGGER = 'Tigger'
    TIMMY = 'Timmy'
    TOMMY = 'Tommy'
    TONY = 'Tony'
    VICTOR = 'Victor'
    WALLACE = 'Wallace'
    WANDA = 'Wanda'
    WEEZEY = 'Weezey'
    WILLOW = 'Willow'
    WINSTON = 'Winston'
    WOJACK = 'Wojack'
    ZIGGY = 'Ziggy'
    ZOE = 'Zoe'


class Last_name(Trait):
    NONE = None
    ABAWI = 'Abawi'
    ADAMS = 'Adams'
    ALVAREZ = 'Alvarez'
    BALDWIN = 'Baldwin'
    BALL = 'Ball'
    BERGER = 'Berger'
    BIGGLESWORTH = 'Bigglesworth'
    BLACK = 'Black'
    BOUTLIER = 'Boutlier'
    CALLAHAN = 'Callahan'
    CAMPBELL = 'Campbell'
    CASTRO = 'Castro'
    CAT = 'Cat'
    CATMAN = 'Catman'
    CHEN = 'Chen'
    CLARK = 'Clark'
    COOPER = 'Cooper'
    DAVIS = 'Davis'
    DEJARDAN = 'DeJardan'
    DENVER = 'Denver'
    DOOLITTLE = 'Doolittle'
    DUPONT = 'DuPont'
    EDWARDS = 'Edwards'
    FEDEROV = 'Federov'
    FERNANDEZ = 'Fernandez'
    FISCHER = 'Fischer'
    GALLAGHER = 'Gallagher'
    GOMEZ = 'Gomez'
    HARDY = 'Hardy'
    HOWARD = 'Howard'
    IDOL = 'Idol'
    IVANOV = 'Ivanov'
    JACKSON = 'Jackson'
    JAMEAL = 'Jameal'
    JEFFERSON = 'Jefferson'
    JOHNSON = 'Johnson'
    JONES = 'Jones'
    KLEIN = 'Klein'
    KOZAK = 'Kozak'
    KOZLOV = 'Kozlov'
    LARDHI = 'Lardhi'
    LEBLANC = 'Leblanc'
    LEE = 'Lee'
    LOPEZ = 'Lopez'
    LUND = 'Lund'
    MACDONALD = 'MacDonald'
    MACINNIS = 'MacInnis'
    MAGEE = 'Magee'
    MAGILLICUTTY = 'Magillicutty'
    MAGOO = 'Magoo'
    MARTIN = 'Martin'
    MARTINEZ = 'Martinez'
    MCGEE = 'McGee'
    MCIVER = 'McIver'
    MCKENZIE = 'McKenzie'
    MILLER = 'Miller'
    MUNCHER = 'Muncher'
    MURPHY = 'Murphy'
    NAKAMOTO = 'Nakamoto'
    NAKAMURA = 'Nakamura'
    OTTO = 'Otto'
    PAPAGEORGIO = 'Papageorgio'
    PEREZ = 'Perez'
    PICKLES = 'Pickles'
    PINKMAN = 'Pinkman'
    POPOV = 'Popov'
    ROBERTSON = 'Robertson'
    RODRIGUEZ = 'Rodriguez'
    ROY = 'Roy'
    SANTOS = 'Santos'
    SAWYER = 'Sawyer'
    SCHMIDT = 'Schmidt'
    SHERWIN = 'Sherwin'
    SMITH = 'Smith'
    SUMMERS = 'Summers'
    SUZUKI = 'Suzuki'
    TANAKA = 'Tanaka'
    THOMPSON = 'Thompson'
    TYSON = 'Tyson'
    WAGNER = 'Wagner'
    WANG = 'Wang'
    WHITE = 'White'
    WILLIAMS = 'Williams'
    WINTERS = 'Winters'
    ZIMMERMAN = 'Zimmerman'


class Suffix_name(Trait):
    NONE = None
    ESQ = 'Esq.'
    PHD = 'Ph.D.'
    MK_IV = 'mk IV'
    THE_FIRST = 'the First'    
    THE_FOURTH = 'the Fourth'
    THE_SECOND = 'the Second'
    THE_THIRD = 'the Third'
    V2 = 'v2'
    V3 = 'v3'


def name_has_part(name, nametype):
    for part in nametype:
        if f""" {part.value} """ in f""" {name} """:
            return part.value
    return None


class Name():
    def __init__(self, name: str) -> None:
        self.name = name
        self.prefix = name_has_part(name, nametype = Prefix_name)
        name = name[len(self.prefix):].strip() if self.prefix else name

        self.suffix = name_has_part(name, nametype = Suffix_name)
        name = name[:-len(self.suffix)].strip() if self.suffix else name

        self.lastname = name_has_part(name[1:], nametype = Last_name)
        name = name[:-len(self.lastname)].strip() if self.lastname else name

        self.firstname = name_has_part(name, nametype = First_name)

        prefix = f"""{self.prefix} """ if self.prefix else ""
        firstname = f"""{self.firstname} """ if self.firstname else ""
        lastname = f"""{self.lastname} """ if self.lastname else ""
        suffix = f"""{self.suffix}""" if self.suffix else ""
        reconstructed_name = f"""{prefix}{firstname}{lastname}{suffix}""".strip()

        if not self.name == reconstructed_name:
            raise ValueError(f"""Reconstructed name <{reconstructed_name}> doesn't match original name <{self.name}>!""")