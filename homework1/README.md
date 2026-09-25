# CS 4300 Homework 1

## Setup

From `/coursework`, activate the virtual environment and install the dependencies:

```bash
source hw1_venv/bin/activate
cd cs4300/homework1
python3 -m pip install -r requirements.txt
```

All commands below are run from the `homework1` directory. Task 6 opens
`task6_read_me.txt` by a relative path and task 7 saves its image to the
current folder, so running from anywhere else will not work correctly.

## Running the tasks

```bash
python3 src/task1.py   # prints Hello, World!
python3 src/task2.py   # data types
python3 src/task3.py   # control structures (asks for a number)
python3 src/task4.py   # discount calculator (asks for a price and a discount)
python3 src/task5.py   # lists and dictionaries
python3 src/task6.py   # word count of task6_read_me.txt
python3 src/task7.py   # saves the graph as task7_output.png
```

## Running the tests

```bash
python3 -m pytest -v
```

All 64 tests should pass. Test configuration is in `pyproject.toml`, and the
shared fixtures are in `tests/conftest.py`.