from resources.functions import isfloat, addition, subtraction, multiplication, division, diff, product, div
import pytest

def test_isfloat():
    assert isfloat("cat") == False
    assert isfloat("12c34") == False
    assert isfloat("12.34.5") == False
    assert isfloat("12.3") == True
    assert isfloat(12.3) == True
    assert isfloat("12345") == True
    assert isfloat(12345) == True

def test_addition():
    fn, sn = addition("Easy")
    assert fn < 10, sn < 10
    fn, sn = addition("Normal")
    assert 10 <= fn <= 30, 10 <= sn <= 20
    fn, sn = addition("Hard")
    assert fn <= 100, sn <= 100
    assert addition("") == None
    with pytest.raises(TypeError):
        fn, sn = addition(1)

# Test Subtraction
def test_subtraction():
    fn, sn = subtraction("Easy")
    assert 8 <= fn <= 15, 1 <= sn <= 8
    fn, sn = subtraction("Normal")
    assert 30 <= fn <= 80, 15 <= sn <= 40
    fn, sn = subtraction("Hard")
    assert -50 <= fn <= 100, -50 <= sn <= 100
    assert subtraction("") == None
    with pytest.raises(TypeError):
        fn, sn = subtraction(1)

# Test multiplication
def test_multiplication():
    fn, sn = multiplication("Easy")
    assert fn <= 12, sn <= 12
    fn, sn = multiplication("Normal")
    assert 10 <= fn <= 20, 13 <= sn <= 20
    fn, sn = multiplication("Hard")
    assert -50 <= fn <= 100, -50 <= sn <= 100
    assert multiplication("") == None
    with pytest.raises(TypeError):
        fn, sn = multiplication(1)

# Test division
def test_division():
    fn, sn = division("Easy")
    assert fn <= 12, sn <= 12
    fn, sn = division("Normal")
    assert 10 <= fn <= 20, 13 <= sn <= 20
    fn, sn = division("Hard")
    assert -50 <= fn <= 100, -50 <= sn <= 100
    assert division("") == None
    with pytest.raises(TypeError):
        fn, sn = division(1)

# Test diff
def test_diff():
    assert diff(3, 2) == 1
    assert diff(3, 5) == -2
    assert diff(3, 3) == 0
    with pytest.raises(TypeError):
        diff("cat", "rat")

# Test product
def test_product():
    assert product(5, 11) == 55
    assert product(2, 3, 2) == 12
    assert product() == 1
    assert product(0, 10) == 0
    assert product(-2, 3) == -6
    assert product(-2, -3) == 6
    with pytest.raises(TypeError):
        product("cat", "foo", 3)

# Test div
def test_div():
    assert div(6, 3) == 2
    assert div(2, 2) == 1
    assert div(0, 1) == 0
    with pytest.raises(ZeroDivisionError):
        div(2, 0)
        div(0, 0)
        
    with pytest.raises(TypeError):
        div("foo", "cat")
