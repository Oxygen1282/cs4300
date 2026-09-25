"""Task 5: Lists and dictionaries.

A list of favorite books (title followed by author) with slicing, and a
dictionary mapping student IDs to student names.
"""

# Each book takes two entries: its title, then its author.
favorite_books = [
    "To Kill a Mockingbird", "Harper Lee",
    "1984", "George Orwell",
    "The Great Gatsby", "F. Scott Fitzgerald",
    "Pride and Prejudice", "Jane Austin",
    "The Catcher in the Rye", "J.D. Salinger",
    "Harry Potter and the Sorcerer's Stone", "J.K. Rowling",
    "The Lord of the Rings", "J.R.R. Tolkien",
    "The Hunger Games", "Suzanne Collins",
    "The Da Vinci Code", "Dan Brown",
    "The Alchemist", "Paulo",
]

# Slice [start:stop:step]: indices 0, 2 and 4 are the first three titles.
# The step of 2 skips over each author.
print(favorite_books[0:6:2])

# Student database: ID -> name. IDs are strings so leading zeros are kept
# ("001" would become 1 as an int).
students = {
    "001": "David Zark",
    "002": "John Smith",
    "003": "Anne Frank",
    "004": "Ameila Airheart",
    "005": "Bradly Martin",
}

# Looping over a dictionary gives its keys; students[key] looks up the name.
for key in students:
    print("Student ID: " + key + "      Name: " + students[key])