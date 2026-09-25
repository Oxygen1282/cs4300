"""Task 4: Functions and duck typing.

calculate_discount works with any numeric type because it only relies on
the number supporting comparison and arithmetic, not on its exact type.
"""


def calculate_discount(price, discount):
    """Return the price after taking off a percentage discount.

    Works with any numeric type that supports comparison and arithmetic
    (int, float, Decimal, Fraction) - that's duck typing.

    Raises ValueError if price is negative or discount is not 0-100.
    """
    # Validate with comparisons rather than isinstance checks, so any
    # number-like type is still accepted. Non-numbers such as strings
    # can't be compared to 0 and raise TypeError on their own.
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount <= 100:
        raise ValueError("Discount must be between 0 and 100")

    # Convert the percentage to a fraction (20 -> 0.2) and subtract that
    # share of the price.
    priceToSubtract = price * (discount / 100)
    cost = price - priceToSubtract
    return cost


price = float(input("Enter a price: "))
discount = float(input("Enter a discount: "))

# Print as dollars with 2 decimal places; show a clear message instead of
# crashing if the values are out of range.
try:
    print(f"${calculate_discount(price, discount):.2f}")
except ValueError as error:
    print(f"Invalid input: {error}")