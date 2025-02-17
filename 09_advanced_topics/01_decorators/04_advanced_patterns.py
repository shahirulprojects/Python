# advanced decorator patterns in python
from typing import Any, Callable, TypeVar, cast, Optional, Dict, List, Type
from functools import wraps, partial
import logging
import inspect
import time
import asyncio
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

def compose(*decorators: Callable[[F], F]) -> Callable[[F], F]:
    """decorator to compose multiple decorators."""
    def decorator(func: F) -> F:
        for dec in reversed(decorators):
            func = dec(func)
        return func
    return decorator

def parametric_decorator(
    param1: Any = None,
    param2: Any = None
) -> Callable[[F], F]:
    """decorator factory with parameters."""
    def real_decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # use parameters in wrapper
            if param1:
                logging.info(f"param1: {param1}")
            if param2:
                logging.info(f"param2: {param2}")
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return real_decorator

class DecoratorClass:
    """class-based decorator."""
    def __init__(self, func: F) -> None:
        self.func = func
        wraps(func)(self)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        logging.info("before function call")
        result = self.func(*args, **kwargs)
        logging.info("after function call")
        return result
    
    def __get__(self, obj: Any, objtype: Any) -> Callable[..., Any]:
        """support instance methods."""
        if obj is None:
            return self
        return partial(self.__call__, obj)

class DecoratorWithContext:
    """decorator with context manager support."""
    def __init__(self, func: F) -> None:
        self.func = func
        wraps(func)(self)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self:
            return self.func(*args, **kwargs)
    
    def __enter__(self) -> 'DecoratorWithContext':
        logging.info("entering context")
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        logging.info("exiting context")

def aspect_decorator(
    before: Optional[Callable[..., Any]] = None,
    after: Optional[Callable[..., Any]] = None,
    around: Optional[Callable[..., Any]] = None
) -> Callable[[F], F]:
    """decorator implementing aspect-oriented programming."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # before advice
            if before:
                before(*args, **kwargs)
            
            # around advice
            if around:
                result = around(func, *args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # after advice
            if after:
                after(result)
            
            return result
        return cast(F, wrapper)
    return decorator

@dataclass
class Event:
    """event data class."""
    name: str
    data: Any
    timestamp: datetime = datetime.now()

class Observable(ABC):
    """abstract base class for observable objects."""
    def __init__(self) -> None:
        self._observers: Dict[str, List[Callable[[Event], None]]] = {}
    
    def add_observer(
        self,
        event_type: str,
        observer: Callable[[Event], None]
    ) -> None:
        """add observer for event type."""
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)
    
    def notify_observers(self, event: Event) -> None:
        """notify observers of event."""
        for observer in self._observers.get(event_type, []):
            observer(event)

def observe(*event_types: str) -> Callable[[F], F]:
    """decorator to make methods observable."""
    def decorator(method: F) -> F:
        @wraps(method)
        def wrapper(self: Observable, *args: Any, **kwargs: Any) -> Any:
            # create before event
            before_event = Event(
                f"before_{method.__name__}",
                {"args": args, "kwargs": kwargs}
            )
            self.notify_observers(before_event)
            
            # call method
            result = method(self, *args, **kwargs)
            
            # create after event
            after_event = Event(
                f"after_{method.__name__}",
                {"result": result}
            )
            self.notify_observers(after_event)
            
            return result
        return cast(F, wrapper)
    return decorator

# example usage
@compose(
    parametric_decorator(param1="value1"),
    DecoratorClass
)
def combined_example(x: int) -> int:
    """function with combined decorators."""
    return x * 2

@DecoratorWithContext
def context_example() -> str:
    """function with context manager decorator."""
    return "example with context"

def log_before(*args: Any, **kwargs: Any) -> None:
    """before advice function."""
    logging.info("before function call")

def log_after(result: Any) -> None:
    """after advice function."""
    logging.info(f"after function call, result: {result}")

def log_around(
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any
) -> Any:
    """around advice function."""
    logging.info("before function call (around)")
    result = func(*args, **kwargs)
    logging.info("after function call (around)")
    return result

@aspect_decorator(
    before=log_before,
    after=log_after,
    around=log_around
)
def aspect_example(x: int) -> int:
    """function with aspect-oriented decorator."""
    return x * 2

class DataProcessor(Observable):
    """class demonstrating observable methods."""
    def __init__(self, data: list):
        super().__init__()
        self.data = data
    
    @observe("process")
    def process_data(self) -> list:
        """process data with observable events."""
        return [x * 2 for x in self.data]

def main():
    """demonstrate advanced decorator patterns."""
    # 1. composed decorators
    print("1. testing composed decorators:")
    result = combined_example(5)
    print(f"result: {result}")
    
    # 2. context manager decorator
    print("\n2. testing context manager decorator:")
    result = context_example()
    print(f"result: {result}")
    
    # 3. aspect-oriented decorator
    print("\n3. testing aspect-oriented decorator:")
    result = aspect_example(5)
    print(f"result: {result}")
    
    # 4. observable decorator
    print("\n4. testing observable decorator:")
    processor = DataProcessor([1, 2, 3])
    
    def log_event(event: Event) -> None:
        logging.info(f"event: {event.name}, data: {event.data}")
    
    processor.add_observer("process", log_event)
    result = processor.process_data()
    print(f"result: {result}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a decorator pattern that:
#    - implements dependency injection
#    - manages object lifecycle
#    - supports circular dependencies
#    - handles dependency resolution

# 2. create a decorator pattern that:
#    - implements state machine
#    - manages state transitions
#    - validates state changes
#    - supports event handling

# 3. create a decorator pattern that:
#    - implements plugin system
#    - manages plugin registration
#    - handles plugin dependencies
#    - supports plugin versioning 