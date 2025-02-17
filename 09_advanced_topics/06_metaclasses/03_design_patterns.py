from typing import Any, Dict, Type, Optional, ClassVar
from abc import ABC, abstractmethod
import threading
import json
from datetime import datetime

# hey there! in this module, we'll see how metaclasses can help us implement
# common design patterns in a clean and elegant way :D

# 1. singleton pattern using metaclass
class SingletonMeta(type):
    # we'll store the instance here
    _instances: Dict[Type[Any], Any] = {}
    _lock = threading.Lock()  # for thread safety
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # check if we already have an instance
        if cls not in cls._instances:
            with cls._lock:  # thread safe check
                # double check (another thread might have created instance)
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# 2. abstract factory pattern with metaclass
class InterfaceCheckerMeta(type):
    def __new__(
        mcs: Type[Any],
        name: str,
        bases: tuple,
        namespace: Dict[str, Any]
    ) -> Type[Any]:
        # get required methods from class attributes
        required = namespace.get('__required_methods__', [])
        
        # check if all required methods are implemented
        for method in required:
            if method not in namespace:
                raise TypeError(
                    f"can't create abstract class {name}: "
                    f"missing required method {method}"
                )
        
        return super().__new__(mcs, name, bases, namespace)

# 3. registry pattern with metaclass
class RegistryMeta(type):
    # store registered classes here
    _registry: Dict[str, Type[Any]] = {}
    
    def __new__(
        mcs: Type[Any],
        name: str,
        bases: tuple,
        namespace: Dict[str, Any]
    ) -> Type[Any]:
        # create the class
        cls = super().__new__(mcs, name, bases, namespace)
        
        # register the class if it's not abstract
        if not namespace.get('__abstract__', False):
            mcs._registry[name] = cls
        
        return cls
    
    @classmethod
    def get_registered(mcs) -> Dict[str, Type[Any]]:
        return mcs._registry.copy()

# now let's use these metaclasses in real-world examples

# example 1: singleton database connection
class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        # simulate database connection
        self.connected = False
        self._connect()
    
    def _connect(self) -> None:
        # in real code, this would actually connect to a database
        self.connected = True
        print("connecting to database...")
    
    def query(self, sql: str) -> str:
        if not self.connected:
            self._connect()
        return f"executing query: {sql}"

# example 2: abstract factory for UI elements
class UIFactory(metaclass=InterfaceCheckerMeta):
    # define required methods for UI factories
    __required_methods__ = ['create_button', 'create_input']
    
    @abstractmethod
    def create_button(self, label: str) -> Any:
        pass
    
    @abstractmethod
    def create_input(self, placeholder: str) -> Any:
        pass

# concrete implementation for web
class WebUIFactory(UIFactory):
    def create_button(self, label: str) -> str:
        return f'<button>{label}</button>'
    
    def create_input(self, placeholder: str) -> str:
        return f'<input placeholder="{placeholder}">'

# example 3: plugin registry system
class Plugin(metaclass=RegistryMeta):
    __abstract__ = True  # base class, won't be registered
    
    @abstractmethod
    def execute(self) -> None:
        pass

class LoggingPlugin(Plugin):
    def execute(self) -> None:
        print(f"[{datetime.now()}] logging plugin executed")

class CachePlugin(Plugin):
    def execute(self) -> None:
        print("cache plugin executed")

def main():
    # test singleton
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"\nsingleton test - same instance: {db1 is db2}")
    print(db1.query("SELECT * FROM users"))
    
    # test interface checker
    ui = WebUIFactory()
    print(f"\nui elements:")
    print(ui.create_button("Click me"))
    print(ui.create_input("Enter text..."))
    
    # test registry
    print("\nregistered plugins:")
    for name, plugin_class in RegistryMeta.get_registered().items():
        print(f"- {name}")
        plugin = plugin_class()
        plugin.execute()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement a metaclass for:
#    - observer pattern
#    - automatic event notification
#    - subscriber management

# 2. implement a metaclass for:
#    - builder pattern
#    - fluent interface
#    - method chaining

# 3. implement a metaclass for:
#    - proxy pattern
#    - method interception
#    - access control 