# error handling in web frameworks (Flask and Django)
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, ValidationError
import jwt
from typing import Dict, Any, Optional, Callable, TypeVar
import logging
from functools import wraps
import traceback
from datetime import datetime
from dataclasses import dataclass

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# custom exceptions
class APIError(Exception):
    """base class for API errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(APIError):
    """authentication related errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=401)

class AuthorizationError(APIError):
    """authorization related errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=403)

class ValidationError(APIError):
    """validation related errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

class ResourceNotFoundError(APIError):
    """resource not found errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

# validation schemas
class UserSchema(Schema):
    """user data validation schema."""
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=lambda n: 0 < n < 150)

# error handlers
def handle_api_error(error: APIError) -> tuple[Dict[str, Any], int]:
    """handle custom API errors."""
    return {
        'error': error.message,
        'status_code': error.status_code,
        'timestamp': datetime.utcnow().isoformat()
    }, error.status_code

def handle_validation_error(error: ValidationError) -> tuple[Dict[str, Any], int]:
    """handle marshmallow validation errors."""
    return {
        'error': 'validation error',
        'details': error.messages,
        'status_code': 422,
        'timestamp': datetime.utcnow().isoformat()
    }, 422

def handle_http_error(error: HTTPException) -> tuple[Dict[str, Any], int]:
    """handle werkzeug HTTP errors."""
    return {
        'error': error.description,
        'status_code': error.code,
        'timestamp': datetime.utcnow().isoformat()
    }, error.code

def handle_generic_error(error: Exception) -> tuple[Dict[str, Any], int]:
    """handle all other errors."""
    logging.error(f"unexpected error: {str(error)}")
    logging.error(traceback.format_exc())
    return {
        'error': 'internal server error',
        'status_code': 500,
        'timestamp': datetime.utcnow().isoformat()
    }, 500

# decorators
def require_auth(f: Callable) -> Callable:
    """decorator for requiring authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError('missing authorization header')
        
        try:
            # validate JWT token
            token = auth_header.split('Bearer ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            request.user = payload
        except (IndexError, jwt.InvalidTokenError) as e:
            raise AuthenticationError(f'invalid token: {str(e)}')
        
        return f(*args, **kwargs)
    return decorated

def validate_request(schema: Schema) -> Callable:
    """decorator for request validation."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                data = request.get_json()
                validated_data = schema().load(data)
                return f(validated_data, *args, **kwargs)
            except ValidationError as e:
                raise ValidationError(str(e.messages))
        return decorated
    return decorator

def log_errors(f: Callable) -> Callable:
    """decorator for error logging."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"error in {f.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            raise
    return decorated

# Flask application
app = Flask(__name__)

# register error handlers
app.register_error_handler(APIError, handle_api_error)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(HTTPException, handle_http_error)
app.register_error_handler(Exception, handle_generic_error)

# routes
@app.route('/api/users', methods=['POST'])
@log_errors
@require_auth
@validate_request(UserSchema)
def create_user(data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
    """create new user."""
    try:
        # simulate user creation
        user_id = 123
        return {
            'message': 'user created successfully',
            'user_id': user_id
        }, 201
    except Exception as e:
        raise APIError(f"failed to create user: {str(e)}")

@app.route('/api/users/<int:user_id>', methods=['GET'])
@log_errors
@require_auth
def get_user(user_id: int) -> Dict[str, Any]:
    """get user by ID."""
    try:
        # simulate database query
        if user_id != 123:
            raise ResourceNotFoundError(f"user {user_id} not found")
        
        return {
            'id': user_id,
            'username': 'test_user',
            'email': 'test@example.com'
        }
    except ResourceNotFoundError:
        raise
    except Exception as e:
        raise APIError(f"failed to get user: {str(e)}")

@app.route('/api/protected', methods=['GET'])
@log_errors
@require_auth
def protected_route() -> Dict[str, Any]:
    """protected route example."""
    user = request.user
    if user.get('role') != 'admin':
        raise AuthorizationError('admin access required')
    
    return {'message': 'access granted'}

# Django-style error handling
@dataclass
class DjangoRequest:
    """simplified Django request."""
    method: str
    path: str
    user: Optional[Dict[str, Any]] = None

class DjangoMiddleware:
    """example Django middleware for error handling."""
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: DjangoRequest) -> Dict[str, Any]:
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.handle_error(e)
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """handle different types of errors."""
        if isinstance(error, APIError):
            return handle_api_error(error)[0]
        elif isinstance(error, ValidationError):
            return handle_validation_error(error)[0]
        elif isinstance(error, HTTPException):
            return handle_http_error(error)[0]
        else:
            return handle_generic_error(error)[0]

# example usage
def main():
    """demonstrate web framework error handling."""
    # simulate requests
    print("1. testing user creation:")
    try:
        # missing authorization
        create_user({
            'username': 'test_user',
            'email': 'test@example.com',
            'age': 25
        })
    except AuthenticationError as e:
        print(f"auth error: {e}")
    
    print("\n2. testing user retrieval:")
    try:
        # user not found
        get_user(456)
    except ResourceNotFoundError as e:
        print(f"not found error: {e}")
    
    print("\n3. testing protected route:")
    try:
        # insufficient permissions
        request.user = {'role': 'user'}
        protected_route()
    except AuthorizationError as e:
        print(f"authorization error: {e}")
    
    print("\n4. testing Django middleware:")
    middleware = DjangoMiddleware(lambda r: {'success': True})
    
    # simulate successful request
    request = DjangoRequest('GET', '/api/test')
    response = middleware(request)
    print(f"success response: {response}")
    
    # simulate error
    def error_view(request):
        raise ValidationError('invalid data')
    
    middleware = DjangoMiddleware(error_view)
    response = middleware(request)
    print(f"error response: {response}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a REST API that:
#    - implements CRUD operations
#    - handles all HTTP methods
#    - validates request data
#    - provides detailed error responses

# 2. create a middleware system that:
#    - handles authentication
#    - rate limiting
#    - request logging
#    - error tracking

# 3. create an API gateway that:
#    - routes requests to services
#    - handles service failures
#    - implements circuit breaker
#    - provides metrics 