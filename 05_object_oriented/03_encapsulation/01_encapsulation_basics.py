# encapsulation and data hiding in python
from typing import Optional, Dict, Any
from datetime import datetime

# basic encapsulation example
class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        # private attributes (name mangling)
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__transaction_history = []
    
    # getter method for balance
    def get_balance(self) -> float:
        return self.__balance
    
    # getter method for account number (masked)
    def get_account_number(self) -> str:
        return f"***{self.__account_number[-4:]}"
    
    # public methods to interact with private data
    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.__balance += amount
            self.__log_transaction("deposit", amount)
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__log_transaction("withdrawal", amount)
            return True
        return False
    
    # private helper method
    def __log_transaction(self, transaction_type: str, amount: float) -> None:
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now(),
            "balance": self.__balance
        }
        self.__transaction_history.append(transaction)
    
    # method to view transaction history
    def get_transaction_history(self) -> list:
        return [
            f"{t['timestamp']}: {t['type']} ${t['amount']} (balance: ${t['balance']})"
            for t in self.__transaction_history
        ]

# using the bank account class
print("bank account example:")
account = BankAccount("12345678")
account.deposit(1000)
account.withdraw(500)
print(f"account: {account.get_account_number()}")
print(f"balance: ${account.get_balance()}")
print("\ntransaction history:")
for transaction in account.get_transaction_history():
    print(transaction)

# property decorators for encapsulation
class Person:
    def __init__(self, name: str, age: int):
        self.__name = name
        self.__age = age
    
    # property decorator for name
    @property
    def name(self) -> str:
        return self.__name
    
    # setter for name
    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("name cannot be empty")
        self.__name = value.strip()
    
    # property decorator for age
    @property
    def age(self) -> int:
        return self.__age
    
    # setter for age
    @age.setter
    def age(self, value: int) -> None:
        if not (0 <= value <= 150):
            raise ValueError("invalid age")
        self.__age = value
    
    # read-only property
    @property
    def is_adult(self) -> bool:
        return self.__age >= 18

print("\nperson class with properties:")
person = Person("alice", 25)
print(f"name: {person.name}")
print(f"age: {person.age}")
print(f"is adult? {person.is_adult}")

# trying to set invalid values
try:
    person.age = 200
except ValueError as e:
    print(f"error: {e}")

# encapsulation with composition
class Engine:
    def __init__(self, horsepower: int):
        self.__horsepower = horsepower
        self.__running = False
    
    def start(self) -> str:
        self.__running = True
        return "engine started"
    
    def stop(self) -> str:
        self.__running = False
        return "engine stopped"
    
    @property
    def is_running(self) -> bool:
        return self.__running

class Car:
    def __init__(self, make: str, model: str, horsepower: int):
        self.__make = make
        self.__model = model
        self.__engine = Engine(horsepower)  # composition
        self.__speed = 0
    
    def start(self) -> str:
        return self.__engine.start()
    
    def stop(self) -> str:
        self.__speed = 0
        return self.__engine.stop()
    
    def accelerate(self, speed_increase: int) -> None:
        if self.__engine.is_running:
            self.__speed = min(200, self.__speed + speed_increase)
    
    def brake(self, speed_decrease: int) -> None:
        self.__speed = max(0, self.__speed - speed_decrease)
    
    @property
    def speed(self) -> int:
        return self.__speed
    
    @property
    def info(self) -> str:
        return f"{self.__make} {self.__model}"

print("\ncar with encapsulated engine:")
car = Car("toyota", "camry", 200)
print(car.info)
print(car.start())
car.accelerate(50)
print(f"speed: {car.speed} mph")
car.brake(20)
print(f"speed after braking: {car.speed} mph")
print(car.stop())

# data validation with encapsulation
class Temperature:
    def __init__(self, celsius: float = 0):
        self.__celsius = celsius
    
    @property
    def celsius(self) -> float:
        return self.__celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:  # absolute zero
            raise ValueError("temperature cannot be below absolute zero")
        self.__celsius = value
    
    @property
    def fahrenheit(self) -> float:
        return (self.__celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5/9

print("\ntemperature conversion:")
temp = Temperature(25)
print(f"celsius: {temp.celsius}°C")
print(f"fahrenheit: {temp.fahrenheit}°F")
temp.fahrenheit = 68
print(f"new celsius: {temp.celsius}°C")

# practice exercises:
# 1. create a class that:
#    - represents a secure password manager
#    - encrypts stored passwords
#    - provides controlled access to passwords
#    - logs access attempts

# 2. create a class that:
#    - manages a user profile
#    - validates email and phone formats
#    - controls access to sensitive data
#    - provides data update mechanisms

# 3. create a class that:
#    - implements a game character
#    - manages health and power levels
#    - controls state modifications
#    - logs character actions

# example solution for #2:
import re
from typing import Optional

class UserProfile:
    def __init__(self, username: str, email: str):
        self.__username = username
        self.__email = self.__validate_email(email)
        self.__phone: Optional[str] = None
        self.__private_data: Dict[str, Any] = {}
    
    def __validate_email(self, email: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("invalid email format")
        return email
    
    def __validate_phone(self, phone: str) -> str:
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, phone):
            raise ValueError("invalid phone format")
        return phone
    
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, value: str) -> None:
        self.__email = self.__validate_email(value)
    
    @property
    def phone(self) -> Optional[str]:
        return self.__phone
    
    @phone.setter
    def phone(self, value: Optional[str]) -> None:
        if value is not None:
            self.__phone = self.__validate_phone(value)
        else:
            self.__phone = None
    
    def set_private_data(self, key: str, value: Any) -> None:
        self.__private_data[key] = value
    
    def get_private_data(self, key: str) -> Optional[Any]:
        return self.__private_data.get(key)
    
    def get_public_info(self) -> Dict[str, Any]:
        return {
            "username": self.__username,
            "email": self.__email,
            "phone": self.__phone
        }

# testing the solution
print("\ntesting user profile:")
user = UserProfile("alice_smith", "alice@example.com")
user.phone = "+1234567890"
user.set_private_data("address", "123 main st")

print("public info:", user.get_public_info())
print("private data:", user.get_private_data("address"))

try:
    user.email = "invalid-email"
except ValueError as e:
    print(f"error: {e}") 