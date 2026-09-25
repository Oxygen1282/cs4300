"""Task 2: Variables and data types.

Demonstrates Python's four basic data types (int, float, str, bool) and
how they behave in arithmetic, slicing, concatenation and if statements.
"""

# Integers: whole numbers. int + int stays an int, so this prints 15.
int1, int2 = 7, 8

print(int1 + int2)

# Floats: numbers with a decimal point. Float arithmetic can have tiny
# rounding errors because floats are stored in binary.
float1, float2 = 10.0, 14.9

print(float1 + float2)
# Mixing a float with an int produces a float, so this prints 18.0, not 18.
print(float1 + int2)

# Strings: text. Slicing [1:4] takes characters at indices 1, 2 and 3;
# the end index is excluded, so "String"[1:4] is "tri".
string = "String"
print(string)

new_string = string[1:4]
print(new_string)

# Booleans: True or False, used here to decide whether code runs.
boolian = True

# Runs because boolian is True. str() is needed because Python won't
# join a string and an int with + directly.
if boolian:
    print(string + str(int1))
    boolian = False

# Skipped: boolian was set to False above, so this never prints.
if boolian:
    print("This shouldn't print")

# A float also has to be converted with str() before joining it to a string.
print(new_string + str(float2))