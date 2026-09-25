"""Task 1: the script must print "Hello, World!" to stdout."""

def test_prints_hello_world(run_script, capsys):
    """Capture stdout and compare it to the exact text the assignment asks for.
 
    print() adds a newline, so the expected output ends in "\\n". An exact
    match (not "in") means extra or missing characters are caught too.
    """
    run_script("task1")
    assert capsys.readouterr().out == "Hello, World!\n"