# advanced error handling patterns and best practices
# this module demonstrates sophisticated error handling techniques

from typing import Any, Optional, Dict, List
import logging
import traceback
from dataclasses import dataclass
from enum import Enum, auto

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ErrorSeverity(Enum):
    """defines different levels of error severity
    
    why we need this:
    not all errors are equal - some need immediate attention,
    others are just warnings we can handle gracefully
    """
    LOW = auto()      # minor issues, can continue
    MEDIUM = auto()   # significant issues, might need attention
    HIGH = auto()     # critical issues, needs immediate attention
    FATAL = auto()    # unrecoverable issues, must stop

@dataclass
class ErrorContext:
    """contains detailed context about an error
    
    why we need this:
    when errors occur, we often need more than just the error message
    having context helps with debugging and error reporting
    """
    message: str
    severity: ErrorSeverity
    timestamp: float
    stack_trace: str
    additional_info: Dict[str, Any]

class BusinessLogicError(Exception):
    """base exception for all business logic related errors
    
    why we need this:
    separating business logic errors from technical errors helps with:
    - better error handling based on error type
    - clearer error messages for users
    - easier debugging and logging
    """
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM):
        self.context = ErrorContext(
            message=message,
            severity=severity,
            timestamp=time.time(),
            stack_trace=traceback.format_exc(),
            additional_info={}
        )
        super().__init__(message)

class ValidationError(BusinessLogicError):
    """raised when data validation fails"""
    def __init__(self, message: str, invalid_fields: List[str]):
        super().__init__(message, ErrorSeverity.LOW)
        self.context.additional_info['invalid_fields'] = invalid_fields

class ResourceError(BusinessLogicError):
    """raised when resource access or manipulation fails"""
    def __init__(self, message: str, resource_id: str):
        super().__init__(message, ErrorSeverity.HIGH)
        self.context.additional_info['resource_id'] = resource_id

def handle_error(error: Exception) -> None:
    """centralized error handling with different strategies based on error type
    
    why we need this:
    centralizing error handling helps maintain consistent error handling across
    the application and makes it easier to modify error handling behavior
    """
    if isinstance(error, BusinessLogicError):
        # handle business logic errors
        context = error.context
        logging.error(
            f"Business error: {context.message} "
            f"(Severity: {context.severity.name})"
        )
        
        if context.severity in (ErrorSeverity.HIGH, ErrorSeverity.FATAL):
            # send alert to admin
            alert_admin(context)
    else:
        # handle unexpected technical errors
        logging.error(f"Unexpected error: {str(error)}")
        logging.debug(f"Stack trace: {traceback.format_exc()}")

def alert_admin(error_context: ErrorContext) -> None:
    """simulates sending an alert to system administrators
    
    in a real application, this might:
    - send an email
    - create a ticket
    - trigger a notification
    """
    print(f"ALERT: Critical error occurred!")
    print(f"Message: {error_context.message}")
    print(f"Severity: {error_context.severity.name}")
    print(f"Additional info: {error_context.additional_info}")

def process_user_data(data: Dict[str, Any]) -> None:
    """demonstrates advanced error handling in action
    
    why this matters:
    real applications need to handle errors at different levels
    and provide appropriate responses based on the error type
    """
    try:
        # validate user data
        invalid_fields = []
        if 'email' not in data:
            invalid_fields.append('email')
        if 'age' in data and not isinstance(data['age'], int):
            invalid_fields.append('age')
        
        if invalid_fields:
            raise ValidationError(
                "invalid user data provided",
                invalid_fields
            )
        
        # simulate resource access
        if 'user_id' in data:
            try:
                # simulate database operation
                if data['user_id'] == 'invalid':
                    raise ResourceError(
                        "failed to access user record",
                        data['user_id']
                    )
            except ResourceError as e:
                # add more context and re-raise
                e.context.additional_info['operation'] = 'user_lookup'
                raise
        
        # process the data (simulated)
        print("processing user data...")
        
    except Exception as e:
        # use our centralized error handler
        handle_error(e)
        # decide whether to re-raise based on severity
        if isinstance(e, BusinessLogicError) and \
           e.context.severity == ErrorSeverity.FATAL:
            raise

def main():
    """demonstrates the advanced error handling patterns"""
    # example 1: handling validation error
    print("1. Testing validation error:")
    process_user_data({'name': 'John'})  # missing email
    
    # example 2: handling resource error
    print("\n2. Testing resource error:")
    process_user_data({
        'email': 'john@example.com',
        'user_id': 'invalid'
    })
    
    # example 3: successful processing
    print("\n3. Testing successful case:")
    process_user_data({
        'email': 'john@example.com',
        'age': 30,
        'user_id': 'valid123'
    })

if __name__ == "__main__":
    main()

# practice exercises:
# 1. extend the error handling system:
#    - add more error types for specific scenarios
#    - implement different handling strategies
#    - add error recovery mechanisms

# 2. implement a retry mechanism:
#    - create a decorator for retrying failed operations
#    - add exponential backoff
#    - handle different types of errors differently

# 3. create an error reporting system:
#    - aggregate similar errors
#    - generate error reports
#    - implement error tracking and analytics 