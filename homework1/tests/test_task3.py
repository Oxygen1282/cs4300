"""Task 3: if statement, for loop (primes), while loop (sum 1..100)."""
import pytest

FIRST_10_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

@pytest.mark.parametrize("user_input, expected", [
    ("5", "That number is positive"),
    ("-5", "That number is negative"),
    ("0", "That number is 0"),
    ("0.001", "That number is positive"),   # tiny positive, just above 0
    ("-0.001", "That number is negative"),  # tiny negative, just below 0
    ("-0", "That number is 0")              # -0.0 == 0 in Python
])
def test_sign_check(run_script, capsys, user_input, expected):
    """One case per branch of the if/elif/else, plus edge cases right at
    the boundary. The values near zero catch a mistake like >= vs >."""
    run_script("task3", [user_input])
    assert expected in capsys.readouterr().out

@pytest.mark.parametrize("bad_input", ["abc", "", "1,000", "nan"])
def test_invalid_input_reprompts(run_script, capsys, bad_input):
    """Anything that isn't a real number is rejected and the user is asked
    again. The second answer is valid, so the script finishes normally.
    "nan" matters because float("nan") succeeds but NaN is neither > 0
    nor < 0, so without the check it would be reported as 0."""
    run_script("task3", [bad_input, "5"])
    out = capsys.readouterr().out
    assert out.count("That isn't a number, try again.") == 1
    assert "That number is positive" in out 
    assert "That number is 0" not in out

def test_reprompts_until_valid(run_script, capsys):
    """Several bad answers in a row: one retry message per bad answer, then
    the valid one is used. If the loop stopped asking, the fake input would
    run out and the test would fail."""
    run_script("task3", ["abc", "", "-3"])
    out = capsys.readouterr().out
    assert out.count("That isn't a number, try again.") == 2
    assert "That number is negative" in out

def test_first_ten_primes(run_script):
    """The for loop should find exactly the first 10 primes. Comparing
    the whole list checks the count, the order, and that no composite
    number such as 9, 15 or 25 (odd numbers that look prime) slipped in."""
    variables = run_script("task3", ["1"])
    assert variables["primes"] == FIRST_10_PRIMES

def test_primes_printed(run_script, capsys):
    """The prime list is also printed to the console."""
    run_script("task3", ["1"])
    assert str(FIRST_10_PRIMES) in capsys.readouterr().out 

def test_sum_1_to_100(run_script, capsys):
    """Gauss's formula n(n+1)/2 gives 100*101/2 = 5050, an independent
    check on the while loop. An off-by-one loop would give 4950 or 5151."""
    variables = run_script("task3", ["1"])
    assert variables["total"] == 100 * 101 // 2 == 5050
    assert capsys.readouterr().out.splitlines()[-1] == "5050"