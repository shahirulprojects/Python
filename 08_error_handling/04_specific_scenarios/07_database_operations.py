# handling database operations errors
# this module demonstrates error handling for common database scenarios

import sqlite3
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
import logging
from datetime import datetime
from dataclasses import dataclass

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class DatabaseError(Exception):
    """custom exception for database-related errors
    
    why we need this:
    database operations can fail in many ways, and we want to:
    - provide clear error messages
    - distinguish between different types of failures
    - handle each case appropriately
    """
    message: str
    error_code: Optional[str] = None
    query: Optional[str] = None
    params: Optional[tuple] = None

@contextmanager
def database_connection(db_path: str):
    """creates a database connection using context manager
    
    why we need this:
    database connections are resources that need proper cleanup
    using a context manager ensures we:
    - always close the connection
    - handle connection errors gracefully
    - use consistent connection handling across the application
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        # enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    except sqlite3.Error as e:
        # handle connection errors
        raise DatabaseError(
            message=f"failed to connect to database: {str(e)}",
            error_code="CONNECTION_ERROR"
        )
    finally:
        # ensure connection is closed even if an error occurs
        if conn:
            conn.close()

class UserDatabase:
    """handles user-related database operations with error handling"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """creates necessary tables if they don't exist
        
        handles errors that might occur during initialization
        """
        try:
            with database_connection(self.db_path) as conn:
                cursor = conn.cursor()
                
                # create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # create user_logs table for tracking operations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                conn.commit()
        except DatabaseError as e:
            logging.error(f"database initialization failed: {e.message}")
            raise
        except Exception as e:
            logging.error(f"unexpected error during initialization: {str(e)}")
            raise DatabaseError(
                message="failed to initialize database",
                error_code="INIT_ERROR"
            )
    
    def create_user(self, username: str, email: str) -> int:
        """creates a new user with error handling for duplicates
        
        why this needs careful error handling:
        - username/email might already exist
        - database might be locked
        - connection might fail
        """
        try:
            with database_connection(self.db_path) as conn:
                cursor = conn.cursor()
                
                # attempt to insert new user
                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (?, ?)",
                    (username, email)
                )
                
                # get the id of the new user
                user_id = cursor.lastrowid
                
                # log the creation
                cursor.execute(
                    "INSERT INTO user_logs (user_id, action) VALUES (?, ?)",
                    (user_id, "USER_CREATED")
                )
                
                conn.commit()
                return user_id
                
        except sqlite3.IntegrityError as e:
            # handle duplicate username/email
            if "UNIQUE constraint failed: users.username" in str(e):
                raise DatabaseError(
                    message=f"username '{username}' already exists",
                    error_code="DUPLICATE_USERNAME"
                )
            elif "UNIQUE constraint failed: users.email" in str(e):
                raise DatabaseError(
                    message=f"email '{email}' already exists",
                    error_code="DUPLICATE_EMAIL"
                )
            raise DatabaseError(
                message=f"integrity error: {str(e)}",
                error_code="INTEGRITY_ERROR"
            )
        except sqlite3.OperationalError as e:
            # handle database locked or similar operational errors
            raise DatabaseError(
                message=f"database operation failed: {str(e)}",
                error_code="OPERATIONAL_ERROR"
            )
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """retrieves user data with error handling for missing users"""
        try:
            with database_connection(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT id, username, email, created_at FROM users WHERE id = ?",
                    (user_id,)
                )
                
                result = cursor.fetchone()
                if result is None:
                    return None
                
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'created_at': result[3]
                }
                
        except sqlite3.Error as e:
            raise DatabaseError(
                message=f"failed to retrieve user: {str(e)}",
                error_code="RETRIEVAL_ERROR",
                query="SELECT FROM users",
                params=(user_id,)
            )

def main():
    """demonstrates database error handling scenarios"""
    # create a test database
    db = UserDatabase("test.db")
    
    # scenario 1: create a user successfully
    try:
        print("1. creating a new user:")
        user_id = db.create_user("john_doe", "john@example.com")
        print(f"user created with id: {user_id}")
    except DatabaseError as e:
        print(f"failed to create user: {e.message}")
    
    # scenario 2: attempt to create duplicate user
    try:
        print("\n2. attempting to create duplicate user:")
        db.create_user("john_doe", "another@example.com")
    except DatabaseError as e:
        print(f"expected error: {e.message}")
    
    # scenario 3: retrieve existing user
    try:
        print("\n3. retrieving existing user:")
        user = db.get_user(1)
        if user:
            print(f"found user: {user}")
        else:
            print("user not found")
    except DatabaseError as e:
        print(f"failed to retrieve user: {e.message}")
    
    # scenario 4: retrieve non-existent user
    try:
        print("\n4. retrieving non-existent user:")
        user = db.get_user(999)
        if user:
            print(f"found user: {user}")
        else:
            print("user not found (as expected)")
    except DatabaseError as e:
        print(f"failed to retrieve user: {e.message}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement update and delete operations:
#    - handle cases where the user doesn't exist
#    - implement proper transaction management
#    - log all operations in user_logs

# 2. add connection pooling:
#    - implement a connection pool manager
#    - handle pool exhaustion errors
#    - implement proper cleanup

# 3. implement a retry mechanism:
#    - retry failed operations with exponential backoff
#    - handle different types of database errors differently
#    - log retry attempts 