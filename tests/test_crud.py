import pytest
import pytest_asyncio
from fixtures import *
from database.CRUD import (save_user_data,
                           save_fact_entry,
                           get_user_info_by_tg_id,
                           save_new_weight,is_user_exists)


@pytest.mark.asyncio
async def test_saved_user(user):
    result = await save_user_data(**user)
    assert result is not None
    assert result.tg_id == 777
    assert result.name == "Test"
    assert result.last_name == "User"
    assert result.gender == "male"
    assert result.age == 27
    assert result.height == 180
    assert result.weight_progress[0] == 70
    assert result.goal_weight == 75
    assert result.goal == "Набор веса"
    assert result.activity_level == "Средний"
    assert result.body_type == "Мезоморф"
    assert result.allergies == "нет"

@pytest.mark.asyncio
async def test_entry_food(entry_data):
    result = await save_fact_entry(**entry_data)
    assert result is True

@pytest.mark.asyncio
async def test_get_user_by_id():
    result = await get_user_info_by_tg_id(777)
    assert result.tg_id == 777

@pytest.mark.asyncio
async def test_save_new_weight():
    result1 = await save_new_weight(777, 80)
    result2 = await save_new_weight("777", 80)
    assert result1 is True
    assert result2 is False

@pytest.mark.asyncio
async def test_is_user_exist():
    result1 = await is_user_exists(777)
    result2 = await is_user_exists("777")
    result3 = await is_user_exists(677)
    assert result1.tg_id == 777
    assert result2 is False
    assert result3 is False


