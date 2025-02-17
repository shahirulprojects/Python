from typing import Any, Dict, Type

# hey there! welcome to the magical world of metaclasses in python :D
# metaclasses are like recipes that tell python how to create classes
# think of them as "class factories" - they help us make classes with special powers

# first, let's understand what happens when python creates a class
# normally, python uses type() to create classes behind the scenes
# we can actually do this ourselves :)

# this is how we usually create a class
class NormalClass:
    x = 1
    
    def hello(self):
        return "hi there!"

# but we can also create the same class using type()
# type(name, bases, namespace) is the recipe for creating classes
NormalClassWithType = type(
    "NormalClassWithType",  # name of our class
    (),                     # tuple of parent classes (empty here)
    {                       # class attributes and methods
        "x": 1,
        "hello": lambda self: "hi there!"
    }
)

# now let's create our first metaclass :D
# a metaclass is just a class that inherits from type
class LoggingMetaclass(type):
    # this method runs when python creates a new class
    def __new__(
        mcs: Type[Any],           # the metaclass itself
        name: str,                # name of the class being created
        bases: tuple,             # parent classes
        namespace: Dict[str, Any] # class attributes and methods
    ) -> Type[Any]:
        # let's log what's happening when the class is created
        print(f"creating class named: {name}")
        print(f"it has these parent classes: {bases}")
        print(f"and these attributes/methods: {list(namespace.keys())}")
        
        # create and return the new class using type's __new__
        return super().__new__(mcs, name, bases, namespace)

# now let's use our metaclass to create a class with special powers
class MySpecialClass(metaclass=LoggingMetaclass):
    # python will use LoggingMetaclass to create this class
    # it will print info about the class creation process
    
    def __init__(self, value: int):
        self.value = value
    
    def double_value(self) -> int:
        return self.value * 2

# let's see it in action
def main():
    # create instances of our classes
    normal = NormalClass()
    normal_type = NormalClassWithType()
    special = MySpecialClass(42)
    
    # they all work the same way
    print(f"\nnormal class says: {normal.hello()}")
    print(f"type-created class says: {normal_type.hello()}")
    print(f"special class doubled value: {special.double_value()}")

if __name__ == "__main__":
    main()

# practice exercises to help you learn:
# 1. create a metaclass that:
#    - adds a timestamp to every method call
#    - logs which methods are most frequently used
#    - measures how long each method takes to run

# 2. create a metaclass that:
#    - automatically adds property getters/setters
#    - validates attribute types
#    - prevents attribute deletion

# 3. create a metaclass that:
#    - enforces a specific naming convention
#    - requires documentation for all methods
#    - adds debug logging to all methods 