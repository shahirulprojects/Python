# exception handling in python
# this file explains how to handle errors and unexpected situations gracefully

# 1. basic try-except structure
# when we think something might go wrong, we use try-except
def divide_numbers(a, b):
    # tries to perform division, handles potential errors
    try:
        # attempt the division
        result = a / b
        return result
    except ZeroDivisionError:
        # handles the specific case of division by zero
        return "sorry, can't divide by zero"
    except TypeError:
        # handles cases where inputs aren't numbers
        return "please provide valid numbers"

# examples of different scenarios
print(divide_numbers(10, 2))     # works fine: 5.0
print(divide_numbers(10, 0))     # handles zero division
print(divide_numbers(10, "2"))   # handles invalid type

# 2. handling multiple exceptions
def process_user_data(data):
    """
    processes user input data safely
    
    args:
        data: user input to process
    
    returns:
        processed result or error message
    """
    try:
        # convert to integer and process
        number = int(data)
        result = number * 2
        
        # check if result is too large
        if result > 1000:
            raise ValueError("result is too large")
        
        return result
    
    except ValueError as e:
        # handles both int conversion and our custom error
        return f"value error: {str(e)}"
    except TypeError:
        # handles wrong input type
        return "please provide a valid input"
    except Exception as e:
        # catches any other unexpected errors
        return f"an unexpected error occurred: {str(e)}"

# 3. using else and finally
def read_user_preferences(filename):
    """
    reads user preferences from a file with complete error handling
    
    args:
        filename: name of the preferences file
    """
    try:
        # attempt to open and read the file
        with open(filename, 'r') as file:
            data = file.read()
            # process the data here
    
    except FileNotFoundError:
        # handles missing file
        print("preferences file not found, using defaults")
    
    else:
        # runs only if try block succeeds
        print("successfully loaded preferences")
    
    finally:
        # always runs, regardless of success or failure
        print("finished checking preferences")

# 4. creating custom exceptions
class AgeError(Exception):
    # custom exception for age-related errors
    pass

def verify_age(age):
    """
    verifies if an age is valid
    
    args:
        age: age to verify
    
    raises:
        AgeError: if age is invalid
    """
    try:
        # convert to integer and validate
        age_num = int(age)
        
        if age_num < 0:
            raise AgeError("age cannot be negative")
        if age_num > 150:
            raise AgeError("age seems unrealistic")
        
        return f"age {age_num} is valid"
    
    except ValueError:
        return "please provide a valid number"
    except AgeError as e:
        return f"invalid age: {str(e)}"

# 5. practical examples

def safe_list_access(lst, index):
    """
    safely accesses a list element with error handling
    
    args:
        lst: list to access
        index: index to retrieve
    
    returns:
        element or error message
    """
    try:
        return lst[index]
    except IndexError:
        return f"index {index} is out of range"
    except TypeError:
        return "please provide a valid list and index"

# example usage
numbers = [1, 2, 3]
print(safe_list_access(numbers, 1))    # works: 2
print(safe_list_access(numbers, 10))   # handles out of range
print(safe_list_access(None, 1))       # handles invalid list

def process_configuration(config_file):
    """
    processes a configuration file with comprehensive error handling
    
    args:
        config_file: path to configuration file
    """
    try:
        # attempt to read and process configuration
        with open(config_file, 'r') as file:
            # read configuration
            config_data = file.read()
            
            # simulate some processing
            if not config_data:
                raise ValueError("empty configuration")
            
            # process successful
            print("configuration loaded successfully")
            
    except FileNotFoundError:
        # handles missing configuration file
        print("configuration file not found")
        print("creating default configuration...")
        # could create default config here
        
    except ValueError as e:
        # handles invalid configuration
        print(f"invalid configuration: {str(e)}")
        print("using fallback settings...")
        
    except Exception as e:
        # handles any other unexpected errors
        print(f"unexpected error: {str(e)}")
        print("using safe mode settings...")
        
    finally:
        # always ensure we have a working configuration
        print("configuration check complete")

# 6. context managers with error handling
class DatabaseConnection:
    """example of a context manager with error handling"""
    
    def __enter__(self):
        # simulate database connection
        print("connecting to database...")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        # ensure proper cleanup
        print("closing database connection...")
        
        # handle any errors that occurred
        if exc_type is not None:
            print(f"an error occurred: {exc_value}")
            # return True to suppress the error
            return True

def safe_database_operation():
    """demonstrates safe resource handling"""
    try:
        with DatabaseConnection() as db:
            # simulate some database operations
            print("performing database operations...")
            # simulate an error
            raise Exception("database error")
            
    except Exception as e:
        print(f"operation failed: {str(e)}")
    
    finally:
        print("database operation completed") 