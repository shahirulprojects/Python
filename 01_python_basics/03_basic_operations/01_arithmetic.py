# python supports all basic arithmetic operations

# addition
a = 5 + 3
print("5 + 3 =", a)  # prints 8

# subtraction
b = 10 - 4
print("10 - 4 =", b)  # prints 6

# multiplication
c = 4 * 3
print("4 * 3 =", c)  # prints 12

# division (always returns a float)
d = 15 / 3
print("15 / 3 =", d)  # prints 5.0

# integer division (removes decimal part)
e = 17 // 3
print("17 // 3 =", e)  # prints 5

# modulus (remainder)
f = 17 % 3
print("17 % 3 =", f)  # prints 2

# exponentiation (power)
g = 2 ** 3
print("2 ** 3 =", g)  # prints 8

# order of operations (PEMDAS)
# parentheses, exponents, multiplication/division, addition/subtraction
result = 2 + 3 * 4
print("2 + 3 * 4 =", result)  # prints 14

result_with_parentheses = (2 + 3) * 4
print("(2 + 3) * 4 =", result_with_parentheses)  # prints 20

# working with variables
x = 10
y = 5

# we can use variables in operations
sum_result = x + y
difference = x - y
product = x * y
quotient = x / y

print("Sum:", sum_result)
print("Difference:", difference)
print("Product:", product)
print("Quotient:", quotient)

# augmented assignment operators
number = 5
print("Original number:", number)

number += 3  # same as: number = number + 3
print("After adding 3:", number)

number -= 2  # same as: number = number - 2
print("After subtracting 2:", number)

number *= 4  # same as: number = number * 4
print("After multiplying by 4:", number)

number /= 2  # same as: number = number / 2
print("After dividing by 2:", number)

# practice exercises:
# 1. calculate the area of a rectangle with length 8 and width 5
# 2. calculate the remainder when 25 is divided by 4
# 3. calculate 3 to the power of 4
# 4. use parentheses to change the result of: 4 + 3 * 2

# example solution for #1:
length = 8
width = 5
area = length * width
print("Area of rectangle:", area) 