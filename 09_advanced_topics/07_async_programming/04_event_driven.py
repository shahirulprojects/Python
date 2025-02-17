import asyncio
from typing import Any, Dict, List, Optional, Set, Callable
from dataclasses import dataclass
from datetime import datetime
import logging
from contextlib import asynccontextmanager
import random
import json

# welcome to event-driven programming! here we'll learn how to build systems
# that react to events and handle them asynchronously :D

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 1. event emitter - base class for event-driven objects
class EventEmitter:
    def __init__(self):
        self._handlers: Dict[str, Set[Callable]] = {}
    
    def on(self, event: str, handler: Callable) -> None:
        if event not in self._handlers:
            self._handlers[event] = set()
        self._handlers[event].add(handler)
    
    def off(self, event: str, handler: Callable) -> None:
        if event in self._handlers:
            self._handlers[event].discard(handler)
    
    async def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        if event in self._handlers:
            for handler in self._handlers[event]:
                # run handlers concurrently
                await asyncio.create_task(handler(*args, **kwargs))

# 2. event bus - central event dispatcher
class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, Set[Callable]] = {}
        self._middleware: List[Callable] = []
    
    def subscribe(self, event: str, handler: Callable) -> None:
        if event not in self._subscribers:
            self._subscribers[event] = set()
        self._subscribers[event].add(handler)
    
    def unsubscribe(self, event: str, handler: Callable) -> None:
        if event in self._subscribers:
            self._subscribers[event].discard(handler)
    
    def add_middleware(self, middleware: Callable) -> None:
        self._middleware.append(middleware)
    
    async def publish(self, event: str, data: Any = None) -> None:
        # create event object
        event_obj = {
            'type': event,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # apply middleware
        for middleware in self._middleware:
            event_obj = await middleware(event_obj)
            if event_obj is None:
                return
        
        # notify subscribers
        if event in self._subscribers:
            await asyncio.gather(*(
                handler(event_obj)
                for handler in self._subscribers[event]
            ))

# 3. reactive stream - processes events as a stream
class ReactiveStream:
    def __init__(self):
        self._observers: Set[Callable] = set()
        self._operators: List[Callable] = []
    
    def subscribe(self, observer: Callable) -> None:
        self._observers.add(observer)
    
    def pipe(self, operator: Callable) -> ReactiveStream:
        self._operators.append(operator)
        return self
    
    async def next(self, value: Any) -> None:
        # apply operators
        processed = value
        for op in self._operators:
            processed = await op(processed)
            if processed is None:
                return
        
        # notify observers
        await asyncio.gather(*(
            observer(processed)
            for observer in self._observers
        ))
    
    async def error(self, error: Exception) -> None:
        for observer in self._observers:
            if hasattr(observer, 'error'):
                await observer.error(error)
    
    async def complete(self) -> None:
        for observer in self._observers:
            if hasattr(observer, 'complete'):
                await observer.complete()

# 4. event sourcing - stores history of events
@dataclass
class Event:
    type: str
    data: Any
    timestamp: datetime
    version: int

class EventStore:
    def __init__(self):
        self._events: List[Event] = []
        self._handlers: Dict[str, List[Callable]] = {}
        self._version = 0
    
    def register_handler(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def append(self, event_type: str, data: Any) -> None:
        # create new event
        event = Event(
            type=event_type,
            data=data,
            timestamp=datetime.now(),
            version=self._version + 1
        )
        
        # store event
        self._events.append(event)
        self._version += 1
        
        # process event
        if event_type in self._handlers:
            await asyncio.gather(*(
                handler(event)
                for handler in self._handlers[event_type]
            ))
    
    def get_events(self, since_version: int = 0) -> List[Event]:
        return [
            event for event in self._events
            if event.version > since_version
        ]

# 5. event-driven state machine
class StateMachine(EventEmitter):
    def __init__(self, initial_state: str):
        super().__init__()
        self._state = initial_state
        self._transitions: Dict[str, Dict[str, str]] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def add_transition(
        self,
        event: str,
        from_state: str,
        to_state: str
    ) -> None:
        if from_state not in self._transitions:
            self._transitions[from_state] = {}
        self._transitions[from_state][event] = to_state
    
    def add_handler(self, state: str, handler: Callable) -> None:
        self._handlers[state] = handler
    
    async def trigger(self, event: str) -> None:
        if (
            self._state in self._transitions
            and event in self._transitions[self._state]
        ):
            old_state = self._state
            new_state = self._transitions[self._state][event]
            
            # transition to new state
            self._state = new_state
            
            # emit state change event
            await self.emit('state_changed', {
                'from': old_state,
                'to': new_state,
                'event': event
            })
            
            # run state handler
            if new_state in self._handlers:
                await self._handlers[new_state]()

# now let's see these patterns in action
async def example_event_driven():
    # example 1: event emitter
    print("event emitter example:")
    emitter = EventEmitter()
    
    async def on_message(msg: str):
        logging.info(f"received message: {msg}")
    
    emitter.on('message', on_message)
    await emitter.emit('message', "hello world")
    
    # example 2: event bus
    print("\nevent bus example:")
    bus = EventBus()
    
    # add logging middleware
    async def log_middleware(event: dict) -> dict:
        logging.info(f"event: {event}")
        return event
    
    bus.add_middleware(log_middleware)
    
    # add subscriber
    async def handle_user_event(event: dict):
        logging.info(f"handling user event: {event}")
    
    bus.subscribe('user', handle_user_event)
    await bus.publish('user', {'action': 'login'})
    
    # example 3: reactive stream
    print("\nreactive stream example:")
    stream = ReactiveStream()
    
    # add operator
    async def filter_even(value: int) -> Optional[int]:
        return value if value % 2 == 0 else None
    
    # add observer
    async def print_value(value: int):
        logging.info(f"value: {value}")
    
    stream.pipe(filter_even).subscribe(print_value)
    
    for i in range(5):
        await stream.next(i)
    
    # example 4: event store
    print("\nevent store example:")
    store = EventStore()
    
    # register event handler
    async def handle_order_created(event: Event):
        logging.info(f"processing order: {event.data}")
    
    store.register_handler('order_created', handle_order_created)
    
    # append events
    await store.append('order_created', {
        'id': '123',
        'items': ['item1', 'item2']
    })
    
    # example 5: state machine
    print("\nstate machine example:")
    machine = StateMachine('idle')
    
    # define states and transitions
    machine.add_transition('start', 'idle', 'running')
    machine.add_transition('pause', 'running', 'paused')
    machine.add_transition('resume', 'paused', 'running')
    machine.add_transition('stop', 'running', 'idle')
    
    # add state handlers
    async def on_running():
        logging.info("machine is running")
    
    async def on_paused():
        logging.info("machine is paused")
    
    machine.add_handler('running', on_running)
    machine.add_handler('paused', on_paused)
    
    # add state change listener
    async def on_state_changed(change: dict):
        logging.info(
            f"state changed from {change['from']} to {change['to']}"
        )
    
    machine.on('state_changed', on_state_changed)
    
    # trigger transitions
    await machine.trigger('start')
    await machine.trigger('pause')
    await machine.trigger('resume')
    await machine.trigger('stop')

async def main():
    try:
        await example_event_driven()
    except Exception as e:
        logging.error(f"error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# practice exercises:
# 1. implement a pub/sub system that:
#    - supports topic wildcards
#    - handles backpressure
#    - provides message persistence

# 2. create an event sourcing system that:
#    - implements event versioning
#    - supports snapshots
#    - handles concurrent updates

# 3. implement a reactive pipeline that:
#    - supports multiple operators
#    - handles error propagation
#    - provides backpressure control 