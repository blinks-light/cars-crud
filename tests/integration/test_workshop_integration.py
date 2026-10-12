from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)
    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020

def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)
    
    # 创建两辆车
    first = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    second = database.create_car(
        database_path,
        CarInput(make="Honda", model="Civic", year=2022, color="Black"),
    )
    
    # 只删除第一辆
    database.delete_car(database_path, first.id)
    
    # 断言第一辆查不到
    assert database.get_car(database_path, first.id) is None
    
    # 断言第二辆还在，且列表里只有第二辆
    loaded_second = database.get_car(database_path, second.id)
    assert loaded_second is not None
    assert loaded_second.id == second.id
    
    cars = database.list_cars(database_path)
    assert len(cars) == 1
    assert cars[0].id == second.id