ROLES_ACCESS = {
        998185453083705425: "Admin", # Admins
        998186644836470806: "Bot", # Bots
        1001480465259175947: "verified", #verified member 
        }


ROLES_NUMBER_OF_CATS = {
        998190425275904000:   ("Stray Cat", 0), # 0 cats
        998571659382505492:   ("Puurrty Cat", 1), # 1 cat
        1001479213062299709:  ("Puurrty Puurrson", 2), # 2-4 cats
        1001479154555953202:  ("Puurrty Lovuurr", 5), # 5-9 cats
        1001479010167038043:  ("Puurrty Hoarduurr", 10), # 10-24 cats
        1001478933528723506:  ("Puurrty 25+", 25), # 25-49 cats
        1001478852020797521:  ("Puurrty 50+", 50), # 50-79 cats
        1001478797595517018:  ("Puurrty 80+", 80), # 80-124 cats
        1001478314013229208:  ("Puurrty 125+", 125), # 125-174 cats
        1001478244752699482:  ("Puurrty 200+", 175), # 175-349 cats
        1001478112602763335:  ("Puurrty 350+", 350), # 350-699 cats
        1001477747866075216:  ("Puurrty 700+", 700) # 700+ cats
        }


ROLES_NUMBER_OF_CATS_DICT = {v[1]:k for k, v in ROLES_NUMBER_OF_CATS.items()}


ROLES_FAMILY = {
        "Kitsune":  1001838062667579456,
        "Zombie":   1001838223263281152,
        "Wizard":   1001838343216181258,
        "Angel":    1002193337408835605,
        "Crystal":  1002193227975250050,
        "Cyborg":   1002193140452692068,
        "Devil":    1002193053576085534,
        "Gold":     1002192993589133402,
        "Jason":    1002192909107482765,
        "Royal":    1002192837066117150,
        "Unique":   1002192667410710639,
        "Pirate":   1002195354051166270,
        "Skeleton": 1002192551081693226,
        "Laser":    1001982288042655825,
        "Educated": 1002563315509248110,
        }


ROLES_BASED_ON_TRAITS = {
        1003995315935912056: ( ('hands', 'Cardano Coin'), ), # Coin
        1003994809385635840: ( ('hat', 'Crown'), ), # Crown
        1002948740396634142: ( ('fur', 'Cyborg'), ), # Cyborg
        1003995192514330715: ( ('hat', 'Devil'), ), # Devil hat
        1003995806434603059: ( ('eyes', 'Fire Eyes'), ), # Fire Eyes
        1003995087560249464: ( ('mouth', 'Gas Mask'), ), # Gas Mask
        1002939280714371092: ( ('mask', 'Jason'), ), # Jason
        1002939378068365362: ( ('mask', 'Kitsune'), ), # Kitsune
        1002948874064908401: ( ('eyes', 'Laser Eyes'), ), # Laser Eyes
        1002938967806705775: ( ('fur', 'Skeleton'), ), # Skeleton
        1003995578188963901: ( ('unique', 'Yes'), ), # Unique
        1003995148205707314: ( ('wings', 'Angel Wings'), ), # Wings
        1002939170626482257: ( ('fur', 'Zombie'), ), # Zombie
        }


ROLES_BASED_ON_FAMILY = {
        1001838062667579456: ( ('mask', 'Kitsune'), ), 
        1001838223263281152: ( ('fur', 'Zombie'), ),
        1001838343216181258: ( ('hat','Wizard Hat'), 
                               ('outfit','Wizard Robe'),
                               ('hands','Wand') ),
        1002193337408835605: ( ('hat', 'Halo'),
                               ('wings','Angel Wings') ),
        1002193227975250050: ( ('fur', 'Crystal'), ),
        1002193140452692068: ( ('fur', 'Cyborg'), ),
        1002193053576085534: ( ('hat','Devil'),
                               ('eyes','Fire Eyes'),
                               ('tail','Devil Tail') ),
        1002192993589133402: ( ('fur', 'Gold'), ),
        1002192909107482765: ( ('mask', 'Jason'), ),
        1002192837066117150: ( ('hat', 'Pharaoh Headdress'), 
                               ('hat', 'Crown'), 
                               ('outfit', 'Royal Cloak') ),
        1002192667410710639: ( ('unique', 'Yes'), ),
        1002195354051166270: ( ('hat', 'Pirate Hat'), 
                               ('outfit', 'Pirate Jacket') ),
        1002192551081693226: ( ('fur', 'Skeleton'), ),
        1001982288042655825: ( ('eyes', 'Laser Eyes'), ),
        1002563315509248110: ( ('prefix_name', 'Professor'),
                               ('prefix_name', 'Dr.'),
                               ('prefix_name', 'Ph.D.') )
        }   