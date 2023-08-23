import string
import random

_symbols = string.ascii_letters + string.digits + string.punctuation


def generate_sequence(length: int) -> str:
    """Generate a random sequence of digits, letters and
    punctuation marks of the passed length.

    Args:
        length (int): The length of the output random sequence.

    Returns:
        str: A random sequence.
    """

    return "".join(random.sample(_symbols, length))
