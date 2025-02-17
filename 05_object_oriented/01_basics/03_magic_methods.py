#!/usr/bin/env python3

# magic methods (dunder methods) in python
# these are special methods that start and end with double underscores
# they allow us to define how objects behave in different situations

class BankAccount:
    def __init__(self, account_holder, balance=0):
        # initialize method - called when creating a new instance
        # this runs when we create a new BankAccount object
        self.holder = account_holder
        self.balance = balance
        self.transactions = []
    
    def __str__(self):
        # string representation for humans
        # this runs when we print the object or convert it to string
        return f"bank account belonging to {self.holder} with balance ${self.balance:.2f}"
    
    def __repr__(self):
        # detailed string representation for developers
        # this should ideally contain enough info to recreate the object
        return f"BankAccount(account_holder='{self.holder}', balance={self.balance})"
    
    def __len__(self):
        # length method - defines what len(object) returns
        # in this case, we'll return the number of transactions
        return len(self.transactions)
    
    def __add__(self, amount):
        # addition operator - defines behavior for '+'
        # allows us to use: account + 100 to deposit money
        if isinstance(amount, (int, float)) and amount > 0:
            self.balance += amount
            self.transactions.append(f"deposit: +${amount:.2f}")
        return self
    
    def __sub__(self, amount):
        # subtraction operator - defines behavior for '-'
        # allows us to use: account - 50 to withdraw money
        if isinstance(amount, (int, float)) and amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transactions.append(f"withdrawal: -${amount:.2f}")
            else:
                raise ValueError("insufficient funds for withdrawal")
        return self
    
    def __bool__(self):
        # boolean representation - defines behavior for bool(object)
        # returns True if account has positive balance
        return self.balance > 0
    
    def __getitem__(self, index):
        # defines behavior for accessing items with square brackets
        # allows us to access transactions like: account[0]
        return self.transactions[index]
    
    def __eq__(self, other):
        # equality comparison - defines behavior for ==
        if not isinstance(other, BankAccount):
            return False
        return self.holder == other.holder and self.balance == other.balance

# practical examples showing how magic methods work
def demonstrate_magic_methods():
    # creating a new account (uses __init__)
    account = BankAccount("john doe", 1000)
    
    # printing account info (uses __str__)
    print(account)  # outputs: bank account belonging to john doe with balance $1000.00
    
    # developer representation (uses __repr__)
    print(repr(account))  # outputs: BankAccount(account_holder='john doe', balance=1000)
    
    # using addition to deposit (uses __add__)
    account + 500
    
    # using subtraction to withdraw (uses __sub__)
    account - 200
    
    # checking number of transactions (uses __len__)
    print(f"number of transactions: {len(account)}")  # outputs: 2
    
    # checking if account has money (uses __bool__)
    print(f"account has funds: {bool(account)}")  # outputs: True
    
    # accessing transaction history (uses __getitem__)
    print(f"first transaction: {account[0]}")  # outputs: deposit: +$500.00
    
    # comparing accounts (uses __eq__)
    another_account = BankAccount("jane doe", 2000)
    print(f"accounts are equal: {account == another_account}")  # outputs: False

if __name__ == "__main__":
    demonstrate_magic_methods() 