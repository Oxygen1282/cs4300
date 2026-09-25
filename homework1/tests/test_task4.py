"""Task 4: calculate_discount works with any numeric type (duck typing)."""
from decimal import Decimal 
from fractions import Fraction 

import pytest

@pytest.fixture 
def calculate_discount(run_script):
    """Run task4 with dummy input and hand back its function to test directly."""
    return run_script("task4", ["100", "10"])["calculate_discount"]

@pytest.mark.parametrize("price, discount, expected", [
    (100, 10, 90),              # int, int 
    (100.0, 10.0, 90.0),        # float, float
    (100, 12.5, 87.5),          # int, float
    (19.99, 20, 15.992),        # float, int
    (50, 0, 50),                # no discount 
    (50, 100, 0),               # full discount
    (0, 25, 0),                 # free item
])
def test_numeric_types(calculate_discount, price, discount, expected):
    """Duck typing: the function only needs * / and -, so ints, floats and
    mixes of the two all work. approx absorbs float rounding error."""
    assert calculate_discount(price, discount) == pytest.approx(expected)

def test_decimal_and_fraction(calculate_discount):
    """Other number types that 'quack like numbers' work too, and keep
    their own type (Decimal stays Decimal), which shows duck typing."""
    assert calculate_discount(Decimal("100"), Decimal("10")) == Decimal("90")
    assert calculate_discount(Fraction(1), Fraction(50)) == Fraction(1, 2)

@pytest.mark.parametrize("price, discount", [
    ("100", 10),        # string price
    (100, None),        # missing discount
])
def test_non_numeric_rejected(calculate_discount, price, discount):
    """Things that don't behave like numbers should raise TypeError."""
    with pytest.raises(TypeError):
        calculate_discount(price, discount)
        
@pytest.mark.parametrize("price, discount", [
    (-10, 10),      # negative price
    (100, -5),      # negative discount
    (100, 150),     # discount over 100%
])
def test_out_of_range_rejected(calculate_discount, price, discount):
    """Input validation: a price can't be negative and
    a discount must be 0-100, so these should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_discount(price, discount)

def test_script_output_format(run_script, capsys):
    """The script prints the result as dollars with two decimal places."""
    run_script("task4", ["19.99", "20"])
    assert capsys.readouterr().out.strip() == "$15.99"