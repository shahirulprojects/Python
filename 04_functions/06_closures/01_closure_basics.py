# function closures and scoping in python
# this file explains how functions can capture and remember their environment

# 1. understanding closures
# a closure is a function that remembers values from its enclosing scope

def create_multiplier(factor):
    """
    creates a function that multiplies by a specific factor
    
    args:
        factor (number): the multiplication factor
    
    returns:
        function: a function that multiplies by factor
    """
    # inner function has access to factor
    def multiplier(x):
        # uses factor from outer scope
        return x * factor
    
    return multiplier

# creating specific multipliers
double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))    # prints: 10
print(triple(5))    # prints: 15

# 2. closures with state
def create_counter():
    """
    creates a counter that remembers its state
    
    returns:
        function: a function that counts up
    """
    count = 0    # this value is remembered
    
    def counter():
        # uses nonlocal to modify outer variable
        nonlocal count
        count += 1
        return count
    
    return counter

# create two independent counters
counter1 = create_counter()
counter2 = create_counter()

print(counter1())    # prints: 1
print(counter1())    # prints: 2
print(counter2())    # prints: 1 (separate count)

# 3. understanding variable scope
x = 10    # global variable

def outer_function():
    x = 20    # outer function's local variable
    
    def inner_function():
        x = 30    # inner function's local variable
        print(f"inner x: {x}")
    
    inner_function()
    print(f"outer x: {x}")

outer_function()
print(f"global x: {x}")

# 4. modifying outer scope variables
def create_accumulator():
    """
    creates an accumulator that adds numbers
    
    returns:
        tuple: (add_function, get_total_function)
    """
    total = 0
    
    def add(x):
        # modifies the outer total
        nonlocal total
        total += x
    
    def get_total():
        # accesses but doesn't modify total
        return total
    
    return add, get_total

# using the accumulator
add, get_total = create_accumulator()
add(5)
add(3)
print(get_total())    # prints: 8

# 5. practical examples

# creating a logger with configurable prefix
def create_logger(prefix):
    """
    creates a logging function with a fixed prefix
    
    args:
        prefix (str): prefix for log messages
    
    returns:
        function: configured logging function
    """
    def log(message):
        print(f"[{prefix}] {message}")
    
    return log

# create specific loggers
error_logger = create_logger("ERROR")
info_logger = create_logger("INFO")

error_logger("something went wrong")
info_logger("operation completed")

# creating a rate limiter
import time

def create_rate_limiter(max_calls, time_window):
    """
    creates a rate limiter that allows max_calls in time_window seconds
    
    args:
        max_calls (int): maximum number of allowed calls
        time_window (float): time window in seconds
    
    returns:
        function: rate-limited function wrapper
    """
    calls = []    # list to track call timestamps
    
    def rate_limit(func):
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            # remove old calls
            while calls and current_time - calls[0] > time_window:
                calls.pop(0)
            
            # check if we can make a new call
            if len(calls) < max_calls:
                calls.append(current_time)
                return func(*args, **kwargs)
            else:
                return "rate limit exceeded"
        
        return wrapper
    
    return rate_limit

# example usage
@create_rate_limiter(max_calls=2, time_window=1)
def make_request(url):
    return f"requesting {url}"

# test rate limiting
print(make_request("example.com"))    # works
print(make_request("example.com"))    # works
print(make_request("example.com"))    # rate limited

# 6. advanced closure patterns

# creating a memoization decorator with timeout
def memoize_with_timeout(timeout):
    """
    creates a memoization decorator with result timeout
    
    args:
        timeout (float): how long to cache results (seconds)
    """
    def decorator(func):
        cache = {}    # stores results and timestamps
        
        def wrapper(*args):
            current_time = time.time()
            
            # clear expired results
            expired = [k for k, v in cache.items()
                      if current_time - v[1] > timeout]
            for k in expired:
                del cache[k]
            
            # check cache or compute
            if args not in cache:
                result = func(*args)
                cache[args] = (result, current_time)
                return result
            
            return cache[args][0]
        
        return wrapper
    return decorator

# example usage
@memoize_with_timeout(timeout=5)
def expensive_operation(x):
    print(f"computing for {x}...")
    time.sleep(1)    # simulate expensive computation
    return x * x

print(expensive_operation(4))    # computes
print(expensive_operation(4))    # uses cache
time.sleep(6)    # wait for timeout
print(expensive_operation(4))    # computes again

# 7. closure-based state machines
def create_state_machine():
    """
    creates a simple state machine using closures
    """
    state = "start"
    
    def transition(action):
        nonlocal state
        
        if state == "start":
            if action == "begin":
                state = "running"
                return "started machine"
        elif state == "running":
            if action == "pause":
                state = "paused"
                return "machine paused"
            elif action == "stop":
                state = "stopped"
                return "machine stopped"
        elif state == "paused":
            if action == "resume":
                state = "running"
                return "machine resumed"
            elif action == "stop":
                state = "stopped"
                return "machine stopped"
        
        return f"invalid action {action} for state {state}"
    
    def get_state():
        return state
    
    return transition, get_state

# using the state machine
transition, get_state = create_state_machine()
print(get_state())                # start
print(transition("begin"))        # started machine
print(transition("pause"))        # machine paused
print(transition("resume"))       # machine resumed
print(transition("stop"))         # machine stopped 