# understanding python exceptions and error handling
# this module covers the fundamentals of handling errors in python programs

from typing import Any, Optional, Union, List
import sys

def divide_numbers(a: Union[int, float], b: Union[int, float]) -> Optional[float]:
    """performs division of two numbers with careful error handling
    
    why we need this:
    when dividing numbers, several things can go wrong:
    - division by zero (mathematically impossible)
    - trying to divide non-numeric values
    - other unexpected errors
    
    parameters:
        a: the number to be divided (dividend)
        b: the number to divide by (divisor)
    
    returns:
        the result of division if successful, None if an error occurs
    
    examples:
        divide_numbers(10, 2)  -> returns 5.0
        divide_numbers(10, 0)  -> returns None (can't divide by zero)
        divide_numbers('10', 2) -> returns None (invalid type)
    """
    try:
        # attempt the division operation
        result = a / b
        return result
    except ZeroDivisionError:
        # handles the case when someone tries to divide by zero
        print("error: cannot divide by zero :( this is mathematically impossible")
        return None
    except TypeError as e:
        # handles cases where the input types are not numbers
        print(f"error: oops, looks like you're not using numbers - {e}")
        return None

def access_list_element(lst: List[Any], index: int) -> Optional[Any]:
    """safely retrieves an element from a list with error protection
    
    why we need this:
    when accessing list elements, common errors include:
    - trying to access an index beyond the list's size
    - using wrong types for indexing (like strings instead of integers)
    
    parameters:
        lst: the list to access elements from
        index: the position of the element we want (starting from 0)
    
    returns:
        the element at the specified index if found, None if an error occurs
    
    examples:
        numbers = [1, 2, 3]
        access_list_element(numbers, 1)  -> returns 2
        access_list_element(numbers, 5)  -> returns None (index too large)
        access_list_element(numbers, '1') -> returns None (wrong index type)
    """
    try:
        return lst[index]
    except IndexError:
        # handles attempts to access elements beyond the list's size
        print(f"error: whoops, index {index} is too large for this list :( the list only has {len(lst)} elements")
        return None
    except TypeError:
        # handles cases where the index is not an integer
        print("error: hey, we need a number to access list elements :D try using an integer")
        return None

def parse_string_to_int(value: str) -> Optional[int]:
    """convert string to integer with error handling."""
    try:
        return int(value)
    except ValueError:
        print(f"error: '{value}' cannot be converted to integer")
        return None

def read_file_content(filename: str) -> Optional[str]:
    """read file content with error handling."""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"error: file '{filename}' not found")
        return None
    except PermissionError:
        print(f"error: no permission to read '{filename}'")
        return None
    except IOError as e:
        print(f"error: failed to read file - {e}")
        return None

def process_data(data: Any) -> Optional[str]:
    """process data with multiple error handling."""
    try:
        # attempt multiple operations that might fail
        if len(data) == 0:
            raise ValueError("empty data")
        
        result = str(data).upper()
        return result
    except TypeError:
        print("error: data cannot be processed")
        return None
    except ValueError as e:
        print(f"error: {e}")
        return None
    except Exception as e:
        print(f"unexpected error: {e}")
        return None

def demonstrate_finally():
    """demonstrate finally block usage."""
    resource = None
    try:
        resource = open("temp.txt", "w")
        resource.write("test data")
    except IOError as e:
        print(f"error writing to file: {e}")
    finally:
        # cleanup code that always runs
        if resource:
            resource.close()
            print("file closed in finally block")

def demonstrate_else():
    """demonstrate else block in exception handling."""
    try:
        value = int(input("enter a number: "))
    except ValueError:
        print("that's not a valid number")
    else:
        # runs only if no exception occurred
        print(f"you entered: {value}")

def get_exception_info(code: str) -> dict:
    """get detailed exception information."""
    try:
        exec(code)
    except Exception as e:
        return {
            'type': type(e).__name__,
            'message': str(e),
            'module': e.__class__.__module__,
            'traceback': {
                'filename': sys.exc_info()[2].tb_frame.f_code.co_filename,
                'line': sys.exc_info()[2].tb_lineno
            }
        }
    return {}

# example usage
def main():
    """demonstrate basic exception handling."""
    print("1. division with error handling:")
    print(f"10 / 2 = {divide_numbers(10, 2)}")
    print(f"10 / 0 = {divide_numbers(10, 0)}")
    print(f"'10' / 2 = {divide_numbers('10', 2)}")
    
    print("\n2. list access with error handling:")
    numbers = [1, 2, 3]
    print(f"numbers[1] = {access_list_element(numbers, 1)}")
    print(f"numbers[5] = {access_list_element(numbers, 5)}")
    print(f"numbers['1'] = {access_list_element(numbers, '1')}")
    
    print("\n3. string parsing with error handling:")
    print(f"parse '123': {parse_string_to_int('123')}")
    print(f"parse 'abc': {parse_string_to_int('abc')}")
    
    print("\n4. file operations with error handling:")
    print(f"read 'nonexistent.txt': {read_file_content('nonexistent.txt')}")
    
    print("\n5. data processing with error handling:")
    print(f"process 'hello': {process_data('hello')}")
    print(f"process None: {process_data(None)}")
    print(f"process '': {process_data('')}")
    
    print("\n6. finally block demonstration:")
    demonstrate_finally()
    
    print("\n7. else block demonstration:")
    demonstrate_else()
    
    print("\n8. exception info:")
    code = "1/0"  # code that will raise an exception
    info = get_exception_info(code)
    print("exception details:")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a calculator program that:
#    - handles division by zero
#    - validates input types
#    - provides helpful error messages
#    - logs errors for debugging

# 2. create a file processor that:
#    - handles multiple file formats
#    - validates file contents
#    - manages resources properly
#    - recovers from errors

# 3. create a data validator that:
#    - checks data types
#    - validates ranges
#    - handles missing values
 