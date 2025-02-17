# advanced closure patterns and techniques in python
# this file explores complex closure patterns, functional programming concepts, and real-world applications

# 1. closure factories (higher-order closures)
def create_validator_factory(validation_type):
    """
    creates specialized validator factories based on type
    
    args:
        validation_type (str): type of validation to create
    
    returns:
        function: a factory function that creates validators
    """
    if validation_type == "range":
        def create_range_validator(min_val, max_val):
            def validate(value):
                return min_val <= value <= max_val
            return validate
        return create_range_validator
    
    elif validation_type == "pattern":
        import re
        def create_pattern_validator(pattern):
            compiled_pattern = re.compile(pattern)
            def validate(value):
                return bool(compiled_pattern.match(str(value)))
            return validate
        return create_pattern_validator

# using the validator factory
range_validator_factory = create_validator_factory("range")
is_valid_age = range_validator_factory(0, 120)
is_valid_percentage = range_validator_factory(0, 100)

pattern_validator_factory = create_validator_factory("pattern")
is_valid_email = pattern_validator_factory(r'^[\w\.-]+@[\w\.-]+\.\w+$')

print(is_valid_age(25))         # prints: True
print(is_valid_age(150))        # prints: False
print(is_valid_email("user@example.com"))  # prints: True

# 2. currying with closures
def curry(func, arity):
    """
    transforms a function into a series of unary functions
    
    args:
        func: the function to curry
        arity (int): number of arguments the function takes
    
    returns:
        function: curried version of the input function
    """
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        
        def inner(*more_args):
            return curried(*(args + more_args))
        return inner
    
    return curried

# example usage of currying
def add_three_numbers(x, y, z):
    return x + y + z

curried_add = curry(add_three_numbers, 3)
print(curried_add(1)(2)(3))      # prints: 6
print(curried_add(1, 2)(3))      # prints: 6
print(curried_add(1)(2, 3))      # prints: 6

# 3. partial application with closures
def partial(func, *fixed_args):
    """
    creates a new function with some arguments fixed
    
    args:
        func: the function to partially apply
        fixed_args: arguments to fix
    
    returns:
        function: partially applied function
    """
    def wrapper(*args, **kwargs):
        return func(*fixed_args, *args, **kwargs)
    return wrapper

# example of partial application
def format_message(prefix, message, suffix):
    return f"{prefix} | {message} | {suffix}"

log_error = partial(format_message, "ERROR", suffix="!")
log_info = partial(format_message, "INFO", suffix=".")

print(log_error("disk full"))     # prints: ERROR | disk full | !
print(log_info("backup complete")) # prints: INFO | backup complete | .

# 4. advanced memoization patterns
def memoize_with_policy():
    """
    creates a memoization decorator with configurable caching policies
    """
    cache = {}
    max_size = 100
    
    def decorator(func):
        def get_cache_key(*args, **kwargs):
            # creates a unique key for the function call
            return (func.__name__, args, frozenset(kwargs.items()))
        
        def wrapper(*args, **kwargs):
            cache_key = get_cache_key(*args, **kwargs)
            
            # implement least recently used (LRU) cache
            if cache_key in cache:
                return cache[cache_key]
            
            # clear cache if it exceeds max size
            if len(cache) >= max_size:
                # remove oldest entry (first key)
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            # compute and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = result
            return result
        
        # add cache inspection methods
        wrapper.cache_info = lambda: {
            "size": len(cache),
            "max_size": max_size,
            "hits": sum(1 for k in cache if k[0] == func.__name__)
        }
        
        wrapper.clear_cache = lambda: cache.clear()
        
        return wrapper
    return decorator

# example usage of advanced memoization
@memoize_with_policy()
def fibonacci(n):
    """calculates the nth fibonacci number"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))               # computes
print(fibonacci(10))               # uses cache
print(fibonacci.cache_info())      # prints cache stats

# 5. context-preserving closures
def preserve_context(context_key):
    """
    creates a closure that preserves context across function calls
    
    args:
        context_key: key to identify the context
    
    returns:
        tuple: (set_context, get_context, with_context decorator)
    """
    context_data = {}
    
    def set_context(value):
        context_data[context_key] = value
    
    def get_context():
        return context_data.get(context_key)
    
    def with_context(func):
        def wrapper(*args, **kwargs):
            # preserve original context
            original_context = get_context()
            try:
                return func(*args, **kwargs)
            finally:
                # restore original context
                if original_context is not None:
                    set_context(original_context)
                else:
                    context_data.pop(context_key, None)
        return wrapper
    
    return set_context, get_context, with_context

# example of context preservation
set_user, get_user, with_user_context = preserve_context("current_user")

@with_user_context
def perform_action():
    current_user = get_user()
    return f"action performed by {current_user}"

# using the context
set_user("alice")
print(perform_action())    # prints: action performed by alice
print(get_user())         # prints: alice

# 6. event emitter with closures
def create_event_emitter():
    """
    creates a simple event emitter using closures
    
    returns:
        tuple: (on, emit, off) functions for event handling
    """
    listeners = {}
    
    def on(event, callback):
        """registers an event listener"""
        if event not in listeners:
            listeners[event] = []
        listeners[event].append(callback)
        
        # return unsubscribe function
        def unsubscribe():
            off(event, callback)
        return unsubscribe
    
    def emit(event, *args, **kwargs):
        """emits an event with data"""
        if event in listeners:
            # create a copy to allow listeners to unsubscribe during iteration
            for callback in listeners[event][:]:
                callback(*args, **kwargs)
    
    def off(event, callback):
        """removes an event listener"""
        if event in listeners:
            listeners[event] = [cb for cb in listeners[event] if cb != callback]
            if not listeners[event]:
                del listeners[event]
    
    return on, emit, off

# using the event emitter
on, emit, off = create_event_emitter()

def handle_user_login(user):
    print(f"user {user} logged in")

def log_event(user):
    print(f"logging login event for {user}")

# register listeners
unsubscribe = on("login", handle_user_login)
on("login", log_event)

# emit event
emit("login", "bob")      # triggers both listeners

# unsubscribe one listener
unsubscribe()
emit("login", "alice")    # triggers only log_event 