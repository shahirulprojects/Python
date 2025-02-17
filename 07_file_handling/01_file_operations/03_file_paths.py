# working with file paths in python
# this module shows how to handle file paths correctly across different operating systems

import os
from pathlib import Path
import shutil
import tempfile

# pathlib is the modern way to handle paths in python
# it provides an object-oriented interface to filesystem paths
# and works consistently across all operating systems

def demonstrate_path_basics():
    """shows basic path operations using pathlib
    
    this helps you understand:
    - how to create paths safely
    - how to join paths together
    - how to get path information
    """
    # create a path object (works on all operating systems)
    current_dir = Path.cwd()  # get current working directory
    
    print("basic path operations:")
    print(f"current directory: {current_dir}")
    print(f"parent directory: {current_dir.parent}")
    print(f"absolute path: {current_dir.absolute()}")
    
    # joining paths (works on all operating systems)
    data_dir = current_dir / 'data'  # creates path to 'data' directory
    file_path = data_dir / 'example.txt'  # creates path to a file
    
    print(f"\njoined paths:")
    print(f"data directory: {data_dir}")
    print(f"file path: {file_path}")
    
    # getting path components
    print(f"\npath components:")
    print(f"file name: {file_path.name}")
    print(f"stem (name without extension): {file_path.stem}")
    print(f"extension: {file_path.suffix}")
    print(f"parent directory: {file_path.parent}")

def work_with_temporary_paths():
    """demonstrates how to work with temporary files and directories
    
    temporary files are useful for:
    - storing intermediate results
    - processing data without cluttering the filesystem
    - ensuring cleanup after the program ends
    """
    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # create some files in the temporary directory
        file1_path = temp_path / 'test1.txt'
        file2_path = temp_path / 'test2.txt'
        
        # write some content
        file1_path.write_text("this is a test file")
        file2_path.write_text("another test file")
        
        print("\ntemporary file operations:")
        print(f"temporary directory: {temp_path}")
        print(f"files in temporary directory: {list(temp_path.glob('*.txt'))}")
        
        # read content back
        print(f"content of {file1_path.name}: {file1_path.read_text()}")
    
    # the temporary directory and its contents are automatically cleaned up
    print("temporary directory has been cleaned up")

def handle_path_patterns():
    """shows how to work with file patterns and searching
    
    this helps you:
    - find files matching patterns
    - recursively search directories
    - filter files by type
    """
    # create a temporary directory structure for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # create some test files
        (temp_path / 'doc1.txt').write_text("document 1")
        (temp_path / 'doc2.txt').write_text("document 2")
        (temp_path / 'image.jpg').write_text("fake image")
        
        # create a subdirectory with files
        sub_dir = temp_path / 'subdir'
        sub_dir.mkdir()
        (sub_dir / 'doc3.txt').write_text("document 3")
        
        print("\nfile pattern matching:")
        
        # find all .txt files
        print("\nall .txt files:")
        for txt_file in temp_path.glob('*.txt'):
            print(f"- {txt_file.name}")
        
        # find all files recursively
        print("\nall files (recursive):")
        for file_path in temp_path.rglob('*'):
            if file_path.is_file():  # check if it's a file (not directory)
                print(f"- {file_path.relative_to(temp_path)}")

def demonstrate_path_operations():
    """shows common path operations and best practices
    
    learn how to:
    - check if paths exist
    - create directories
    - move and copy files
    - handle paths safely
    """
    # create a temporary directory for our examples
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # create a directory structure
        data_dir = temp_path / 'data'
        backup_dir = temp_path / 'backup'
        
        print("\npath operations:")
        
        # create directories
        data_dir.mkdir(exist_ok=True)  # exist_ok=True prevents errors if directory exists
        backup_dir.mkdir(exist_ok=True)
        
        # create a test file
        test_file = data_dir / 'test.txt'
        test_file.write_text("this is test content")
        
        print(f"created file: {test_file}")
        print(f"file exists: {test_file.exists()}")
        print(f"is file: {test_file.is_file()}")
        print(f"is directory: {test_file.is_dir()}")
        
        # copy file to backup
        backup_file = backup_dir / test_file.name
        shutil.copy2(test_file, backup_file)
        print(f"\ncopied to: {backup_file}")
        
        # get file information
        file_stat = test_file.stat()
        print(f"\nfile statistics:")
        print(f"size: {file_stat.st_size} bytes")
        print(f"last modified: {file_stat.st_mtime}")
        
        # demonstrate path comparison
        print(f"\npath comparison:")
        print(f"same file? {test_file.samefile(backup_file)}")

def main():
    """runs all the path handling demonstrations"""
    print("python path handling demonstration\n")
    
    demonstrate_path_basics()
    work_with_temporary_paths()
    handle_path_patterns()
    demonstrate_path_operations()

if __name__ == "__main__":
    main() 