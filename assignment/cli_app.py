"""
This application asks the user to type in two whole numbers and a opperation.
(+, -, *, /) then it preforms mathematic calcaltion with the numbers and operation and
prints the value.
"""

x = input("Please enter a number: ")

if not x.strip().replace("-", "").isdigit():
    print(f'The value "{x}" is not a valid number.')

y = input("Please enter a number: ")

if not y.strip().replace("-", "").isdigit():
    print(f'The value "{y}" is not a valid number.')

op = input("Please enter an operation: ")

if op not in ("+", "-", "*", "/"):
    print(f'The value "{op}" is not a valid operation.')

x = int(x)
y = int(y)

if op == "+":
    print(f"{x} + {y} = {x + y}")

if op == "-":
    print(f"{x} - {y} = {x - y}")

if op == "/":
    print(f"{x} + {y} = {round(x / y, 2)}")

if op == "*":
    print(f"{x} + {y} = {x * y}")
