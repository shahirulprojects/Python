# error handling in network operations
import socket
import requests
import urllib3
from typing import Optional, Dict, Any, Union
import json
import ssl
from contextlib import contextmanager
import time
import logging

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NetworkError(Exception):
    """base class for network-related errors."""
    pass

class ConnectionTimeoutError(NetworkError):
    """error for connection timeouts."""
    pass

class SSLCertificateError(NetworkError):
    """error for SSL certificate issues."""
    pass

@contextmanager
def timeout_handler(seconds: int):
    """context manager for handling timeouts."""
    def timeout_signal(signum, frame):
        raise ConnectionTimeoutError("operation timed out")
    
    # set timeout
    original_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(seconds)
    
    try:
        yield
    finally:
        # restore original timeout
        socket.setdefaulttimeout(original_timeout)

def make_http_request(url: str, method: str = 'GET', 
                     params: Optional[Dict[str, Any]] = None,
                     timeout: int = 30) -> Dict[str, Any]:
    """make HTTP request with comprehensive error handling."""
    try:
        with timeout_handler(timeout):
            response = requests.request(
                method=method,
                url=url,
                params=params,
                verify=True,  # verify SSL certificates
                timeout=timeout
            )
            
            # raise for status
            response.raise_for_status()
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'data': response.json() if response.content else None
            }
            
    except requests.exceptions.Timeout:
        logging.error(f"request to {url} timed out after {timeout} seconds")
        raise ConnectionTimeoutError(f"request timed out after {timeout} seconds")
    
    except requests.exceptions.SSLError as e:
        logging.error(f"SSL certificate error for {url}: {str(e)}")
        raise SSLCertificateError(f"SSL verification failed: {str(e)}")
    
    except requests.exceptions.ConnectionError as e:
        logging.error(f"connection error for {url}: {str(e)}")
        raise NetworkError(f"failed to connect: {str(e)}")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"request failed for {url}: {str(e)}")
        raise NetworkError(f"request failed: {str(e)}")

def create_tcp_server(host: str, port: int, 
                     backlog: int = 5) -> socket.socket:
    """create TCP server with error handling."""
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(backlog)
        return server_socket
    
    except socket.error as e:
        if server_socket:
            server_socket.close()
        logging.error(f"failed to create TCP server: {str(e)}")
        raise NetworkError(f"server creation failed: {str(e)}")

def create_ssl_context(cert_file: str, key_file: str) -> ssl.SSLContext:
    """create SSL context with error handling."""
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        return context
    
    except ssl.SSLError as e:
        logging.error(f"SSL context creation failed: {str(e)}")
        raise SSLCertificateError(f"SSL context creation failed: {str(e)}")
    
    except FileNotFoundError as e:
        logging.error(f"certificate file not found: {str(e)}")
        raise SSLCertificateError(f"certificate file not found: {str(e)}")

class HTTPClient:
    """HTTP client with retry and error handling."""
    
    def __init__(self, base_url: str, timeout: int = 30, 
                 max_retries: int = 3, retry_delay: int = 1):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _make_url(self, endpoint: str) -> str:
        """construct full URL from endpoint."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def request(self, method: str, endpoint: str, 
                **kwargs) -> Dict[str, Any]:
        """make HTTP request with retry logic."""
        url = self._make_url(endpoint)
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'data': response.json() if response.content else None
                }
            
            except requests.exceptions.RequestException as e:
                last_error = e
                logging.warning(
                    f"attempt {attempt + 1}/{self.max_retries} failed: {str(e)}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        raise NetworkError(f"request failed after {self.max_retries} attempts") from last_error

def download_file(url: str, output_path: str, 
                 chunk_size: int = 8192) -> None:
    """download file with progress tracking and error handling."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"download progress: {progress:.1f}%", end='\r')
        
        print("\ndownload completed!")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"download failed: {str(e)}")
        raise NetworkError(f"download failed: {str(e)}")
    
    except IOError as e:
        logging.error(f"failed to write file: {str(e)}")
        raise NetworkError(f"failed to write file: {str(e)}")

# example usage
def main():
    """demonstrate network error handling."""
    # 1. basic HTTP request
    print("1. making HTTP request:")
    try:
        result = make_http_request(
            "https://api.github.com/users/octocat",
            timeout=5
        )
        print(f"response: {json.dumps(result, indent=2)}")
    except NetworkError as e:
        print(f"request failed: {e}")
    
    # 2. HTTP client with retries
    print("\n2. using HTTP client with retries:")
    with HTTPClient("https://api.github.com", max_retries=3) as client:
        try:
            result = client.request('GET', '/users/octocat')
            print(f"response: {json.dumps(result, indent=2)}")
        except NetworkError as e:
            print(f"request failed: {e}")
    
    # 3. file download
    print("\n3. downloading file:")
    try:
        download_file(
            "https://www.python.org/static/img/python-logo.png",
            "python-logo.png"
        )
    except NetworkError as e:
        print(f"download failed: {e}")
    
    # 4. TCP server
    print("\n4. creating TCP server:")
    try:
        server = create_tcp_server("localhost", 8000)
        print("server created successfully")
        server.close()
    except NetworkError as e:
        print(f"server creation failed: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a WebSocket client that:
#    - handles connection errors
#    - implements reconnection logic
#    - manages heartbeat messages
#    - provides event callbacks

# 2. create an FTP client that:
#    - handles various FTP error codes
#    - implements retry logic
#    - supports secure connections
#    - manages file transfers

# 3. create a network monitoring tool that:
#    - checks service availability
#    - measures response times
#    - detects network issues
#    - generates alerts 