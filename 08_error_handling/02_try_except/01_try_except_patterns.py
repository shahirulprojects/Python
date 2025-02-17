# try-except patterns and context managers in python
from typing import Any, Optional, Generator, TextIO
from contextlib import contextmanager
import time
import logging
from datetime import datetime
import traceback
import sys

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RetryError(Exception):
    """custom error for retry failures."""
    pass

@contextmanager
def timer():
    """context manager to measure execution time."""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"execution time: {end - start:.2f} seconds")

@contextmanager
def error_logger(operation: str):
    """context manager for logging errors."""
    try:
        yield
    except Exception as e:
        logging.error(f"error during {operation}: {str(e)}")
        raise

@contextmanager
def file_handler(filename: str, mode: str = 'r') -> Generator[TextIO, None, None]:
    """context manager for file handling."""
    file = None
    try:
        file = open(filename, mode)
        yield file
    finally:
        if file:
            file.close()

def retry_operation(max_attempts: int = 3, delay: float = 1.0):
    """decorator for retrying failed operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logging.warning(
                        f"attempt {attempt + 1}/{max_attempts} failed: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise RetryError(f"operation failed after {max_attempts} attempts") from last_error
        return wrapper
    return decorator

def handle_multiple_exceptions(value: Any) -> Optional[str]:
    """demonstrate handling multiple exceptions."""
    try:
        # attempt risky operations
        result = str(value).upper()
        int(result)  # try to convert to integer
        return result
    except (TypeError, ValueError) as e:
        # handle multiple exception types
        logging.error(f"conversion error: {str(e)}")
        return None
    except Exception as e:
        # catch-all for unexpected errors
        logging.error(f"unexpected error: {str(e)}")
        return None

def nested_exception_handling(data: Any) -> Optional[str]:
    """demonstrate nested exception handling."""
    try:
        # outer try block
        result = str(data)
        try:
            # inner try block
            if len(result) == 0:
                raise ValueError("empty string")
            return result.upper()
        except ValueError as e:
            logging.warning(f"inner operation failed: {str(e)}")
            return None
    except Exception as e:
        logging.error(f"outer operation failed: {str(e)}")
        return None

def exception_chaining():
    """demonstrate exception chaining."""
    try:
        try:
            raise ValueError("original error")
        except ValueError as e:
            raise RuntimeError("subsequent error") from e
    except RuntimeError as e:
        print(f"error chain: {e.__cause__}")

def get_full_traceback():
    """get formatted traceback information."""
    try:
        raise ValueError("sample error")
    except Exception:
        return {
            'traceback': traceback.format_exc(),
            'stack': traceback.extract_stack(),
            'frame': sys._getframe()
        }

@retry_operation(max_attempts=3)
def unstable_operation():
    """simulate an unstable operation."""
    if time.time() % 2 > 1:  # randomly fail
        raise ConnectionError("network error")
    return "operation successful"

# example usage
def main():
    """demonstrate try-except patterns."""
    print("1. using timer context manager:")
    with timer():
        time.sleep(1)  # simulate work
    
    print("\n2. using error logger:")
    try:
        with error_logger("data processing"):
            raise ValueError("invalid data")
    except Exception as e:
        print(f"caught error: {e}")
    
    print("\n3. using file handler:")
    try:
        with file_handler("test.txt", 'w') as f:
            f.write("test data")
    except IOError as e:
        print(f"file operation failed: {e}")
    
    print("\n4. handling multiple exceptions:")
    print(handle_multiple_exceptions("123"))  # valid case
    print(handle_multiple_exceptions(None))   # TypeError case
    print(handle_multiple_exceptions("abc"))  # ValueError case
    
    print("\n5. nested exception handling:")
    print(nested_exception_handling("hello"))  # valid case
    print(nested_exception_handling(""))      # inner exception case
    print(nested_exception_handling(None))    # outer exception case
    
    print("\n6. exception chaining:")
    exception_chaining()
    
    print("\n7. getting traceback info:")
    info = get_full_traceback()
    print("traceback information:")
    print(info['traceback'])
    
    print("\n8. retry operation:")
    try:
        result = unstable_operation()
        print(f"result: {result}")
    except RetryError as e:
        print(f"retry failed: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a resource manager that:
#    - handles multiple resource types
#    - ensures proper cleanup
#    - logs resource usage
#    - handles nested resources

# 2. create a retry mechanism that:
#    - supports different retry strategies
#    - handles timeout conditions
#    - provides progress feedback
#    - allows custom error handling

# 3. create an error reporting system that:
#    - captures detailed error context
#    - formats error messages
#    - supports error categorization
#    - integrates with logging 