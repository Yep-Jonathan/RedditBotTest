import interpret
import json
import pytest

@pytest.fixture
def cardList():
    with open("data/testCardList.json", "r", encoding="utf_16") as f:
         cardList = json.load(f)
    yield cardList

def test_name_only(cardList):
    bulbasaurCards = interpret.Interpret("bulbasaur", cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 4
    for c in cards:
        assert c["cardName"] == "Bulbasaur"

def test_name_specified(cardList):
    bulbasaurCards = interpret.Interpret("name=bulbasaur", cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 4
    for c in cards:
        assert c["cardName"] == "Bulbasaur"

def test_capitalization(cardList):
    bulbasaurCards = interpret.Interpret("NAME=bulbasaur", cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 4
    for c in cards:
        assert c["cardName"] == "Bulbasaur"

def test_name_and_set(cardList):
    bulbasaurCards = interpret.Interpret("Bulbasaur+set=A1", cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 2
    for c in cards:
        assert c["setName"] == "A1"
        assert c["cardName"] == "Bulbasaur"

def test_name_and_number(cardList):
    ivysaurCards = interpret.Interpret("Ivysaur+number=2", cardList)
    cards = list(ivysaurCards)
    assert len(cards) == 1
    assert cards[0]["cardName"] == "Ivysaur"
    assert int(cards[0]["cardNumber"]) == 2

def test_name_and_type(cardList):
    oricorioCards = interpret.Interpret("Oricorio+t=R", cardList)
    cards = list(oricorioCards)
    assert len(cards) == 1
    assert cards[0]["cardName"] == "Oricorio"
    assert cards[0]["type"] == "{R}"

def test_multiple_same(cardList):
    oricorioCards = interpret.Interpret("Oricorio+t=R+type=Fire", cardList)
    cards = list(oricorioCards)
    assert len(cards) == 1
    assert cards[0]["cardName"] == "Oricorio"
    assert cards[0]["type"] == "{R}"

def test_spaces_in_match(cardList):
    bulbasaurCards = interpret.Interpret(" bulbasaur + set = A1", cardList)
    cards = list(bulbasaurCards)
    assert len(cards) == 2
    for c in cards:
        assert c["setName"] == "A1"
        assert c["cardName"] == "Bulbasaur"

    charizardEXCards = interpret.Interpret(" Charizard EX + set = Genetic Apex  ", cardList)
    cards = list(charizardEXCards)
    assert len(cards) == 4
    for c in cards:
        assert c["setName"] == "A1"
        assert c["cardName"] == "Charizard ex"

def test_bad_interpret(cardList):
    cards = interpret.Interpret("bulbasaur + color = green", cardList)
    assert len(list(cards)) == 0
