# nested conditionals are if statements inside other if statements
# they help us make more complex decisions

# basic nested if
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("you can enter the venue")
    else:
        print("you need to show ID")
else:
    print("you must be 18 or older")

# the same logic using and operator (more concise)
if age >= 18 and has_id:
    print("you can enter the venue")
else:
    print("you cannot enter the venue")

# complex decision making
is_weekend = True
weather = "sunny"
temperature = 25
has_money = True

if is_weekend:
    if weather == "sunny" and temperature > 20:
        if has_money:
            print("\nlet's go to the beach!")
        else:
            print("\nlet's go to the park instead")
    else:
        print("\nlet's stay home and watch movies")
else:
    print("\nit's a work day")

# using elif for multiple conditions
# example: movie ticket pricing
age = 15
is_student = True
is_senior = False

if age < 12:
    ticket_price = 5  # child price
elif age >= 65 or is_senior:
    ticket_price = 7  # senior price
elif is_student:
    ticket_price = 8  # student price
else:
    ticket_price = 12  # regular adult price

print(f"\nticket price: ${ticket_price}")

# combining conditions with parentheses
has_membership = True
items_in_cart = 5
cart_value = 150

# complex discount rules
if (has_membership and cart_value > 100) or (items_in_cart > 10):
    discount = 0.2  # 20% discount
elif has_membership or cart_value > 200:
    discount = 0.1  # 10% discount
else:
    discount = 0    # no discount

final_price = cart_value * (1 - discount)
print(f"\ncart value: ${cart_value}")
print(f"discount: {discount:.0%}")
print(f"final price: ${final_price:.2f}")

# using nested if vs. and operator
# method 1: nested if (more readable for complex conditions)
if temperature > 25:
    if weather == "sunny":
        if has_money:
            print("\nperfect day for ice cream!")

# method 2: using and (more concise)
if temperature > 25 and weather == "sunny" and has_money:
    print("perfect day for ice cream!")

# practice exercises:
# 1. create a loan eligibility checker that checks:
#    - minimum age of 21
#    - minimum income of 30000
#    - minimum credit score of 700
#    - no existing loans
#    use nested if statements

# 2. create a game character's action decision system:
#    - check if character has weapon
#    - check if character has enough health (> 50)
#    - check if there are enemies nearby
#    - decide whether to attack, heal, or run

# 3. create a shopping cart discount system:
#    - apply different discounts based on:
#      * cart total
#      * membership status
#      * seasonal sale
#      * coupon code
#    - print the final price with all applicable discounts

# example solution for #1:
age = 25
income = 45000
credit_score = 750
has_existing_loan = False

print("\nLoan Eligibility Check:")
if age >= 21:
    if income >= 30000:
        if credit_score >= 700:
            if not has_existing_loan:
                print("congratulations! you are eligible for a loan")
            else:
                print("sorry, you already have an existing loan")
        else:
            print("sorry, your credit score is too low")
    else:
        print("sorry, your income does not meet the minimum requirement")
else:
    print("sorry, you must be at least 21 years old") 