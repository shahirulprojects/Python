# error handling with third-party libraries
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import redis
from redis.exceptions import RedisError
import pymongo
from pymongo.errors import PyMongoError
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from pandas.errors import *
import requests
from requests.exceptions import RequestException
from typing import Any, Dict, List, Optional, Union
import logging
import json
from contextlib import contextmanager

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# SQLAlchemy error handling
class DatabaseError(Exception):
    """custom database error."""
    pass

@contextmanager
def database_session(engine: sa.Engine):
    """context manager for database sessions."""
    session = sa.orm.Session(engine)
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise DatabaseError(f"integrity error: {str(e)}")
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"database error: {str(e)}")
    finally:
        session.close()

# Redis error handling
class CacheError(Exception):
    """custom cache error."""
    pass

class RedisCache:
    """redis cache with error handling."""
    
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.client = redis.Redis(host=host, port=port)
    
    def get(self, key: str) -> Optional[str]:
        """get value from cache."""
        try:
            value = self.client.get(key)
            return value.decode() if value else None
        except RedisError as e:
            logging.error(f"redis get error: {str(e)}")
            raise CacheError(f"failed to get key '{key}': {str(e)}")
    
    def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """set value in cache."""
        try:
            return self.client.set(key, value, ex=expire)
        except RedisError as e:
            logging.error(f"redis set error: {str(e)}")
            raise CacheError(f"failed to set key '{key}': {str(e)}")

# MongoDB error handling
class MongoDBError(Exception):
    """custom MongoDB error."""
    pass

class MongoDBClient:
    """MongoDB client with error handling."""
    
    def __init__(self, uri: str, database: str):
        try:
            self.client = pymongo.MongoClient(uri)
            self.db = self.client[database]
        except PyMongoError as e:
            raise MongoDBError(f"failed to connect: {str(e)}")
    
    def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        """insert document with error handling."""
        try:
            result = self.db[collection].insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise MongoDBError(f"failed to insert document: {str(e)}")
    
    def find_documents(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """find documents with error handling."""
        try:
            return list(self.db[collection].find(query))
        except PyMongoError as e:
            raise MongoDBError(f"failed to find documents: {str(e)}")

# AWS S3 error handling
class S3Error(Exception):
    """custom S3 error."""
    pass

class S3Client:
    """S3 client with error handling."""
    
    def __init__(self, bucket: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
    
    def upload_file(self, file_path: str, key: str) -> bool:
        """upload file to S3."""
        try:
            self.s3.upload_file(file_path, self.bucket, key)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise S3Error(f"bucket '{self.bucket}' does not exist")
            raise S3Error(f"failed to upload file: {str(e)}")
    
    def download_file(self, key: str, file_path: str) -> bool:
        """download file from S3."""
        try:
            self.s3.download_file(self.bucket, key, file_path)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise S3Error(f"key '{key}' does not exist")
            raise S3Error(f"failed to download file: {str(e)}")

# Pandas error handling
def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """process dataframe with error handling."""
    try:
        # data validation
        if df.empty:
            raise ValueError("empty dataframe")
        
        # check required columns
        required_columns = ['id', 'value']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"missing columns: {missing_columns}")
        
        # data processing
        df['value'] = pd.to_numeric(df['value'], errors='raise')
        df['processed'] = df['value'] * 2
        
        return df
    
    except (ValueError, KeyError) as e:
        raise ValueError(f"data validation error: {str(e)}")
    except EmptyDataError:
        raise ValueError("empty data provided")
    except ParserError:
        raise ValueError("failed to parse data")
    except Exception as e:
        raise ValueError(f"processing error: {str(e)}")

# Requests error handling
class APIClient:
    """API client with error handling."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def request(self, method: str, endpoint: str, 
                **kwargs) -> Dict[str, Any]:
        """make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'data': response.json() if response.content else None
            }
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                raise ValueError(f"resource not found: {endpoint}")
            elif status_code == 401:
                raise ValueError("unauthorized access")
            elif status_code == 403:
                raise ValueError("forbidden access")
            raise ValueError(f"HTTP error: {str(e)}")
            
        except requests.exceptions.ConnectionError:
            raise ValueError(f"failed to connect to {self.base_url}")
            
        except requests.exceptions.Timeout:
            raise ValueError("request timed out")
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"request failed: {str(e)}")

# example usage
def main():
    """demonstrate third-party library error handling."""
    # 1. SQLAlchemy example
    print("1. SQLAlchemy example:")
    try:
        engine = sa.create_engine('sqlite:///example.db')
        with database_session(engine) as session:
            # example query
            result = session.execute(sa.text('SELECT 1')).scalar()
            print(f"query result: {result}")
    except DatabaseError as e:
        print(f"database error: {e}")
    
    # 2. Redis example
    print("\n2. Redis example:")
    try:
        cache = RedisCache()
        cache.set('test_key', 'test_value', expire=60)
        value = cache.get('test_key')
        print(f"cached value: {value}")
    except CacheError as e:
        print(f"cache error: {e}")
    
    # 3. MongoDB example
    print("\n3. MongoDB example:")
    try:
        mongo = MongoDBClient('mongodb://localhost:27017', 'test_db')
        doc_id = mongo.insert_document('test_collection', {'key': 'value'})
        print(f"inserted document ID: {doc_id}")
    except MongoDBError as e:
        print(f"MongoDB error: {e}")
    
    # 4. Pandas example
    print("\n4. Pandas example:")
    try:
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': ['10', '20', '30']
        })
        result_df = process_dataframe(df)
        print("processed dataframe:")
        print(result_df)
    except ValueError as e:
        print(f"pandas error: {e}")
    
    # 5. API client example
    print("\n5. API client example:")
    try:
        client = APIClient('https://api.github.com')
        result = client.request('GET', '/users/octocat')
        print(f"API response: {json.dumps(result, indent=2)}")
    except ValueError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a data pipeline that:
#    - reads from multiple sources (SQL, MongoDB, S3)
#    - processes data with pandas
#    - handles all possible errors
#    - provides detailed error reporting

# 2. create a caching system that:
#    - uses Redis as primary cache
#    - implements fallback mechanisms
#    - handles cache invalidation
#    - monitors cache health

# 3. create an ETL process that:
#    - extracts data from APIs
#    - transforms with pandas
#    - loads to database
#    - implements error recovery 