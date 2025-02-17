# handling file processing errors
# this module demonstrates error handling for various file operations

import os
import json
import csv
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import shutil
import logging
from dataclasses import dataclass
from contextlib import contextmanager
import tempfile

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class FileProcessingError(Exception):
    """custom exception for file processing errors
    
    why we need this:
    file operations can fail in many ways:
    - file not found
    - permission issues
    - disk space issues
    - corrupted files
    - etc.
    
    having specific error types helps us handle each case appropriately
    """
    message: str
    error_code: str
    file_path: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class SafeFileProcessor:
    """handles file operations with comprehensive error handling
    
    why we need this:
    file operations need careful handling to:
    - prevent data loss
    - handle system errors
    - ensure atomic operations
    - clean up temporary files
    """
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """ensures the base directory exists
        
        handles permission and existence errors gracefully
        """
        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise FileProcessingError(
                message=f"no permission to create directory: {self.base_dir}",
                error_code="PERMISSION_DENIED"
            )
        except OSError as e:
            raise FileProcessingError(
                message=f"failed to create directory: {str(e)}",
                error_code="DIRECTORY_CREATE_ERROR"
            )
    
    @contextmanager
    def safe_open(self, filename: str, mode: str = 'r'):
        """safely opens files using a context manager
        
        why we need this:
        ensures files are properly closed even if errors occur
        provides consistent error handling for file operations
        """
        file_path = self.base_dir / filename
        try:
            with open(file_path, mode) as f:
                yield f
        except FileNotFoundError:
            raise FileProcessingError(
                message=f"file not found: {filename}",
                error_code="FILE_NOT_FOUND",
                file_path=str(file_path)
            )
        except PermissionError:
            raise FileProcessingError(
                message=f"permission denied: {filename}",
                error_code="PERMISSION_DENIED",
                file_path=str(file_path)
            )
        except IOError as e:
            raise FileProcessingError(
                message=f"IO error: {str(e)}",
                error_code="IO_ERROR",
                file_path=str(file_path)
            )
    
    def safe_write(self, filename: str, content: str) -> None:
        """safely writes content to a file
        
        why we need this:
        - prevents partial writes that could corrupt files
        - ensures atomic operations
        - handles various write errors
        """
        temp_file = None
        try:
            # create a temporary file
            fd, temp_path = tempfile.mkstemp(dir=str(self.base_dir))
            temp_file = os.fdopen(fd, 'w')
            
            # write to temporary file
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_file.close()
            
            # atomically move temporary file to target
            target_path = self.base_dir / filename
            shutil.move(temp_path, target_path)
            
        except IOError as e:
            raise FileProcessingError(
                message=f"failed to write file: {str(e)}",
                error_code="WRITE_ERROR",
                file_path=filename
            )
        finally:
            # clean up temporary file if it exists
            if temp_file:
                temp_file.close()
    
    def read_json(self, filename: str) -> Dict[str, Any]:
        """safely reads and parses JSON files
        
        handles:
        - file not found
        - invalid JSON
        - permission issues
        """
        try:
            with self.safe_open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise FileProcessingError(
                message=f"invalid JSON in file: {str(e)}",
                error_code="INVALID_JSON",
                file_path=filename,
                details={'position': e.pos, 'line': e.lineno, 'column': e.colno}
            )
    
    def write_json(self, filename: str, data: Dict[str, Any]) -> None:
        """safely writes JSON data to a file"""
        try:
            json_str = json.dumps(data, indent=2)
            self.safe_write(filename, json_str)
        except TypeError as e:
            raise FileProcessingError(
                message=f"cannot serialize to JSON: {str(e)}",
                error_code="JSON_SERIALIZE_ERROR",
                file_path=filename
            )
    
    def read_csv(self, filename: str) -> List[Dict[str, str]]:
        """safely reads CSV files
        
        handles:
        - malformed CSV
        - encoding issues
        - missing files
        """
        try:
            with self.safe_open(filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except csv.Error as e:
            raise FileProcessingError(
                message=f"invalid CSV format: {str(e)}",
                error_code="INVALID_CSV",
                file_path=filename
            )
    
    def backup_file(self, filename: str) -> str:
        """creates a backup of a file
        
        ensures we don't lose data when modifying files
        """
        source_path = self.base_dir / filename
        backup_path = source_path.with_suffix(source_path.suffix + '.bak')
        
        try:
            shutil.copy2(source_path, backup_path)
            return str(backup_path)
        except IOError as e:
            raise FileProcessingError(
                message=f"failed to create backup: {str(e)}",
                error_code="BACKUP_ERROR",
                file_path=str(source_path)
            )

def main():
    """demonstrates file processing error handling"""
    processor = SafeFileProcessor("test_files")
    
    # scenario 1: writing and reading JSON
    print("1. JSON processing:")
    try:
        # write JSON
        data = {
            'name': 'John Doe',
            'age': 30,
            'email': 'john@example.com'
        }
        processor.write_json('user.json', data)
        print("JSON file written successfully")
        
        # read JSON
        loaded_data = processor.read_json('user.json')
        print(f"read JSON data: {loaded_data}")
        
    except FileProcessingError as e:
        print(f"JSON processing error: {e.message}")
    
    # scenario 2: handling invalid JSON
    print("\n2. handling invalid JSON:")
    try:
        processor.read_json('nonexistent.json')
    except FileProcessingError as e:
        print(f"expected error: {e.message}")
    
    # scenario 3: creating backups
    print("\n3. file backup:")
    try:
        # create a test file
        processor.safe_write('important.txt', 'important data')
        
        # create backup
        backup_path = processor.backup_file('important.txt')
        print(f"backup created at: {backup_path}")
        
    except FileProcessingError as e:
        print(f"backup error: {e.message}")
    
    # scenario 4: handling permission errors
    print("\n4. permission handling:")
    try:
        # attempt to write to a directory without permissions
        bad_processor = SafeFileProcessor("/root/test")
    except FileProcessingError as e:
        print(f"expected error: {e.message}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. implement file compression:
#    - add methods to compress/decompress files
#    - handle corruption errors
#    - implement progress tracking
#    - ensure atomic operations

# 2. add file validation:
#    - implement checksum verification
#    - validate file formats
#    - handle encoding issues
#    - implement file type detection

# 3. create a file processing pipeline:
#    - handle multiple file formats
#    - implement error recovery
#    - add logging and monitoring
#    - ensure proper cleanup 