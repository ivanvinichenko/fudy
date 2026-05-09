import pytest

@pytest.fixture
def user():
    user_data = {
        "tg_id":777,
        "name":"Test",
        "last_name": "User",
        "gender": "male",
        "age": 27,
        "height": 180,
        "weight": 70,
        "goal_weight": 75,
       "goal": "Набор веса",
        "activity_level": "Средний",
        "body_type": "Мезоморф",
        "allergies": "нет",
    }
    return user_data

@pytest.fixture
def entry_data():
    entry_data = {
        'user_id':777,
        'date': '2026-05-06',
        'meal_type': 'breakfast_entry',
        'products': 'products',
        'analysis': 'analysis',
    }
    return entry_data