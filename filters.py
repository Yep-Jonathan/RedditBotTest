
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
    "GRASS": "{G}",
    "FIRE": "{R}",
    "WATER": "{W}",
    "LIGHTNING": "{L}",
    "PSYCHIC": "{P}",
    "FIGHTING": "{F}",
    "DARKNESS": "{D}",
    "METAL": "{M}",
    "FAIRY": "{Y}",
    "DRAGON": "{N}",
    "COLORLESS": "{C}",
}
def ByType(typeName):
    def f(item):
        t = typeName.upper()
        if t in typeAliases:
            t = typeAliases[t]
        return item["type"].upper() == t
    return f
