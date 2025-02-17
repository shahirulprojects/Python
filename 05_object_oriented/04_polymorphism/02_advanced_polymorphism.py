# advanced polymorphism patterns in python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol, TypeVar, Generic
from datetime import datetime
import json
import os
from enum import Enum, auto

# advanced abstract base classes with mixins
class Loggable:
    def __init__(self):
        self._log: List[Dict[str, Any]] = []
    
    def log(self, message: str, level: str = "info"):
        self._log.append({
            "timestamp": datetime.now(),
            "message": message,
            "level": level
        })
    
    def get_logs(self) -> List[Dict[str, Any]]:
        return self._log

class Serializable:
    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

# abstract base class with mixins
class Vehicle(ABC, Loggable, Serializable):
    def __init__(self, make: str, model: str, year: int):
        super().__init__()  # initialize Loggable
        self.make = make
        self.model = model
        self.year = year
        self._status = "stopped"
    
    @abstractmethod
    def start(self) -> str:
        pass
    
    @abstractmethod
    def stop(self) -> str:
        pass
    
    @property
    def status(self) -> str:
        return self._status

# concrete implementations
class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_capacity: float):
        super().__init__(make, model, year)
        self.battery_capacity = battery_capacity
    
    def start(self) -> str:
        self._status = "running"
        self.log("electric car started")
        return "starting electric motor..."
    
    def stop(self) -> str:
        self._status = "stopped"
        self.log("electric car stopped")
        return "stopping electric motor..."

class HybridCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_capacity: float, fuel_capacity: float):
        super().__init__(make, model, year)
        self.battery_capacity = battery_capacity
        self.fuel_capacity = fuel_capacity
    
    def start(self) -> str:
        self._status = "running"
        self.log("hybrid car started in electric mode")
        return "starting hybrid system..."
    
    def stop(self) -> str:
        self._status = "stopped"
        self.log("hybrid car stopped")
        return "stopping hybrid system..."

# solution for file handler exercise
class FileHandler(ABC):
    @abstractmethod
    def read(self, file_path: str) -> Any:
        pass
    
    @abstractmethod
    def write(self, file_path: str, content: Any) -> bool:
        pass
    
    def validate_path(self, file_path: str) -> bool:
        return os.path.exists(os.path.dirname(file_path))

class JsonFileHandler(FileHandler):
    def read(self, file_path: str) -> Dict[str, Any]:
        if not file_path.endswith('.json'):
            raise ValueError("not a json file")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def write(self, file_path: str, content: Dict[str, Any]) -> bool:
        if not self.validate_path(file_path):
            return False
        
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)
        return True

class CsvFileHandler(FileHandler):
    def read(self, file_path: str) -> List[List[str]]:
        if not file_path.endswith('.csv'):
            raise ValueError("not a csv file")
        
        result = []
        with open(file_path, 'r') as f:
            for line in f:
                result.append(line.strip().split(','))
        return result
    
    def write(self, file_path: str, content: List[List[str]]) -> bool:
        if not self.validate_path(file_path):
            return False
        
        with open(file_path, 'w') as f:
            for row in content:
                f.write(','.join(row) + '\n')
        return True

# solution for notification system exercise
class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class NotificationProtocol(Protocol):
    def send(self, message: str, priority: Priority) -> bool:
        pass
    
    def format_message(self, message: str) -> str:
        pass

class EmailNotification:
    def __init__(self, recipient: str):
        self.recipient = recipient
    
    def send(self, message: str, priority: Priority) -> bool:
        formatted = self.format_message(message)
        print(f"sending email to {self.recipient}: {formatted}")
        return True
    
    def format_message(self, message: str) -> str:
        return f"[{datetime.now()}] {message}"

class SlackNotification:
    def __init__(self, channel: str):
        self.channel = channel
    
    def send(self, message: str, priority: Priority) -> bool:
        formatted = self.format_message(message)
        print(f"sending to slack channel {self.channel}: {formatted}")
        return True
    
    def format_message(self, message: str) -> str:
        return f"[{priority.name}] {message}"

class NotificationSystem:
    def __init__(self):
        self.handlers: Dict[Priority, List[NotificationProtocol]] = {
            priority: [] for priority in Priority
        }
    
    def register_handler(self, handler: NotificationProtocol, priority: Priority):
        self.handlers[priority].append(handler)
    
    def notify(self, message: str, priority: Priority):
        for handler in self.handlers[priority]:
            handler.send(message, priority)

# combining polymorphism with encapsulation
class Observable(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: 'Observer'):
        self._observers.append(observer)
    
    def detach(self, observer: 'Observer'):
        self._observers.remove(observer)
    
    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class StockPrice(Observable):
    def __init__(self, symbol: str):
        super().__init__()
        self._symbol = symbol
        self._price = 0.0
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("price cannot be negative")
        old_price = self._price
        self._price = value
        if abs(value - old_price) > old_price * 0.1:  # 10% change
            self.notify(f"significant price change for {self._symbol}: {value:.2f}")

class StockTrader(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str):
        print(f"trader {self.name} received alert: {message}")

# testing advanced patterns
def test_vehicles():
    print("testing vehicles with mixins:")
    cars: List[Vehicle] = [
        ElectricCar("tesla", "model 3", 2024, 75.0),
        HybridCar("toyota", "prius", 2024, 8.8, 43.0)
    ]
    
    for car in cars:
        print(f"\n{car.__class__.__name__}:")
        print(car.start())
        print(car.stop())
        print("logs:", json.dumps(car.get_logs(), indent=2, default=str))
        print("serialized:", car.to_json())

def test_file_handlers():
    print("\ntesting file handlers:")
    handlers: Dict[str, FileHandler] = {
        "json": JsonFileHandler(),
        "csv": CsvFileHandler()
    }
    
    # simulate file operations
    for name, handler in handlers.items():
        print(f"\n{name} handler:")
        print(f"validates path: {handler.validate_path('.')}")

def test_notification_system():
    print("\ntesting notification system:")
    system = NotificationSystem()
    
    # register handlers
    email = EmailNotification("admin@example.com")
    slack = SlackNotification("#alerts")
    
    system.register_handler(email, Priority.HIGH)
    system.register_handler(slack, Priority.CRITICAL)
    
    # send notifications
    system.notify("server load high", Priority.HIGH)
    system.notify("service down!", Priority.CRITICAL)

def test_stock_system():
    print("\ntesting stock system:")
    stock = StockPrice("AAPL")
    trader1 = StockTrader("alice")
    trader2 = StockTrader("bob")
    
    stock.attach(trader1)
    stock.attach(trader2)
    
    stock.price = 150.0  # no alert
    stock.price = 180.0  # should trigger alert (>10% change)

if __name__ == "__main__":
    test_vehicles()
    test_file_handlers()
    test_notification_system()
    test_stock_system() 