"""

a) Both generate_id and weekday are not pure functions.
Why not? How would you write tests for these functions?

b) Rewrite both functions so that they are pure functions.
Observe what happens to the main function after making this change.
Are the functions now easier to test? Are they easier to use as well?
"""
import random
import string
from datetime import datetime
from functools import partial

def generate_id(length: int, my_partial_func) -> str:
    return "".join(
        my_partial_func() for _ in range(length)
    )


def weekday(today: datetime) -> str:
    today = datetime.today()
    return f"{today:%A}"


def main() -> None:
    today = datetime.today()
    my_partial_func=partial(random.choice, seq=string.ascii_uppercase + string.digits)
    print(f"Today is a {weekday(today)}")
    print(f"Your id = {generate_id(10, my_partial_func)}")


if __name__ == "__main__":
    main()
