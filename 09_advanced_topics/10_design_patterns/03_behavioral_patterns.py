from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Set
from dataclasses import dataclass
import random
from datetime import datetime
import asyncio
import logging

# welcome to behavioral patterns! these patterns are all about communication
# between objects, assigning responsibilities, and defining algorithms :D

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 1. observer pattern - defines one-to-many dependency between objects
class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass

class Subject:
    def __init__(self):
        self._observers: Set[Observer] = set()
        self._state: Any = None
    
    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.discard(observer)
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self) -> Any:
        return self._state
    
    @state.setter
    def state(self, value: Any) -> None:
        self._state = value
        self.notify()

class ConcreteObserver:
    def __init__(self, name: str):
        self.name = name
    
    def update(self, subject: Subject) -> None:
        logging.info(
            f"observer {self.name} received update: {subject.state}"
        )

# 2. strategy pattern - defines family of interchangeable algorithms
class Strategy(Protocol):
    def execute(self, data: List[int]) -> List[int]:
        pass

class BubbleSortStrategy:
    def execute(self, data: List[int]) -> List[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

class QuickSortStrategy:
    def execute(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        else:
            pivot = data[0]
            less = [x for x in data[1:] if x <= pivot]
            greater = [x for x in data[1:] if x > pivot]
            return self.execute(less) + [pivot] + self.execute(greater)

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    
    @property
    def strategy(self) -> Strategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy
    
    def execute_strategy(self, data: List[int]) -> List[int]:
        return self._strategy.execute(data)

# 3. command pattern - encapsulates request as an object
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

class Editor:
    def __init__(self):
        self.text = ""
    
    def get_text(self) -> str:
        return self.text
    
    def set_text(self, text: str) -> None:
        self.text = text

class InsertTextCommand(Command):
    def __init__(self, editor: Editor, text: str):
        self.editor = editor
        self.text = text
        self.backup = ""
    
    def execute(self) -> None:
        self.backup = self.editor.get_text()
        self.editor.set_text(self.backup + self.text)
    
    def undo(self) -> None:
        self.editor.set_text(self.backup)

class CommandHistory:
    def __init__(self):
        self._history: List[Command] = []
    
    def push(self, command: Command) -> None:
        self._history.append(command)
    
    def pop(self) -> Optional[Command]:
        return self._history.pop() if self._history else None

# 4. state pattern - allows object to alter behavior when state changes
class State(ABC):
    @abstractmethod
    def handle(self) -> str:
        pass

class Context:
    def __init__(self, state: State):
        self._state = state
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, state: State) -> None:
        logging.info(f"context: transitioning to {type(state).__name__}")
        self._state = state
    
    def request(self) -> str:
        return self._state.handle()

class ConcreteStateA(State):
    def handle(self) -> str:
        return "handling state a"

class ConcreteStateB(State):
    def handle(self) -> str:
        return "handling state b"

# 5. chain of responsibility pattern - passes request along chain of handlers
class Handler(ABC):
    def __init__(self, next_handler: Optional[Handler] = None):
        self._next_handler = next_handler
    
    def handle(self, request: str) -> Optional[str]:
        result = self.process_request(request)
        if result is None and self._next_handler:
            return self._next_handler.handle(request)
        return result
    
    @abstractmethod
    def process_request(self, request: str) -> Optional[str]:
        pass

class AuthenticationHandler(Handler):
    def process_request(self, request: str) -> Optional[str]:
        if "auth" in request:
            return "authenticated request"
        return None

class ValidationHandler(Handler):
    def process_request(self, request: str) -> Optional[str]:
        if "validate" in request:
            return "validated request"
        return None

class ProcessingHandler(Handler):
    def process_request(self, request: str) -> Optional[str]:
        return f"processed: {request}"

# 6. mediator pattern - reduces chaotic dependencies between objects
class Mediator(Protocol):
    def notify(self, sender: Any, event: str) -> None:
        pass

class ConcreteMediator:
    def __init__(self):
        self.component1: Optional[Component1] = None
        self.component2: Optional[Component2] = None
    
    def notify(self, sender: Any, event: str) -> None:
        if event == "A":
            if self.component2:
                self.component2.do_c()
        elif event == "B":
            if self.component1:
                self.component1.do_b()
                if self.component2:
                    self.component2.do_c()

class BaseComponent:
    def __init__(self, mediator: Optional[Mediator] = None):
        self._mediator = mediator
    
    @property
    def mediator(self) -> Mediator:
        return self._mediator
    
    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

class Component1(BaseComponent):
    def do_a(self) -> None:
        logging.info("component 1 does a")
        self.mediator.notify(self, "A")
    
    def do_b(self) -> None:
        logging.info("component 1 does b")

class Component2(BaseComponent):
    def do_c(self) -> None:
        logging.info("component 2 does c")

async def main():
    # example 1: observer
    print("observer pattern:")
    subject = Subject()
    
    observer1 = ConcreteObserver("one")
    observer2 = ConcreteObserver("two")
    
    subject.attach(observer1)
    subject.attach(observer2)
    
    subject.state = "new state"
    
    # example 2: strategy
    print("\nstrategy pattern:")
    data = [64, 34, 25, 12, 22, 11, 90]
    
    context = Context(BubbleSortStrategy())
    result1 = context.execute_strategy(data)
    print(f"bubble sort: {result1}")
    
    context.strategy = QuickSortStrategy()
    result2 = context.execute_strategy(data)
    print(f"quick sort: {result2}")
    
    # example 3: command
    print("\ncommand pattern:")
    editor = Editor()
    history = CommandHistory()
    
    # execute commands
    command1 = InsertTextCommand(editor, "hello ")
    command1.execute()
    history.push(command1)
    
    command2 = InsertTextCommand(editor, "world")
    command2.execute()
    history.push(command2)
    
    print(f"text after commands: {editor.get_text()}")
    
    # undo last command
    if last_command := history.pop():
        last_command.undo()
        print(f"text after undo: {editor.get_text()}")
    
    # example 4: state
    print("\nstate pattern:")
    context = Context(ConcreteStateA())
    print(context.request())
    
    context.state = ConcreteStateB()
    print(context.request())
    
    # example 5: chain of responsibility
    print("\nchain of responsibility pattern:")
    chain = AuthenticationHandler(
        ValidationHandler(
            ProcessingHandler()
        )
    )
    
    print(chain.handle("auth request"))
    print(chain.handle("validate request"))
    print(chain.handle("normal request"))
    
    # example 6: mediator
    print("\nmediator pattern:")
    mediator = ConcreteMediator()
    component1 = Component1()
    component2 = Component2()
    
    mediator.component1 = component1
    mediator.component2 = component2
    component1.mediator = mediator
    component2.mediator = mediator
    
    component1.do_a()

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. implement a memento pattern that:
#    - saves and restores object state
#    - handles complex objects
#    - manages history

# 2. create a visitor pattern that:
#    - processes heterogeneous object structures
#    - implements double dispatch
#    - separates algorithms from objects

# 3. implement an interpreter pattern that:
#    - parses and executes expressions
#    - supports custom grammar
#    - handles operator precedence 