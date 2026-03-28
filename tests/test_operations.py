import pytest
from app.operations import add, subtract, multiply, divide


# --- add ---

def test_add_positive_numbers():
    assert add(3, 5) == 8

def test_add_negative_numbers():
    assert add(-2, -4) == -6

def test_add_mixed_sign():
    assert add(-3, 7) == 4

def test_add_floats():
    assert add(1.5, 2.5) == pytest.approx(4.0)

def test_add_zero():
    assert add(0, 0) == 0


# --- subtract ---

def test_subtract_positive_numbers():
    assert subtract(10, 4) == 6

def test_subtract_negative_result():
    assert subtract(3, 8) == -5

def test_subtract_negative_numbers():
    assert subtract(-5, -3) == -2

def test_subtract_floats():
    assert subtract(5.5, 2.2) == pytest.approx(3.3)

def test_subtract_same_values():
    assert subtract(7, 7) == 0


# --- multiply ---

def test_multiply_positive_numbers():
    assert multiply(4, 5) == 20

def test_multiply_by_zero():
    assert multiply(9, 0) == 0

def test_multiply_negative_numbers():
    assert multiply(-3, -4) == 12

def test_multiply_mixed_sign():
    assert multiply(-3, 4) == -12

def test_multiply_floats():
    assert multiply(2.5, 4.0) == pytest.approx(10.0)


# --- divide ---

def test_divide_positive_numbers():
    assert divide(10, 2) == 5.0

def test_divide_results_in_float():
    assert divide(7, 2) == pytest.approx(3.5)

def test_divide_negative_numbers():
    assert divide(-9, -3) == pytest.approx(3.0)

def test_divide_mixed_sign():
    assert divide(-6, 3) == pytest.approx(-2.0)

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)

def test_divide_zero_by_number():
    assert divide(0, 5) == 0.0
