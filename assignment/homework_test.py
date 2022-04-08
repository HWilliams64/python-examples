import unittest
import random
import string
import math
from assignment.test_helper import ScriptComm


class AddTests(unittest.TestCase):
    def check(self, x, y):
        try:
            from assignment.homework import add
        except ImportError:
            self.fail("The function add() is missing from the homework.py module.")

        expected = x + y

        msg_start = (
            f"The function add({x}, {y}) were called, it was expected to return"
            f" {expected}. "
        )

        try:
            v = add(x, y)
            self.assertEqual(
                expected, v, msg_start + f" But the value {v} was returned."
            )
        except Exception as e:
            self.fail(msg_start + f"But a {type(e).__name__} was raised, because {e}.")

    def test_positive_numbers(self):
        for _ in range(10):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.check(x, y)

    def test_negatives_numbers(self):
        for _ in range(10):
            x = random.randint(-100, 0)
            y = random.randint(-100, 0)
            self.check(x, y)


class RemoveAllTests(unittest.TestCase):
    def check(self, to_remove, sequence):
        try:
            from assignment.homework import remove_all
        except ImportError:
            self.fail(
                "The function remove_all() is missing from the homework.py module."
            )

        expected = [value for value in sequence if value != to_remove]

        msg_start = (
            f"The function remove_all({to_remove}, {sequence}) were called, it was"
            f" expected to return {expected}. "
        )

        try:
            v = remove_all(to_remove, sequence)
            self.assertListEqual(
                expected, v, msg_start + f" But the value {v} was returned."
            )
        except Exception as e:
            self.fail(msg_start + f"But a {type(e).__name__} was raised, because {e}.")

    def test_positive_numbers(self):
        for _ in range(10):

            items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, *string.ascii_lowercase]

            sequence = random.choices(items, k=10)
            to_remove = random.choice(sequence)

            self.check(to_remove, sequence)


class CLITests(unittest.TestCase):
    def test_success(self):
        for op in ("+", "-", "*", "/"):

            x = random.randint(0, 100)
            y = random.randint(0, 100)

            with ScriptComm("cli_app", self) as proc:
                proc.write(x)
                proc.write(y)
                proc.write(op)

                func_dict = {
                    "+": lambda x, y: x + y,
                    "-": lambda x, y: x - y,
                    "*": lambda x, y: x * y,
                    "/": lambda x, y: x / y,
                }

                expected = func_dict[op](x, y)

                if not proc.contains_number(expected_num=expected, delta=0.5):
                    self.fail(
                        f"The module cli_app.py was run and the values {x}, {y}, and"
                        f" {op} were typed in. The application was expected to print"
                        f" the value {expected}. But the following was"
                        f" printed:\n\n{proc.read(last_line=False)}"
                    )
