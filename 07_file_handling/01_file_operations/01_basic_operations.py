# basic file operations in python
import os
from pathlib import Path
from typing import List, Optional

def create_file(filename: str, content: str = "") -> bool:
    """create a new file with optional content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"error creating file: {e}")
        return False

def read_file(filename: str) -> Optional[str]:
    """read entire contents of a file."""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except IOError as e:
        print(f"error reading file: {e}")
        return None

def append_to_file(filename: str, content: str) -> bool:
    """append content to an existing file."""
    try:
        with open(filename, 'a') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"error appending to file: {e}")
        return False

def delete_file(filename: str) -> bool:
    """delete a file if it exists."""
    try:
        os.remove(filename)
        return True
    except FileNotFoundError:
        print(f"file not found: {filename}")
        return False
    except IOError as e:
        print(f"error deleting file: {e}")
        return False

def list_files(directory: str = ".") -> List[str]:
    """list all files in a directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except IOError as e:
        print(f"error listing files: {e}")
        return []

def create_directory(directory: str) -> bool:
    """create a new directory."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except IOError as e:
        print(f"error creating directory: {e}")
        return False

def delete_directory(directory: str) -> bool:
    """delete a directory and its contents."""
    try:
        os.rmdir(directory)  # will only work if directory is empty
        return True
    except FileNotFoundError:
        print(f"directory not found: {directory}")
        return False
    except OSError as e:
        print(f"error deleting directory: {e}")
        return False

# using pathlib for modern file operations
def modern_file_operations():
    """demonstrate modern file operations using pathlib."""
    # create a path object
    path = Path("example")
    
    # create directory
    path.mkdir(exist_ok=True)
    
    # create file
    file_path = path / "test.txt"
    file_path.write_text("hello from pathlib!")
    
    # read file
    content = file_path.read_text()
    print(f"file content: {content}")
    
    # check if file exists
    print(f"file exists: {file_path.exists()}")
    
    # file properties
    print(f"file size: {file_path.stat().st_size} bytes")
    print(f"file extension: {file_path.suffix}")
    
    # delete file
    file_path.unlink()
    
    # delete directory
    path.rmdir()

# file properties and metadata
def file_metadata(filename: str):
    """display file metadata."""
    try:
        stats = os.stat(filename)
        print(f"file: {filename}")
        print(f"size: {stats.st_size} bytes")
        print(f"created: {stats.st_ctime}")
        print(f"modified: {stats.st_mtime}")
        print(f"accessed: {stats.st_atime}")
        print(f"permissions: {oct(stats.st_mode)[-3:]}")
    except FileNotFoundError:
        print(f"file not found: {filename}")
    except IOError as e:
        print(f"error getting metadata: {e}")

# example usage
def main():
    """demonstrate file operations."""
    # create and write to file
    create_file("test.txt", "hello, world!\n")
    append_to_file("test.txt", "this is a test file.")
    
    # read file
    content = read_file("test.txt")
    print(f"file content:\n{content}")
    
    # file metadata
    file_metadata("test.txt")
    
    # create directory
    create_directory("example_dir")
    
    # list files
    print("\nfiles in current directory:")
    for file in list_files():
        print(file)
    
    # cleanup
    delete_file("test.txt")
    delete_directory("example_dir")
    
    # modern file operations
    print("\nmodern file operations:")
    modern_file_operations()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - recursively walks through a directory
#    - counts files by type
#    - calculates total size
#    - generates a report

# 2. create a program that:
#    - monitors a directory for changes
#    - logs file creation/deletion/modification
#    - handles file move operations
#    - generates periodic reports

# 3. create a program that:
#    - implements a simple file backup system
#    - tracks file changes
#    - maintains backup history
#    - allows file restoration 