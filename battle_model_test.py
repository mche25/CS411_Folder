import pytest
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal


@pytest.fixture()
def battle_model():
    return BattleModel()

@pytest.fixture
def sample_meal_1():
    return Meal(id=1, meal="meal 1", price=10.0, cuisine="cuisine A", difficulty="HIGH")

@pytest.fixture
def sample_meal_2():
    return Meal(id=2, meal="meal 2", price=15.0, cuisine="cuisine B", difficulty="LOW")

# Test Cases for prep_combatant Method
def test_prep_combatant_valid(battle_model, sample_meal_1):
    battle_model.prep_combatant(sample_meal_1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == "Meal 1"

def test_prep_combatant_full(battle_model, sample_meal_1, sample_meal_2):
    battle_model.prep_combatant(sample_meal_1)
    battle_model.prep_combatant(sample_meal_2)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(Meal(id=3, meal="Meal 3", price=8.0, cuisine="Cuisine 3", difficulty="LOW"))

def test_battle_not_enough_combatants(battle_model, sample_meal_1):
    battle_model.prep_combatant(sample_meal_1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

def test_clear_combatants(battle_model, sample_meal_1, sample_meal_2):
    battle_model.prep_combatant(sample_meal_1)
    battle_model.prep_combatant(sample_meal_2)
    assert len(battle_model.combatants) == 2  
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Expected combatants list to be empty after clearing"

def test_get_combatants(battle_model, sample_meal_1):
    battle_model.prep_combatant(sample_meal_1)
    combatants = battle_model.get_combatants()
    assert combatants == [sample_meal_1]

def test_prep_combatant_duplicate_combatants(battle_model, sample_meal_1):
    battle_model.prep_combatant(sample_meal_1)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal_1)

# Test Cases for battle Method
def test_battle_success(battle_model, sample_meal_1, sample_meal_2):
    sample_meal_1.price = 5.0
    sample_meal_2.price = 20.0
    battle_model.prep_combatant(sample_meal_1)
    battle_model.prep_combatant(sample_meal_2)
    winner_meal = battle_model.battle()
    assert winner_meal == "Meal 2"
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == "Meal 2"

def test_battle_not_enough_combatants(battle_model, sample_meal_1):
    battle_model.prep_combatant(sample_meal_1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

def test_get_battle_score_high_difficulty(battle_model, sample_meal_1):
    score = battle_model.get_battle_score(sample_meal_1)
    expected_score = (sample_meal_1.price * len(sample_meal_1.cuisine)) - 1  
    assert score == expected_score

def test_get_battle_score_low_difficulty(battle_model):
    meal_low_diff = Meal(id=3, meal="Meal 3", price=8.0, cuisine="French", difficulty="LOW")
    score = battle_model.get_battle_score(meal_low_diff)
    expected_score = (meal_low_diff.price * len(meal_low_diff.cuisine)) - 3  
    assert score == expected_score