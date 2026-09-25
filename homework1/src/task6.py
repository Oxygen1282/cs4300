"""Task 6: File handling.

Reads task6_read_me.txt and counts the words in it. The file is opened by
a relative path, so run this from the homework1 folder:
    python3 src/task6.py
"""

# "with" closes the file automatically, even if an error happens.
with open("task6_read_me.txt", "r") as file:
    file_text = file.read()

# split() with no arguments splits on any run of whitespace (spaces, tabs,
# newlines) and ignores leading/trailing whitespace, so every word is one
# token. Stray "," or "." tokens are dropped because they aren't words.
words = [token for token in file_text.split() if token not in (",", ".")]
count = len(words)

print("There are " + str(count) + " words in that file. (Not counting ',' or '.' as words)")