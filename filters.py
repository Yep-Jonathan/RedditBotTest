
def ByName(name):
    def f(item):
        return item["cardName"].upper() == name.upper()
    return f

SetAliases = {
    "GENETIC APEX": "A1",
    "GA": "A1",
    "MYTHICAL ISLAND": "A1a",
    "MI": "A1a",

    "SPACE TIME SMACKDOWN": "A2",
    "STS": "A2",
    "TRIUMPHANT LIGHT": "A2a",
    "TL": "A2a",
    "SHINING REVELRY": "A2b",
    "SR": "A2b",

    "CELESTIAL GUARDIANS": "A3",
    "CG": "A3",
    "EXTRADIMENSIONAL CRISIS": "A3a",
    "EC": "A3a",
    "EEVEE GROVE": "A3b",
    "EG": "A3b",
}
def BySet(setName):
    def f(item):
        s = setName.upper()
        if s in SetAliases:
            s = SetAliases[s]
        return item["setName"].upper() == s
    return f

def ByCardNumber(num):
    def f(item):
        return int(item["cardNumber"]) == int(num)
    return f

typeAliases = {
    "G": "{G}", "GRASS": "{G}",
    "R": "{R}", "FIRE": "{R}",
    "W": "{W}", "WATER": "{W}",
    "L": "{L}", "LIGHTNING": "{L}",
    "P": "{P}", "PSYCHIC": "{P}",
    "F": "{F}", "FIGHTING": "{F}",
    "D": "{D}", "DARKNESS": "{D}",
    "M": "{M}", "METAL": "{M}",
    "Y": "{Y}", "FAIRY": "{Y}",
    "N": "{N}", "DRAGON": "{N}",
    "C": "{C}", "COLORLESS": "{C}",
}
def ByType(typeName):
    def f(item):
        t = typeName.upper()
        if t in typeAliases:
            t = typeAliases[t]
        return item["type"].upper() == t
    return f

def DiamondRarity():
    """
    Only include diamond rarity
    """
    def f(item):
        rarity = item["rarity"]
        return rarity.startswith("\u25c7")
    return f

def Promo():
    """
    Only include Promo cards
    """
    def f(item):
        rarity = item["rarity"]
        return rarity.startswith("Promo")
    return f
