# basic context managers in python
from typing import Any, Generator, Optional
import logging
from contextlib import contextmanager
import time
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FileHandler:
    """context manager for file handling."""
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """enter the context."""
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """exit the context."""
        if self.file:
            self.file.close()
        return False  # don't suppress exceptions

class Timer:
    """context manager for timing code blocks."""
    def __enter__(self):
        """start timing."""
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """end timing."""
        self.end = time.time()
        self.duration = self.end - self.start
        logging.info(f"time taken: {self.duration:.4f} seconds")
        return False

class LogIndent:
    """context manager for indented logging."""
    _indent = 0
    
    def __enter__(self):
        """increase indent level."""
        LogIndent._indent += 2
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """decrease indent level."""
        LogIndent._indent -= 2
        return False
    
    @classmethod
    def log(cls, msg: str) -> None:
        """log message with current indent."""
        padding = ' ' * cls._indent
        logging.info(f"{padding}{msg}")

class TempFileHandler:
    """context manager for temporary files."""
    def __init__(self, filename: str):
        self.filename = filename
    
    def __enter__(self):
        """create temporary file."""
        self.file = open(self.filename, 'w')
        return self.file
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """clean up temporary file."""
        import os
        self.file.close()
        try:
            os.remove(self.filename)
        except OSError:
            pass
        return False

@contextmanager
def transaction():
    """context manager for transaction-like operations."""
    state = []
    try:
        logging.info("starting transaction")
        yield state
        logging.info("committing transaction")
    except Exception as e:
        logging.error(f"rolling back transaction: {str(e)}")
        raise

@contextmanager
def suppress_errors(*exceptions: type):
    """context manager to suppress specific exceptions."""
    try:
        yield
    except exceptions as e:
        logging.warning(f"suppressed error: {str(e)}")

@contextmanager
def change_dir(path: str):
    """context manager to temporarily change directory."""
    import os
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)

def main():
    """demonstrate context manager usage."""
    # 1. file handling
    print("1. testing file handler:")
    with FileHandler('test.txt', 'w') as f:
        f.write('hello world')
    
    with FileHandler('test.txt', 'r') as f:
        content = f.read()
        print(f"file content: {content}")
    
    # 2. timing code
    print("\n2. testing timer:")
    with Timer():
        time.sleep(0.1)  # simulate work
    
    # 3. indented logging
    print("\n3. testing log indent:")
    LogIndent.log("starting process")
    with LogIndent():
        LogIndent.log("first level")
        with LogIndent():
            LogIndent.log("second level")
        LogIndent.log("back to first level")
    LogIndent.log("back to start")
    
    # 4. temporary file
    print("\n4. testing temporary file:")
    with TempFileHandler('temp.txt') as f:
        f.write('temporary content')
        print("temporary file created")
    print("temporary file removed")
    
    # 5. transaction
    print("\n5. testing transaction:")
    try:
        with transaction() as state:
            state.append('action 1')
            state.append('action 2')
            raise ValueError("simulated error")
    except ValueError:
        print("transaction rolled back")
    
    # 6. error suppression
    print("\n6. testing error suppression:")
    with suppress_errors(ValueError, TypeError):
        raise ValueError("this error will be suppressed")
    
    # 7. directory change
    print("\n7. testing directory change:")
    import os
    original_dir = os.getcwd()
    with change_dir('..'):
        print(f"changed to: {os.getcwd()}")
    print(f"back to: {original_dir}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a context manager that:
#    - manages database connections
#    - handles connection pooling
#    - implements retry logic
#    - manages transactions

# 2. create a context manager that:
#    - implements resource locking
#    - handles deadlock prevention
#    - supports timeout
#    - manages priority

# 3. create a context manager that:
#    - manages environment variables
#    - handles multiple variables
#    - supports nested contexts
#    - manages cleanup