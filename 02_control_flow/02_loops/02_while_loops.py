# while loops repeat a block of code as long as a condition is true
# they're useful when we don't know how many iterations we need

# basic while loop
count = 1
while count <= 5:
    print(f"count is {count}")
    count += 1  # don't forget to update the counter!

# while loop with user input
print("\nguessing game:")
secret_number = 7
guess = 0  # initialize with a number that's not the secret

while guess != secret_number:
    guess = int(input("guess the number (1-10): "))
    if guess < secret_number:
        print("too low!")
    elif guess > secret_number:
        print("too high!")

print("you got it!")

# while loop with multiple conditions
age = 25
savings = 100
target = 1000

print("\nsaving simulator:")
years = 0
while savings < target and age < 65:
    savings += 100  # save 100 per year
    age += 1
    years += 1
    print(f"after year {years}: ${savings}")

# using while True for infinite loops
# (must use break to exit)
print("\ncounting with break:")
count = 1
while True:
    print(count)
    if count >= 5:
        break  # exits the loop
    count += 1

# using continue to skip iterations
print("\nprinting odd numbers:")
count = 0
while count < 10:
    count += 1
    if count % 2 == 0:  # if number is even
        continue  # skip the rest of this iteration
    print(count)

# while loop with else clause
# else runs when condition becomes false (not after break)
print("\ncounting with else:")
count = 1
while count <= 3:
    print(count)
    count += 1
else:
    print("loop completed normally")

# handling invalid input
print("\nhandling invalid input:")
while True:
    try:
        age = int(input("enter your age: "))
        if age < 0:
            print("age cannot be negative")
            continue
        break  # exit loop if input is valid
    except ValueError:
        print("please enter a valid number")

print(f"your age is {age}")

# nested while loops
print("\nmultiplication table using while:")
i = 1
while i <= 3:
    j = 1
    while j <= 3:
        print(f"{i} x {j} = {i * j}")
        j += 1
    print("-" * 15)
    i += 1

# practice exercises:
# 1. create a simple ATM simulator that:
#    - starts with a balance of 1000
#    - allows deposits and withdrawals
#    - continues until user chooses to exit
#    - validates input and maintains minimum balance

# 2. create a number guessing game that:
#    - generates a random number between 1 and 100
#    - gives user limited attempts (e.g., 7)
#    - provides hints (higher/lower)
#    - displays number of attempts used

# 3. create a simple calculator that:
#    - asks for two numbers and an operation (+, -, *, /)
#    - performs the calculation
#    - asks if user wants to continue
#    - handles division by zero and invalid operations

# example solution for #1:
balance = 1000
while True:
    print(f"\ncurrent balance: ${balance}")
    print("1: deposit")
    print("2: withdraw")
    print("3: exit")
    
    choice = input("enter choice (1-3): ")
    
    if choice == "3":
        print("thank you for using our ATM")
        break
    elif choice == "1":
        amount = float(input("enter deposit amount: $"))
        if amount > 0:
            balance += amount
        else:
            print("invalid amount")
    elif choice == "2":
        amount = float(input("enter withdrawal amount: $"))
        if amount > 0 and amount <= balance:
            balance -= amount
        else:
            print("invalid amount or insufficient funds")
    else:
        print("invalid choice") 