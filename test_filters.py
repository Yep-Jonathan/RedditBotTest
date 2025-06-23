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
    assert len(list(bulbasaurCards)) == 4

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

def test_card_set(cardList):
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    assert len(list(geneticApexCards)) == 286

    celestialGuardiansCards = filter(filters.BySet("A3"), cardList)
    assert len(list(celestialGuardiansCards)) == 239

def test_card_number(cardList):
    cards = filter(filters.ByCardNumber(1), cardList)
    assert len(list(cards)) == 8

    cards = filter(filters.ByCardNumber(286), cardList)
    assert len(list(cards)) == 1

def test_multiple_filters(cardList):    
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    cards = filter(filters.ByCardNumber(1), geneticApexCards)
    assert len(list(cards)) == 1

    celestialGuardiansCards = filter(filters.BySet("A3"), cardList)
    cards = filter(filters.ByCardNumber(286), celestialGuardiansCards)
    assert len(list(cards)) == 0  # no card with this number in this set

def test_transitive_filters(cardList):
    geneticApexCards = filter(filters.BySet("A1"), cardList)
    cards = filter(filters.ByName("Bulbasaur"), geneticApexCards)
    assert len(list(cards)) == 2  # regular and full art cards

    bulbasaurCards = filter(filters.ByName("Bulbasaur"), cardList)
    cards = filter(filters.BySet("A1"), bulbasaurCards)
    assert len(list(cards)) == 2

