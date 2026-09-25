"""Task 5: list of books (with slicing) and a student-ID dictionary."""
import pytest

@pytest.fixture 
def task5(run_script, capsys):
    variables = run_script("task5")
    return variables, capsys.readouterr().out.splitlines()

def test_books_list_structure(task5):
    """The list alternates title, author, so its length must be even
    (every title has an author) and there are len/2 books."""
    books = task5[0]["favorite_books"]
    assert isinstance(books, list)
    assert len(books) % 2 == 0
    assert len(books) // 2 == 10 

def test_first_three_books_slice(task5):
    """[0:6:2] takes indices 0, 2, 4: the first three titles. This checks
    the printed slice matches the list rather than a hard-coded copy."""
    variables, lines = task5 
    books = variables["favorite_books"]
    expected = ["To Kill a Mockingbird", "1984", "The Great Gatsby"]
    assert books[0:6:2] == expected 
    assert lines[0] == str(expected)

def test_student_dictionary(task5):
    """Dictionary lookups return the right name for a given ID."""
    students = task5[0]["students"]
    assert isinstance(students, dict)
    assert len(students) == 5
    assert students["001"] == "David Zark"
    assert students["003"] == "Anne Frank"

def test_student_ids_unique_and_formatted(task5):
    """Every ID is a 3-digit string. Keys are strings (not ints) so the
    leading zeros in "001" are kept."""
    for student_id in task5[0]["students"]:
        assert isinstance(student_id, str)
        assert len(student_id) == 3 and student_id.isdigit()

def test_missing_student_raises_keyerror(task5):
    """Looking up an ID that doesn't exist raises KeyError."""
    with pytest.raises(KeyError):
        task5[0]["students"]["999"]


def test_every_student_printed(task5):
    """One printed line per student, each containing its ID and name."""
    variables, lines = task5
    student_lines = lines[1:]
    assert len(student_lines) == len(variables["students"])
    for (student_id, name), line in zip(variables["students"].items(), student_lines):
        assert student_id in line and name in line 