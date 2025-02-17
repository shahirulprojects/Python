# understanding context managers and the with statement
# this module explores how to properly manage resources and handle cleanup

from typing import Any, Optional, TextIO
from contextlib import contextmanager
import time

class DatabaseConnection:
    """simulates a database connection to demonstrate resource management
    
    why we need this:
    many resources (files, network connections, database connections) need proper cleanup
    context managers help us ensure resources are always properly released
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.is_connected = False
    
    def __enter__(self) -> 'DatabaseConnection':
        """called when entering a with block
        
        this is where we set up our resource (like opening a connection)
        """
        print(f"connecting to database '{self.db_name}'...")
        self.is_connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """called when exiting a with block (even if an error occurred)
        
        this is where we clean up our resource (like closing a connection)
        
        parameters:
            exc_type: the type of exception that occurred (if any)
            exc_val: the exception instance (if any)
            exc_tb: the traceback (if any)
        
        returns:
            True if we handled the exception, False to propagate it
        """
        print(f"closing connection to '{self.db_name}'...")
        self.is_connected = False
        # we're not handling any exceptions, so return False
        return False
    
    def query(self, sql: str) -> list:
        """simulates executing a database query"""
        if not self.is_connected:
            raise RuntimeError("cannot execute query - not connected to database")
        print(f"executing query: {sql}")
        return []

@contextmanager
def timer():
    """a simple context manager to measure execution time
    
    why we need this:
    sometimes we want to create simple context managers without a full class
    the @contextmanager decorator makes this easy :D
    
    usage:
        with timer():
            do_something()
    """
    start = time.time()
    try:
        # this is like __enter__
        yield
    finally:
        # this is like __exit__
        end = time.time()
        print(f"execution took {end - start:.2f} seconds")

def demonstrate_file_context_manager(filename: str) -> Optional[str]:
    """demonstrates using a context manager with files
    
    why this is better:
    - no need to explicitly close the file
    - file is closed even if an error occurs
    - code is cleaner and more pythonic
    """
    try:
        with open(filename, 'r') as file:
            # file is automatically closed when we exit this block
            return file.read()
    except IOError as e:
        print(f"error reading file: {e}")
        return None

def main():
    """demonstrates various context manager use cases"""
    # example 1: database connection (custom context manager)
    print("1. database connection example:")
    try:
        with DatabaseConnection("users_db") as db:
            db.query("SELECT * FROM users")
            # even if we raise an error, the connection will be closed
            raise ValueError("something went wrong!")
    except ValueError as e:
        print(f"caught error: {e}")
    
    # example 2: timing code execution
    print("\n2. timing example:")
    with timer():
        # simulate some work
        time.sleep(1)
    
    # example 3: file handling
    print("\n3. file handling example:")
    content = demonstrate_file_context_manager("sample.txt")
    
    # example 4: nested context managers
    print("\n4. nested context managers:")
    try:
        with DatabaseConnection("users_db") as db1, \
             DatabaseConnection("logs_db") as db2:
            db1.query("SELECT * FROM users")
            db2.query("INSERT INTO logs VALUES ('user_query')")
    except Exception as e:
        print(f"error in nested contexts: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a custom context manager:
#    - implement a connection pool manager
#    - handle resource cleanup properly
#    - add proper error handling

# 2. use the @contextmanager decorator:
#    - create a context manager for temporary directory
#    - ensure cleanup happens even if errors occur
#    - measure the execution time

# 3. combine multiple context managers:
#    - work with files and database connections
#    - handle errors appropriately
#    - ensure all resources are cleaned up 