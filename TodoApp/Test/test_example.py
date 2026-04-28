import pytest

def test_equal_or_not_equal():
    assert 3 == 1
    assert 3 != 2

def test_is_instance():
	assert isinstance('this is a string', str)
	assert not isinstance('10', int)

def test_type():
    assert type(20 is int)
    assert type("World" is not int)

def test_greater_and_less_than():
     assert 7 < 3
     assert 4 < 10

def test_list():
    assert [1, 2, 3] == [1, 2, 3]
    assert 1 in [1, 2, 3]
    assert all([1, 2])
    assert any([0, 1, 2])

class Student:
     def __init__(self, first_name: str, last_name: str, major: str, years: int):
            self.first_name = first_name
            self.last_name = last_name
            self.major = major
            self.years = years
         
        
@pytest.fixture
def default_employee():
     return Student("John", "Doe", "Computer Science", 3) 

def test_person_initialization(default_employee):
    p = default_employee
    assert p.first_name == "John", "First name should be John"
    assert p.last_name == "Doe",  "Last name should be Doe"
    assert p.major == "Computer Science"
    assert p.years == 3