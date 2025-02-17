from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol
from dataclasses import dataclass
import json
from datetime import datetime

# welcome to structural design patterns! these patterns help us compose objects
# and classes into larger structures while keeping them flexible and efficient :D

# 1. adapter pattern - makes incompatible interfaces work together
class OldSystem:
    def specific_request(self) -> dict:
        return {
            "data": "old system data",
            "timestamp": datetime.now().isoformat()
        }

class NewSystemProtocol(Protocol):
    def request(self) -> str:
        pass

class OldSystemAdapter(NewSystemProtocol):
    def __init__(self, old_system: OldSystem):
        self.old_system = old_system
    
    def request(self) -> str:
        # adapt old system's response to new format
        result = self.old_system.specific_request()
        return f"{result['data']} at {result['timestamp']}"

# 2. bridge pattern - separates abstraction from implementation
class Implementation(ABC):
    @abstractmethod
    def operation_impl(self) -> str:
        pass

class Abstraction:
    def __init__(self, implementation: Implementation):
        self.implementation = implementation
    
    def operation(self) -> str:
        return f"abstraction: {self.implementation.operation_impl()}"

class ConcreteImplementationA(Implementation):
    def operation_impl(self) -> str:
        return "implementation a"

class ConcreteImplementationB(Implementation):
    def operation_impl(self) -> str:
        return "implementation b"

class RefinedAbstraction(Abstraction):
    def operation(self) -> str:
        return f"refined {super().operation()}"

# 3. composite pattern - treats individual objects and compositions uniformly
class Component(ABC):
    @property
    def parent(self) -> Component:
        return self._parent
    
    @parent.setter
    def parent(self, parent: Component):
        self._parent = parent
    
    def add(self, component: Component) -> None:
        pass
    
    def remove(self, component: Component) -> None:
        pass
    
    def is_composite(self) -> bool:
        return False
    
    @abstractmethod
    def operation(self) -> str:
        pass

class Leaf(Component):
    def operation(self) -> str:
        return "leaf"

class Composite(Component):
    def __init__(self):
        self._children: List[Component] = []
    
    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self
    
    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None
    
    def is_composite(self) -> bool:
        return True
    
    def operation(self) -> str:
        results = []
        for child in self._children:
            results.append(child.operation())
        return f"branch({'+'.join(results)})"

# 4. decorator pattern - adds behavior to objects dynamically
class DataSource(ABC):
    @abstractmethod
    def write_data(self, data: str) -> None:
        pass
    
    @abstractmethod
    def read_data(self) -> str:
        pass

class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename
        self._data = ""
    
    def write_data(self, data: str) -> None:
        self._data = data
    
    def read_data(self) -> str:
        return self._data

class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        self.wrapped = source
    
    def write_data(self, data: str) -> None:
        self.wrapped.write_data(data)
    
    def read_data(self) -> str:
        return self.wrapped.read_data()

class EncryptionDecorator(DataSourceDecorator):
    def write_data(self, data: str) -> None:
        # simulate encryption
        encrypted = f"encrypted[{data}]"
        self.wrapped.write_data(encrypted)
    
    def read_data(self) -> str:
        # simulate decryption
        data = self.wrapped.read_data()
        return data.replace("encrypted[", "").replace("]", "")

class CompressionDecorator(DataSourceDecorator):
    def write_data(self, data: str) -> None:
        # simulate compression
        compressed = f"compressed[{data}]"
        self.wrapped.write_data(compressed)
    
    def read_data(self) -> str:
        # simulate decompression
        data = self.wrapped.read_data()
        return data.replace("compressed[", "").replace("]", "")

# 5. facade pattern - provides simple interface to complex system
class ComplexSubsystemA:
    def operation_a(self) -> str:
        return "subsystem a"

class ComplexSubsystemB:
    def operation_b(self) -> str:
        return "subsystem b"

class ComplexSubsystemC:
    def operation_c(self) -> str:
        return "subsystem c"

class Facade:
    def __init__(self):
        self._subsystem_a = ComplexSubsystemA()
        self._subsystem_b = ComplexSubsystemB()
        self._subsystem_c = ComplexSubsystemC()
    
    def operation(self) -> str:
        results = []
        results.append(self._subsystem_a.operation_a())
        results.append(self._subsystem_b.operation_b())
        results.append(self._subsystem_c.operation_c())
        return f"facade: {' -> '.join(results)}"

# 6. proxy pattern - controls access to objects
class Subject(ABC):
    @abstractmethod
    def request(self) -> None:
        pass

class RealSubject(Subject):
    def request(self) -> None:
        print("real subject: handling request")

class Proxy(Subject):
    def __init__(self, real_subject: RealSubject):
        self._real_subject = real_subject
        self._access_count = 0
    
    def request(self) -> None:
        if self.check_access():
            self._real_subject.request()
            self.log_access()
    
    def check_access(self) -> bool:
        print("proxy: checking access")
        return True
    
    def log_access(self) -> None:
        self._access_count += 1
        print(f"proxy: request count = {self._access_count}")

def main():
    # example 1: adapter
    old_system = OldSystem()
    adapter = OldSystemAdapter(old_system)
    print(f"adapter: {adapter.request()}")
    
    # example 2: bridge
    implementation_a = ConcreteImplementationA()
    implementation_b = ConcreteImplementationB()
    
    abstraction = Abstraction(implementation_a)
    refined = RefinedAbstraction(implementation_b)
    
    print(f"\nbridge:")
    print(f"basic: {abstraction.operation()}")
    print(f"refined: {refined.operation()}")
    
    # example 3: composite
    tree = Composite()
    
    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())
    
    branch2 = Composite()
    branch2.add(Leaf())
    
    tree.add(branch1)
    tree.add(branch2)
    
    print(f"\ncomposite: {tree.operation()}")
    
    # example 4: decorator
    source = FileDataSource("test.txt")
    
    # wrap with encryption and compression
    encrypted_compressed = CompressionDecorator(
        EncryptionDecorator(source)
    )
    
    # write and read data through decorators
    data = "hello world"
    print(f"\ndecorator:")
    print(f"original: {data}")
    
    encrypted_compressed.write_data(data)
    processed = encrypted_compressed.read_data()
    
    print(f"processed: {processed}")
    
    # example 5: facade
    facade = Facade()
    print(f"\n{facade.operation()}")
    
    # example 6: proxy
    print("\nproxy:")
    real_subject = RealSubject()
    proxy = Proxy(real_subject)
    
    proxy.request()
    proxy.request()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement a flyweight pattern that:
#    - manages shared state efficiently
#    - handles object pooling
#    - optimizes memory usage

# 2. create a composite pattern that:
#    - implements file system structure
#    - supports file operations
#    - handles permissions

# 3. implement a decorator pattern that:
#    - adds logging capabilities
#    - handles transactions
#    - manages caching 