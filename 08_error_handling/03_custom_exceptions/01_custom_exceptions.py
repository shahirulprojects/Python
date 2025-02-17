# custom exceptions in python
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import logging

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ValidationError(Exception):
    """base class for validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class DataValidationError(ValidationError):
    """error for data validation failures."""
    
    def __init__(self, message: str, field: str, value: Any):
        super().__init__(message, field)
        self.value = value
    
    def __str__(self):
        return f"validation error in field '{self.field}': {self.message} (value: {self.value})"

class DatabaseError(Exception):
    """base class for database errors."""
    
    def __init__(self, message: str, query: Optional[str] = None):
        self.message = message
        self.query = query
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """convert error to dictionary."""
        return {
            'message': self.message,
            'query': self.query,
            'timestamp': self.timestamp.isoformat(),
            'type': self.__class__.__name__
        }

class DatabaseConnectionError(DatabaseError):
    """error for database connection failures."""
    
    def __init__(self, message: str, host: str, port: int):
        super().__init__(message)
        self.host = host
        self.port = port
    
    def __str__(self):
        return f"failed to connect to database at {self.host}:{self.port} - {self.message}"

class DatabaseQueryError(DatabaseError):
    """error for database query failures."""
    
    def __init__(self, message: str, query: str, params: Optional[Dict[str, Any]] = None):
        super().__init__(message, query)
        self.params = params or {}
    
    def __str__(self):
        return f"query failed: {self.message}\nQuery: {self.query}\nParams: {self.params}"

class ConfigurationError(Exception):
    """error for configuration issues."""
    
    def __init__(self, message: str, config_file: str, missing_keys: Optional[List[str]] = None):
        self.message = message
        self.config_file = config_file
        self.missing_keys = missing_keys or []
        super().__init__(self.message)
    
    def __str__(self):
        base_msg = f"configuration error in '{self.config_file}': {self.message}"
        if self.missing_keys:
            base_msg += f"\nMissing keys: {', '.join(self.missing_keys)}"
        return base_msg

class APIError(Exception):
    """base class for API errors."""
    
    def __init__(self, message: str, status_code: int, response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def to_json(self) -> str:
        """convert error to JSON string."""
        return json.dumps({
            'error': self.message,
            'status_code': self.status_code,
            'timestamp': self.timestamp.isoformat(),
            'response': self.response
        })

class APIRequestError(APIError):
    """error for API request failures."""
    
    def __init__(self, message: str, status_code: int, endpoint: str):
        super().__init__(message, status_code)
        self.endpoint = endpoint
    
    def __str__(self):
        return f"API request failed: {self.message} (endpoint: {self.endpoint}, status: {self.status_code})"

class APIResponseError(APIError):
    """error for API response validation failures."""
    
    def __init__(self, message: str, status_code: int, response: Dict[str, Any], expected_schema: Dict[str, Any]):
        super().__init__(message, status_code, response)
        self.expected_schema = expected_schema
    
    def __str__(self):
        return f"API response validation failed: {self.message} (status: {self.status_code})"

def validate_user_data(data: Dict[str, Any]):
    """validate user data with custom exceptions."""
    required_fields = ['username', 'email', 'age']
    
    # check required fields
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"missing required field: {field}", field)
    
    # validate username
    if not isinstance(data['username'], str) or len(data['username']) < 3:
        raise DataValidationError(
            "username must be a string with at least 3 characters",
            'username',
            data['username']
        )
    
    # validate email
    if '@' not in data.get('email', ''):
        raise DataValidationError(
            "invalid email format",
            'email',
            data['email']
        )
    
    # validate age
    try:
        age = int(data['age'])
        if age < 0 or age > 150:
            raise DataValidationError(
                "age must be between 0 and 150",
                'age',
                age
            )
    except (ValueError, TypeError):
        raise DataValidationError(
            "age must be a valid number",
            'age',
            data['age']
        )

def simulate_database_operation(query: str, params: Dict[str, Any]):
    """simulate database operations with custom exceptions."""
    # simulate connection error
    if 'localhost' in query:
        raise DatabaseConnectionError(
            "connection refused",
            'localhost',
            5432
        )
    
    # simulate query error
    if 'SELECT' in query and not params:
        raise DatabaseQueryError(
            "missing required parameters",
            query,
            params
        )

def load_configuration(config_file: str):
    """load configuration with custom exceptions."""
    required_keys = ['api_key', 'host', 'port']
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ConfigurationError(
            "invalid JSON format",
            config_file
        )
    
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ConfigurationError(
            "missing required configuration keys",
            config_file,
            missing_keys
        )

def make_api_request(endpoint: str, data: Dict[str, Any]):
    """simulate API requests with custom exceptions."""
    # simulate request error
    if not endpoint.startswith('/'):
        raise APIRequestError(
            "invalid endpoint format",
            400,
            endpoint
        )
    
    # simulate response validation error
    if 'auth' in endpoint:
        expected_schema = {'token': str, 'expires_in': int}
        response = {'token': 123, 'expires_in': 'invalid'}
        raise APIResponseError(
            "response does not match expected schema",
            200,
            response,
            expected_schema
        )

# example usage
def main():
    """demonstrate custom exceptions."""
    # 1. data validation
    print("1. testing data validation:")
    try:
        user_data = {
            'username': 'jo',
            'email': 'invalid-email',
            'age': '200'
        }
        validate_user_data(user_data)
    except ValidationError as e:
        print(f"validation failed: {e}")
    
    # 2. database operations
    print("\n2. testing database operations:")
    try:
        simulate_database_operation(
            "SELECT * FROM users WHERE id = :id",
            {}
        )
    except DatabaseError as e:
        print(f"database error: {e}")
        print(f"error details: {e.to_dict()}")
    
    # 3. configuration loading
    print("\n3. testing configuration loading:")
    try:
        load_configuration("config.json")
    except ConfigurationError as e:
        print(f"configuration error: {e}")
    
    # 4. API requests
    print("\n4. testing API requests:")
    try:
        make_api_request("auth/login", {"username": "test"})
    except APIError as e:
        print(f"API error: {e}")
        print(f"error JSON: {e.to_json()}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a validation system that:
#    - defines custom exceptions for different validation rules
#    - supports nested object validation
#    - provides detailed error messages
#    - allows custom validation rules

# 2. create a database wrapper that:
#    - implements custom exceptions for different database operations
#    - handles connection pooling errors
#    - provides transaction management
#    - supports different database types

# 3. create an API client that:
#    - implements custom exceptions for different HTTP status codes
#    - handles authentication errors
#    - validates request/response data
#    - supports retry logic 