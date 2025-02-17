# python has several numeric types: int, float, complex

# integers (int)
# whole numbers, positive or negative, unlimited size
a = 5
b = -17
big_number = 123456789012345678901234567890
print("integers:")
print("a:", a)
print("b:", b)
print("big number:", big_number)

# number systems
binary = 0b1010  # binary (base 2)
octal = 0o12  # octal (base 8)
hexadecimal = 0xFF  # hexadecimal (base 16)

print("\nnumber systems:")
print("binary 0b1010 =", binary)
print("octal 0o12 =", octal)
print("hexadecimal 0xFF =", hexadecimal)

# converting to different bases
number = 42
print("\nconverting 42 to different bases:")
print("binary:", bin(number))
print("octal:", oct(number))
print("hexadecimal:", hex(number))

# floating point numbers (float)
# numbers with decimal points
pi = 3.14159
e = 2.71828
small = 1.23e-4  # scientific notation
large = 1.23e4

print("\nfloating point numbers:")
print("pi:", pi)
print("e:", e)
print("small number:", small)
print("large number:", large)

# floating point precision
a = 0.1 + 0.2
print("\nfloating point precision:")
print("0.1 + 0.2 =", a)
print("0.1 + 0.2 == 0.3:", a == 0.3)  # false due to precision

# handling floating point precision
from decimal import Decimal
a = Decimal('0.1') + Decimal('0.2')
print("using Decimal:", a)
print("is exactly 0.3:", a == Decimal('0.3'))  # true

# complex numbers
# numbers with real and imaginary parts
z1 = 2 + 3j
z2 = complex(2, 3)  # another way to create complex numbers

print("\ncomplex numbers:")
print("z1:", z1)
print("real part:", z1.real)
print("imaginary part:", z1.imag)
print("conjugate:", z1.conjugate())

# type conversion (casting)
# converting between numeric types
x = 5
print("\ntype conversion examples:")
print("integer:", x, type(x))
print("float:", float(x), type(float(x)))
print("complex:", complex(x), type(complex(x)))

# rounding numbers
pi = 3.14159
print("\nrounding numbers:")
print("round to 2 decimal places:", round(pi, 2))
print("round to nearest integer:", round(pi))
print("floor division:", 5 // 2)  # rounds down
print("integer division:", int(5 / 2))  # truncates decimal part

# numeric operations
a = 5
b = 2

print("\nnumeric operations:")
print("addition:", a + b)
print("subtraction:", a - b)
print("multiplication:", a * b)
print("division:", a / b)
print("floor division:", a // b)
print("modulus:", a % b)
print("power:", a ** b)

# absolute values and powers
print("\nmath operations:")
print("absolute value:", abs(-5))
print("power:", pow(2, 3))
print("power with modulus:", pow(2, 3, 5))  # (2³) % 5

# importing math module for more operations
import math

print("\nmath module functions:")
print("square root:", math.sqrt(16))
print("ceiling:", math.ceil(3.7))
print("floor:", math.floor(3.7))
print("factorial:", math.factorial(5))

# practice exercises:
# 1. create a program that:
#    - converts temperatures between Celsius and Fahrenheit
#    - handles floating point precision
#    - rounds to 2 decimal places

# 2. create a program that:
#    - calculates the roots of a quadratic equation
#    - handles complex numbers
#    - formats the output nicely

# 3. create a program that:
#    - converts numbers between different bases
#    - handles negative numbers
#    - validates input

# example solution for #1:
def convert_temperature(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return round(fahrenheit, 2)

temps = [0, 21.5, 37.8, 100]
print("\ntemperature conversion:")
for c in temps:
    f = convert_temperature(c)
    print(f"{c}°C = {f}°F")