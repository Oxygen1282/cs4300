"""Task 6: read task6_read_me.txt and count the words in it."""
import re 
import runpy 

import pytest 

from conftest import HOMEWORK_ROOT, SRC 

def count_from_output(output):
    """Pull the number out of "There are N words in that file..."."""
    return int(re.search(r"There are (\d+) words", output).group(1))

def test_real_file_word_count(monkeypatch, capsys):
    """The lorem ipsum file supplied in the assignment has 104 words.
    The script opens the file by a relative path, so the test moves into
    homework1/, where task6_read_me.txt lives."""
    monkeypatch.chdir(HOMEWORK_ROOT)
    runpy.run_path(str(SRC / "task6.py"))
    assert count_from_output(capsys.readouterr().out) == 104


@pytest.mark.parametrize("text, expected", [
    ("one two three\n", 3),         # simple case
    ("one\n", 1),                   # single word
    ("", 0),                                 # empty file
    ("Hello, world.\n", 2),                  # punctuation attached to words
    ("amet , consectetur .\n", 2),           # stray , and . are not words
    ("one two", 2),                          # no newline at end of file
    ("one  two\n", 2),                       # two spaces in a row
    ("line one\n\nline two\n", 4),           # blank line between lines
    ("tab\tseparated\n", 2),                 # tab is whitespace too
])
def test_word_counts(tmp_path, monkeypatch, capsys, text, expected):
    """Run the script against small files whose correct answer is obvious.
    Each writes a temporary task6_read_me.txt (tmp_path is a fresh folder
    per test, so the real file is never touched) and checks the count.
    The later cases are the formatting variations a real file can have."""
    (tmp_path / "task6_read_me.txt").write_text(text)
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(SRC / "task6.py"))
    assert count_from_output(capsys.readouterr().out) == expected 

def test_missing_file(tmp_path, monkeypatch):
    """With no file present, open() raises FileNotFoundError."""
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        runpy.run_path(str(SRC / "task6.py"))