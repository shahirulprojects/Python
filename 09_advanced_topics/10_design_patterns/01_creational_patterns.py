from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import json
import copy

# welcome to python design patterns! let's start with creational patterns :D
# these patterns help us create objects in a flexible and reusable way

# 1. singleton pattern - ensures only one instance exists
class Singleton:
    _instance: Optional[Singleton] = None
    
    def __new__(cls) -> Singleton:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # initialize only once
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.data = {}

# 2. factory method pattern - creates objects without specifying exact class
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError(f"unknown animal type: {animal_type}")

# 3. abstract factory pattern - creates families of related objects
class UIElement(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Button(UIElement):
    def __init__(self, theme: str):
        self.theme = theme
    
    def render(self) -> str:
        return f"{self.theme} button"

class Input(UIElement):
    def __init__(self, theme: str):
        self.theme = theme
    
    def render(self) -> str:
        return f"{self.theme} input"

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_input(self) -> Input:
        pass

class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return Button("light")
    
    def create_input(self) -> Input:
        return Input("light")

class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return Button("dark")
    
    def create_input(self) -> Input:
        return Input("dark")

# 4. builder pattern - constructs complex objects step by step
@dataclass
class Computer:
    cpu: str = ""
    memory: str = ""
    storage: str = ""
    gpu: str = ""

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu: str) -> ComputerBuilder:
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory: str) -> ComputerBuilder:
        self.computer.memory = memory
        return self
    
    def add_storage(self, storage: str) -> ComputerBuilder:
        self.computer.storage = storage
        return self
    
    def add_gpu(self, gpu: str) -> ComputerBuilder:
        self.computer.gpu = gpu
        return self
    
    def build(self) -> Computer:
        return copy.deepcopy(self.computer)

# 5. prototype pattern - creates new objects by cloning existing ones
class Prototype:
    def clone(self) -> Prototype:
        return copy.deepcopy(self)

@dataclass
class Document(Prototype):
    content: str
    formatting: Dict[str, Any]
    
    def clone(self) -> Document:
        return copy.deepcopy(self)

def main():
    # example 1: singleton
    config1 = Singleton()
    config1.data['server'] = 'localhost'
    
    config2 = Singleton()
    print(f"singleton works: {config1 is config2}")
    print(f"shared data: {config2.data}")
    
    # example 2: factory method
    factory = AnimalFactory()
    
    dog = factory.create_animal("dog")
    cat = factory.create_animal("cat")
    
    print(f"\ndog says: {dog.speak()}")
    print(f"cat says: {cat.speak()}")
    
    # example 3: abstract factory
    light_factory = LightThemeFactory()
    dark_factory = DarkThemeFactory()
    
    # create light theme ui
    light_button = light_factory.create_button()
    light_input = light_factory.create_input()
    
    # create dark theme ui
    dark_button = dark_factory.create_button()
    dark_input = dark_factory.create_input()
    
    print(f"\nlight theme:")
    print(f"- {light_button.render()}")
    print(f"- {light_input.render()}")
    
    print(f"\ndark theme:")
    print(f"- {dark_button.render()}")
    print(f"- {dark_input.render()}")
    
    # example 4: builder
    computer = (
        ComputerBuilder()
        .add_cpu("Intel i9")
        .add_memory("32GB")
        .add_storage("1TB SSD")
        .add_gpu("RTX 3080")
        .build()
    )
    
    print(f"\nbuilt computer:")
    print(json.dumps(computer.__dict__, indent=2))
    
    # example 5: prototype
    original_doc = Document(
        content="hello world",
        formatting={
            'font': 'Arial',
            'size': 12,
            'color': 'black'
        }
    )
    
    # clone and modify
    copy_doc = original_doc.clone()
    copy_doc.content = "hello universe"
    copy_doc.formatting['color'] = 'blue'
    
    print(f"\noriginal document:")
    print(json.dumps(original_doc.__dict__, indent=2))
    
    print(f"\nmodified copy:")
    print(json.dumps(copy_doc.__dict__, indent=2))

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement a registry pattern that:
#    - manages object creation
#    - supports plugin architecture
#    - handles dependencies

# 2. create a pool pattern that:
#    - manages reusable objects
#    - handles resource limits
#    - implements cleanup

# 3. implement a multiton pattern that:
#    - supports multiple instances
#    - manages instance lifecycle
#    - handles state management 