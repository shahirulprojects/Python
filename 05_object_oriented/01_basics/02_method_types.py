#!/usr/bin/env python3

# method types in python classes
# this file explains the different types of methods you can define in a python class
# we'll cover instance methods, class methods, and static methods with practical examples

class Temperature:
    # this is a class variable that all instances can access
    scale = "Celsius"
    
    def __init__(self, temperature):
        # instance method to initialize the object
        # self refers to the instance being created
        self.temperature = temperature
    
    def get_temperature(self):
        # regular instance method that can access and modify instance attributes
        # takes self as first parameter to access instance data
        return f"{self.temperature}°{self.scale}"
    
    @classmethod
    def set_scale(cls, new_scale):
        # class method that can modify class-level attributes
        # takes cls as first parameter to access class data
        # useful for alternative constructors or modifying class state
        if new_scale in ["Celsius", "Fahrenheit", "Kelvin"]:
            cls.scale = new_scale
            return True
        return False
    
    @classmethod
    def from_fahrenheit(cls, fahrenheit_temp):
        # class method as an alternative constructor
        # converts fahrenheit to celsius and creates a new instance
        celsius = (fahrenheit_temp - 32) * 5/9
        return cls(celsius)
    
    @staticmethod
    def is_valid_temperature(temp):
        # static method that doesn't need access to class or instance data
        # useful for utility functions related to the class
        # doesn't take self or cls as first parameter
        return isinstance(temp, (int, float)) and temp >= -273.15

# practical examples showing how to use different method types
def demonstrate_method_types():
    # creating an instance using the regular constructor
    room_temp = Temperature(25)
    
    # using instance method
    print(f"current temperature: {room_temp.get_temperature()}")  # outputs: 25°Celsius
    
    # using class method to change the scale
    Temperature.set_scale("Fahrenheit")
    print(f"after scale change: {room_temp.get_temperature()}")  # outputs: 25°Fahrenheit
    
    # using alternative constructor (class method)
    hot_day = Temperature.from_fahrenheit(98.6)
    print(f"converted temperature: {hot_day.get_temperature()}")
    
    # using static method
    print(f"is 25°C valid? {Temperature.is_valid_temperature(25)}")  # outputs: True
    print(f"is -300°C valid? {Temperature.is_valid_temperature(-300)}")  # outputs: False

if __name__ == "__main__":
    demonstrate_method_types() 