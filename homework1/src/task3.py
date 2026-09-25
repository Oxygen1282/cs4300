"""Task 3: Control structures.

Uses an if statement to classify a number as positive, negative or zero,
a for loop to find the first 10 prime numbers, and a while loop to sum
the numbers from 1 to 100.
"""
import math

# --- Input with validation (while loop + try/except) ---
# Keep asking until the user types a real number. float() raises ValueError
# for text like "abc", and "nan" parses as a float but isn't a number that
# can be positive, negative or zero, so both get rejected.
while True:
    try:
        number = float(input("Enter a number: "))
    except ValueError:
        print("That isn't a number, try again.")
        continue
    if math.isnan(number):
        print("That isn't a number, try again.")
        continue
    break

# --- If statement: positive, negative or zero ---
if number > 0:
    print("That number is positive")
elif number < 0:
    print("That number is negative")
else:
    print("That number is 0")

# --- For loop: the first 10 prime numbers ---
# The first 10 primes are all below 30, so checking 2-29 finds exactly 10.
primes = []

for i in range(2, 30):
    # A number that isn't prime always has a factor no bigger than its
    # square root, so only divisors up to sqrt(i) need checking.
    square_root = int(math.sqrt(i)) + 1
    for j in range(2, square_root):
        if i % j == 0:
            break          # found a factor, so i isn't prime
    else:
        # A for loop's else runs only if the loop finished without break,
        # meaning no factor was found and i is prime.
        primes.append(i)

print(primes)

# --- While loop: sum of 1 to 100 ---
# count runs 0-100 (starting at 0 adds nothing), so total ends at 5050.
count, total = 0, 0

while count < 101:
    total += count
    count += 1

print(total)