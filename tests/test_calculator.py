"""
Tests for math functions.
"""
import pytest

from src.exceptions import (
    AdditionError,
    DivisionError,
    MultiplicationError,
    SubstractionError,
)
from src.services.calculator import Calculator


def test_suma_1():
    """
    Test 1 for suma()
    """
    assert Calculator.suma(1, 1) == 2


def test_suma_2():
    """
    Test 2 for suma()
    """
    assert Calculator.suma(-1, -1) == -2


def test_suma_3():
    """
    Test 3 for suma()
    """
    assert Calculator.suma(-1, 1) == 0


def test_suma_4():
    """
    Test 4 for suma()
    """
    assert Calculator.suma(0, 0) == 0


def test_suma_5():
    """
    Test 5 for suma()
    """
    with pytest.raises(AdditionError):
        Calculator.suma("1", 2)
    with pytest.raises(AdditionError):
        Calculator.suma(2, "1")
    with pytest.raises(AdditionError):
        Calculator.suma("1", "2")


def test_resta_1():
    """
    Test 1 for resta()
    """
    assert Calculator.resta(1, 1) == 0


def test_resta_2():
    """
    Test 2 for resta()
    """
    assert Calculator.resta(-1, -1) == 0


def test_resta_3():
    """
    Test 3 for resta()
    """
    assert Calculator.resta(-1, 1) == -2


def test_resta_4():
    """
    Test 4 for resta()
    """
    assert Calculator.resta(0, 0) == 0


def test_resta_5():
    """
    Test 5 for resta()
    """
    with pytest.raises(SubstractionError):
        Calculator.resta("1", 2)
    with pytest.raises(SubstractionError):
        Calculator.resta(2, "1")
    with pytest.raises(SubstractionError):
        Calculator.resta("1", "2")


def test_multiplicacion_1():
    """
    Test 1 for multiplicacion()
    """
    assert Calculator.multiplicacion(0, 0) == 0


def test_multiplicacion_2():
    """
    Test 2 for multiplicacion()
    """
    assert Calculator.multiplicacion(2, 1) == 2


def test_multiplicacion_3():
    """
    Test 3 for multiplicacion()
    """
    assert Calculator.multiplicacion(2, -2) == -4


def test_multiplicacion_4():
    """
    Test 4 for multiplicacion()
    """
    assert Calculator.multiplicacion(-3, -3) == 9


def test_multiplicacion_5():
    """
    Test 5 for multiplicacion()
    """
    with pytest.raises(MultiplicationError):
        Calculator.multiplicacion("1", 2)
    with pytest.raises(MultiplicationError):
        Calculator.multiplicacion(2, "1")
    with pytest.raises(MultiplicationError):
        Calculator.multiplicacion("1", "2")


def test_division_1():
    """
    Test 1 division()
    """
    with pytest.raises(ZeroDivisionError) as excinfo:
        Calculator.division(1, 0)
    assert str(excinfo.value) == "Division by 0 not allowed!"


def test_division_2():
    """
    Test 2 division()
    """
    assert Calculator.division(10, 2) == 5


def test_division_3():
    """
    Test 3 division()
    """
    assert Calculator.division(-4, 2) == -2


def test_division_4():
    """
    Test 4 division()
    """
    assert Calculator.division(-20, -5) == 4


def test_division_5():
    """
    Test 5 for division()
    """
    with pytest.raises(DivisionError):
        Calculator.division("1", 2)
    with pytest.raises(DivisionError):
        Calculator.division(2, "1")
    with pytest.raises(DivisionError):
        Calculator.division("1", "2")
