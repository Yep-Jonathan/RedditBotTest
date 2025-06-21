import requests
from bs4 import BeautifulSoup
import json

typeFullToShort = {
    "Grass": "{G}",
    "Fire": "{R}",
    "Water": "{W}",
    "Lightning": "{L}",
    "Psychic": "{P}",
    "Fighting": "{F}",
    "Darkness": "{D}",
    "Metal": "{M}",
    "Fairy": "{Y}",
    "Dragon": "{N}",
    "Colorless": "{C}",

    "Item": None,
    "Tool": None,
    "Supporter": None
}

tags = ["Ultra Beast"]

energyImagesToCost = {
    "https://img.game8.co/3994730/6e5546e2fbbc5a029ac79acf2b2b8042.png/show": "{C}",
    "https://img.game8.co/4018721/a654c44596214b3bf38769c180602a16.png/show": "{C}",
    "https://img.game8.co/3346529/3dd07276f0d15aef9ef1b5f294a8c94a.png/show": "{C}",
    "https://img.game8.co/3998538/eea8469456d6b7ea7a2daf2995087d00.png/show": "{C}{C}",
    "https://img.game8.co/3998539/6bb558f97aac02e469e3ddc06e2ac167.png/show": "{C}{C}{C}",
    "https://img.game8.co/3998556/3831ed9a23dbc9db0da4254334165863.png/show": "{C}{C}{C}{C}",

    "https://img.game8.co/4018726/c2d96eaebb6cd06d6a53dfd48da5341c.png/show": "{G}",
    "https://img.game8.co/3998531/579b7f81ac7b52e36dd4e8b52a9d2da8.png/show": "{G}{G}",
    "https://img.game8.co/3998547/6f2e2fc20719ed36055b888e5668154f.png/show": "{G}{G}{G}",

    "https://img.game8.co/4018725/13914d1a973822da2863205cffe8d814.png/show": "{R}",
    "https://img.game8.co/3998529/4dc15c825d92aebf14c56e9b44446d40.png/show": "{R}{R}",
    "https://img.game8.co/3998541/5dd95eb13941387b1e3391cc77ebd8f1.png/show": "{R}{R}{R}",
    "https://img.game8.co/3998560/cdf130028d05a96e36151011d719c20f.png/show": "{R}{R}{R}{R}",

    "https://img.game8.co/4018730/0eaf098686c55dd62893b16d190c80b5.png/show": "{W}",
    "https://img.game8.co/3998530/4a14a9c467c46d9519f549cba836473a.png/show": "{W}{W}",
    "https://img.game8.co/3998542/1a14eac8ad4df81b977a2a4f2c412715.png/show": "{W}{W}{W}",
    "https://img.game8.co/3998562/eef3b0c9b0d89657c214c2c766cb09ce.png/show": "{W}{W}{W}{W}",

    "https://img.game8.co/4018727/9851d3f597a114b1ab6ef669071cda7c.png/show": "{L}",
    "https://img.game8.co/3998534/6767c2a94b389122eacf01822d0c2f13.png/show": "{L}{L}",
    "https://img.game8.co/3998550/4eccdfc9a3c59e37f7f1d9fce4a6c820.png/show": "{L}{L}{L}",

    "https://img.game8.co/4018724/e22e7f39587352fc048b3821da0ceea4.png/show": "{F}",
    "https://img.game8.co/3998533/3d670ee685179925d9480e4430606d55.png/show": "{F}{F}",
    "https://img.game8.co/3998549/17758e528bfc2ed2851f41cf08be5364.png/show": "{F}{F}{F}",

    "https://img.game8.co/4018729/5d54ec566203717af2c7b7a14f69e0d7.png/show": "{P}",
    "https://img.game8.co/3998532/607fbff18ca46869887d48d9bfaf8f66.png/show": "{P}{P}",
    "https://img.game8.co/3998548/dd2f475e76563c0f75d3bca92afe0f5c.png/show": "{P}{P}{P}",

    "https://img.game8.co/4018722/3488b79c0d788fbcb381c92ce97b750d.png/show": "{D}",
    "https://img.game8.co/3998536/889ef61097e8b0df4f4fda2f5b7f63fd.png/show": "{D}{D}",
    "https://img.game8.co/3998552/67131977e498da79d71ec552ea1de716.png/show": "{D}{D}{D}",

    "https://img.game8.co/4018728/fdfe7a7dc4753da40de9c04aa96ccc25.png/show": "{M}",
    "https://img.game8.co/3998535/4453a1960e81de8078fad8d20c8b7d46.png/show": "{M}{M}",
    "https://img.game8.co/3998551/6d21a83daabfc9876b6c9d46ad8dcfbc.png/show": "{M}{M}{M}",


    "https://img.game8.co/3998614/b92af68265b2e7623de5efdf8197a9bf.png/show": "n/a"
}


def getCardsList():
    url = "https://game8.co/games/Pokemon-TCG-Pocket/archives/482685"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    tables = soup.find_all("table")

    table = None
    # the table we want is the only one with a thead
    for t in tables:
        header = t.find("thead")
        if header:
            table = t
            break

    if table is None:
        raise ValueError(f"No card data was found at this url ({url})")

    cards = []
    for row in table.find_next("tbody").find_all("tr"):
        card = {}
        tds = row.find_all("td")

        if len(tds) != 11:
            raise ValueError(f"Unexpected table data. Please review data table at {url}")
        
        card["setName"], card["cardNumber"] = tds[1].text.split(" ")[0], tds[1].text.split(" ")[1]

        card["cardURL"] = tds[2].a.get("href")
        card["cardImageURL"] = tds[2].div.get("data-image-url")
        card["cardName"] = tds[2].text.strip()
        
        card["rarity"] = tds[3].text

        card["typeFull"] = tds[5].img.get("alt").split(" ")[-1]
        card["type"] = typeFullToShort[card["typeFull"]]

        card["hp"] = tds[6].text.strip()
        card["stage"] = tds[7].text.strip()

        if card["type"] is not None:
            try:
                divs = tds[9].find_all("div")
                card["retreatCost"] = energyImagesToCost[divs[0].img.get("data-src")] if divs[0].img.get("data-src") else None

                cardText = tds[9].find_all(string=True)
                abilityIndex = cardText.index('[Ability]') if '[Ability]' in cardText else -1
                if abilityIndex != -1:
                    card["ability"] = f"{cardText[abilityIndex+1].strip("\n").strip(" ")}: {cardText[abilityIndex+2].strip("\n").strip(" ")}"

                attacks = []
                for d in divs[1:]:
                    if d.b.text.strip() in tags:
                        if "tags" not in card:
                            card["tags"] = []
                        card["tags"].append(d.b.text)
                        continue
                    effect = d.next_sibling.next_sibling.next_sibling.strip("\n") or None
                    cost = ''.join(energyImagesToCost[a.get("data-src")] for a in d.find_all("img"))

                    attacks.append({
                        "name": d.b.text,
                        "cost": cost,
                        "effect": effect,
                        "damage": d.next_sibling.strip()
                    })

            except (KeyError, IndexError) as e:
                # TODO: handle error better
                raise LookupError(f"Unable to parse {card["cardName"]} ({card["setName"]}, {card["cardNumber"]})")

            card["attacks"] = attacks
        else:
            card["effect"] = tds[9].text.replace("-", "").strip()

        cards.append(card)

    return cards

if __name__ == "__main__":
    cards = getCardsList()
    print(json.dumps(cards, indent=4))
