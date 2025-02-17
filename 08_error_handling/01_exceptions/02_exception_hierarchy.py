# understanding python's exception hierarchy
# this module explores how exceptions are organized in python's class hierarchy

from typing import List, Dict, Any
import sys

def explore_exception_hierarchy() -> Dict[str, List[str]]:
    """explores and demonstrates python's built-in exception hierarchy
    
    why we need this:
    understanding the exception hierarchy helps us:
    - catch the right types of exceptions
    - write more specific error handling code
    - create our own custom exceptions that fit into the hierarchy
    
    returns:
        a dictionary mapping exception categories to their common examples
    """
    # built-in exceptions are organized in a hierarchy
    exception_categories = {
        'arithmetic_errors': [
            'ZeroDivisionError',   # when dividing by zero
            'OverflowError',       # when a calculation is too large
            'FloatingPointError'   # for floating-point calculation errors
        ],
        'lookup_errors': [
            'KeyError',           # when a dictionary key isn't found
            'IndexError',         # when a sequence index is out of range
            'AttributeError'      # when an attribute/method doesn't exist
        ],
        'type_errors': [
            'TypeError',          # when an operation has incompatible types
            'ValueError'          # when an operation has invalid values
        ],
        'io_errors': [
            'FileNotFoundError',  # when a file doesn't exist
            'PermissionError',    # when we lack file access permissions
            'IOError'            # base class for input/output errors
        ]
    }
    return exception_categories

def demonstrate_exception_inheritance():
    """shows how exception inheritance works in practice
    
    why this matters:
    when we catch exceptions, we can:
    - catch specific exceptions for precise handling
    - catch parent exceptions to handle multiple related errors
    """
    try:
        # this will raise a FileNotFoundError
        with open('nonexistent.txt') as f:
            content = f.read()
    except OSError as e:
        # catches FileNotFoundError because it inherits from OSError :D
        print(f"caught a file system error: {e}")
        print(f"specific error type: {type(e).__name__}")

def show_exception_details(exception_type: type) -> Dict[str, Any]:
    """explores the details of a specific exception type
    
    parameters:
        exception_type: the exception class to examine
    
    returns:
        dictionary containing details about the exception
    """
    return {
        'name': exception_type.__name__,
        'parent': exception_type.__base__.__name__,
        'module': exception_type.__module__,
        'doc': exception_type.__doc__
    }

def main():
    """demonstrates the exception hierarchy concepts"""
    # show the main exception categories
    categories = explore_exception_hierarchy()
    print("python's exception categories:")
    for category, exceptions in categories.items():
        print(f"\n{category}:")
        for exc in exceptions:
            print(f"  - {exc}")
    
    # demonstrate exception inheritance
    print("\ndemonstrating exception inheritance:")
    demonstrate_exception_inheritance()
    
    # show details of some common exceptions
    print("\nexception details:")
    for exc in [ValueError, TypeError, IndexError]:
        details = show_exception_details(exc)
        print(f"\n{details['name']}:")
        print(f"  parent: {details['parent']}")
        print(f"  module: {details['module']}")
        print(f"  description: {details['doc']}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that demonstrates catching multiple exception types:
#    - try different arithmetic operations
#    - catch specific exceptions first
#    - then catch their parent exceptions
#    - observe how inheritance affects which except block is executed

# 2. explore the exception hierarchy:
#    - create a function that raises different types of exceptions
#    - catch them at different levels of the hierarchy
#    - document what you learn about exception inheritance

# 3. create a custom exception hierarchy:
#    - define a base exception for your application
#    - create specific exceptions that inherit from it
#    - demonstrate how to use them effectively 