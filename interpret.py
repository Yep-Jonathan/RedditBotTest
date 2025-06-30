"""
Interpret the match found and apply the associated filters
"""
import filters

def Interpret(match: str, cardList: list) -> list:
    tokens = match.split("+")

    try:
        returnList = cardList
        for token in tokens:
            token = token.strip(" ")
            if token.find("=") == -1:  # not using key=value syntax
                returnList = filter(filters.ByName(token), returnList)
                continue

            key, value = token.split("=", 1)
            key = key.strip(" ")
            value = value.strip(" ")

            match key.lower():
                case "set" | "pack" | "s":
                    returnList = filter(filters.BySet(value), returnList)
                case "#" | "number" | "num":
                    returnList = filter(filters.ByCardNumber(int(value)), returnList)
                case "type" | "t":
                    returnList = filter(filters.ByType(value), returnList)
                case "name":
                    returnList = filter(filters.ByName(value), returnList)
                case _:
                    raise NotImplementedError(f"Unable to interpret key {key} with value {value}")
            
        return list(returnList)

    except Exception as e:
        print(f"Unable to interpret match {match}: {e}")
        return []

    