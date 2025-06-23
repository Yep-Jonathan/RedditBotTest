import filters
import json
import pytest


@pytest.fixture
def cardList():
    with open("data/testCardList.json", "r", encoding="utf_16") as f:
         cardList = json.load(f)
    yield cardList

def test_name_bulbasaur(cardList):
    bulbasaurCards = filter(filters.ByName("Bulbasaur"), cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 4
    for c in cards:
        assert c["cardName"] == "Bulbasaur"

def test_name_capitalization(cardList):
    bulbasaurCards = filter(filters.ByName("BuLbAsAuR"), cardList)
    assert len(list(bulbasaurCards)) == 4

def test_name_ex(cardList):
    charizardEXCards = filter(filters.ByName("Charizard ex"), cardList)
    assert len(list(charizardEXCards)) == 7

def test_name_pokeball(cardList):
    pokeball = filter(filters.ByName("Poke Ball"), cardList)
    assert len(list(pokeball)) == 2

def test_bad_name(cardList):
    abcCards = filter(filters.ByName("abc"), cardList)
    assert len(list(abcCards)) == 0

def test_bad_characters(cardList):
    cards = filter(filters.ByName("!@#$%^&*()"), cardList)
    assert len(list(cards)) == 0


def test_set(cardList):
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    cards = list(geneticApexCards)
    assert len(cards) == 286
    for c in cards:
        assert c["setName"] == "A1"

    celestialGuardiansCards = filter(filters.BySet("A3"), cardList)
    cards = list(celestialGuardiansCards)
    assert len(cards) == 239
    for c in cards:
        assert c["setName"] == "A3"

def test_set_aliases(cardList):
    geneticApexCards = filter(filters.BySet("GA"), cardList)
    for c in geneticApexCards:
        assert c["setName"] == "A1"

    geneticApexCards = filter(filters.BySet("genetic apex"), cardList)
    for c in geneticApexCards:
        assert c["setName"] == "A1"

    celestialGuardiansCards = filter(filters.BySet("CG"), cardList)
    for c in celestialGuardiansCards:
        assert c["setName"] == "A3"


def test_number(cardList):
    oneCards = filter(filters.ByCardNumber(1), cardList)
    cards = list(oneCards)
    assert len(cards) == 8
    for c in cards:
        assert int(c["cardNumber"]) == 1

    cards286 = filter(filters.ByCardNumber(286), cardList)
    cards = list(cards286)
    assert len(cards) == 1
    for c in cards:
        assert int(c["cardNumber"]) == 286


def test_type(cardList):
    grassCards = filter(filters.ByType("{G}"), cardList)
    cards = list(grassCards)
    assert len(cards) == 164
    for c in cards:
        assert c["type"] == "{G}"

    grassCards = filter(filters.ByType("grass"), cardList)
    cards = list(grassCards)
    assert len(cards) == 164
    for c in cards:
        assert c["type"] == "{G}"

def test_supporter(cardList):
    supporterCards = filter(filters.ByType("Supporter"), cardList)
    cards = list(supporterCards)
    assert len(cards) == 75
    for c in cards:
        assert c["type"] == "Supporter"


def test_multiple_filters(cardList):    
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    cards = filter(filters.ByCardNumber(1), geneticApexCards)
    c = list(cards)
    assert len(c) == 1
    assert int(c[0]["cardNumber"]) == 1
    assert c[0]["setName"] == "A1"

    celestialGuardiansCards = filter(filters.BySet("A3"), cardList)
    cards = filter(filters.ByCardNumber(286), celestialGuardiansCards)
    assert len(list(cards)) == 0  # no card with this number in this set

def test_transitive_filters(cardList):
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    cards = filter(filters.ByName("Bulbasaur"), geneticApexCards)
    for c in cards:
        assert c["setName"] == "A1"
        assert c["cardName"] == "Bulbasaur"

    bulbasaurCards = filter(filters.ByName("Bulbasaur"), cardList)
    cards = filter(filters.BySet("A1"), bulbasaurCards)
    for c in cards:
        assert c["setName"] == "A1"
        assert c["cardName"] == "Bulbasaur"

def test_oricorio(cardList):
    oricorioCards = filter(filters.ByName("Oricorio"), cardList)
    assert len(list(oricorioCards)) == 5

    oricorioCards = filter(filters.ByName("Oricorio"), cardList)
    cards = filter(filters.ByType("fire"), oricorioCards)
    assert len(list(cards)) == 1
