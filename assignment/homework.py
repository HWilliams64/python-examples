def add(x: int, y: int) -> int:
    """Add two numbers together and returns the sum

    Args:
        x (int): A whole number
        y (int): A whole number

    Returns:
        int: The sum of x and y
    """
    return x + y


def remove_all(value, sequence: list) -> None:
    """Removes all occurrences of the value from the list

    Args:
        value (Any): A value to be removed
        sequence (list): A list of values that will be modified
    """

    while value in sequence:
        sequence.remove(value)

    return sequence
