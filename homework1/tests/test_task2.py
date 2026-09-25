"""Task 2: integers, floats, strings and booleans behave as expected."""
import pytest

@pytest.fixture
def task2(run_script, capsys):
    """Run task2 once per test; return (its variables, the lines it printed)."""
    variables = run_script("task2")
    return variables, capsys.readouterr().out.splitlines()

@pytest.mark.parametrize("name, expected_type", [
    ("int1", int), ("int2", int),
    ("float1", float), ("float2", float),
    ("string", str), ("new_string", str),
    ("boolian", bool),
])
def test_variable_types(task2, name, expected_type):
    """Each variable holds the data type it is meant to demonstrate.
 
    type(...) is used rather than isinstance because bool is a subclass
    of int, so isinstance(True, int) would pass and hide a mistake.
    """
    variables, _ = task2
    assert type(variables[name]) is expected_type

def test_integer_addition(task2):
    """int + int stays an int: 7 + 8 prints "15", not "15.0"."""
    _, lines = task2 
    assert lines[0] == "15"

@pytest.mark.parametrize("line_index, expected", [
    (1, pytest.approx(24.9)),   # float + float
    (2, pytest.approx(18.0)),   # float + int is a float
])

def test_float_arithmetic(task2, line_index, expected):
    """Float results are compared with approx because 10.0 + 14.9 is not
    exactly 24.9 in binary floating point; an exact == could fail on a
    correct program."""
    _, lines = task2
    assert float(lines[line_index]) == expected 

def test_int_plus_float_prints_as_float(task2):
    """Mixing int and float produces a float, so Python prints "18.0"."""
    _, lines = task2
    assert lines[2] == "18.0"

def test_string_and_slice(task2):
    """The string prints unchanged, and "String"[1:4] is indices 1, 2, 3:
    "tri". The end index of a slice is excluded."""
    _, lines = task2
    assert lines[3] == "String"
    assert lines[4] == "tri"

def test_boolean_controls_flow(task2):
    """The first if runs while boolian is True; after it is set to False
    the second if must be skipped, so its message never appears."""
    variables, lines = task2
    assert "String7" in lines
    assert "This shouldn't print" not in lines 
    assert variables["boolian"] is False 

def test_string_concatenation_with_float(task2):
    """str() is needed to join a float to a string: "tri" + "14.9"."""
    _, lines = task2 
    assert lines[-1] == "tri14.9"