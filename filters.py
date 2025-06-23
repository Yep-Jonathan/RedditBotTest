
def ByName(name):
    def f(item):
        return item["cardName"].upper() == name.upper()
    return f

def BySet(set):
    def f(item):
        return item["setName"].upper() == set.upper()
    return f

def ByCardNumber(num):
    def f(item):
        return int(item["cardNumber"]) == int(num)
    return f
