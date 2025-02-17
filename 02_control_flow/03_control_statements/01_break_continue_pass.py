# control statements help us modify the flow of loops and conditional blocks
# main control statements: break, continue, and pass

# break statement: exits the loop completely
print("break example:")
for i in range(1, 6):
    if i == 4:
        break  # exit loop when i is 4
    print(i)
print("loop ended")

# continue statement: skips the rest of the current iteration
print("\ncontinue example:")
for i in range(1, 6):
    if i == 3:
        continue  # skip printing when i is 3
    print(i)

# pass statement: does nothing (placeholder)
print("\npass example:")
for i in range(1, 4):
    if i == 2:
        pass  # placeholder for future code
    else:
        print(i)

# using break in nested loops
print("\nbreak in nested loops:")
for i in range(1, 4):
    for j in range(1, 4):
        if i * j > 6:
            print("product > 6 found")
            break  # breaks only inner loop
        print(f"{i} x {j} = {i * j}")

# breaking out of nested loops using flag
print("\nbreaking nested loops with flag:")
should_break = False
for i in range(1, 4):
    for j in range(1, 4):
        if i * j > 6:
            print("product > 6 found")
            should_break = True
            break
        print(f"{i} x {j} = {i * j}")
    if should_break:
        break

# continue with while loops
print("\ncontinue in while loop:")
count = 0
while count < 5:
    count += 1
    if count == 3:
        continue
    print(count)

# loop else clause
# runs when loop completes normally (not after break)
print("\nloop else example 1:")
for i in range(1, 4):
    print(i)
else:
    print("loop completed normally")

print("\nloop else example 2:")
for i in range(1, 4):
    if i == 2:
        break
    print(i)
else:
    print("this won't print because of break")

# practical example: searching in a list
numbers = [1, 3, 5, 7, 9, 11, 13, 15]
search_for = 10

print("\nsearching for", search_for)
for num in numbers:
    if num == search_for:
        print("found it!")
        break
else:
    print("number not found")

# combining break and continue
print("\ncombining break and continue:")
max_attempts = 3
password = "secret"

attempt = 0
while attempt < max_attempts:
    user_input = input("enter password: ")
    attempt += 1
    
    if user_input == "":
        print("empty input, try again")
        continue
        
    if user_input == password:
        print("access granted!")
        break
else:
    print("too many attempts")

# practice exercises:
# 1. create a program that:
#    - asks user for numbers until they enter 0
#    - skips negative numbers
#    - prints the sum of positive numbers
#    - uses break and continue appropriately

# 2. create a prime number checker that:
#    - takes a number from user
#    - checks if it's prime
#    - uses break when number is found to be not prime
#    - uses else clause to confirm it's prime

# 3. create a shopping list program that:
#    - allows adding items
#    - allows removing items
#    - uses pass for features to be implemented later
#    - exits when user enters 'done'

# example solution for #1:
print("\nsum of positive numbers:")
total = 0
while True:
    num = float(input("enter a number (0 to stop): "))
    
    if num == 0:
        break
    
    if num < 0:
        print("skipping negative number")
        continue
        
    total += num

print(f"sum of positive numbers: {total}") 