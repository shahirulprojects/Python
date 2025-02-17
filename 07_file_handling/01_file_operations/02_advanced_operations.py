# advanced file system operations in python
import os
import shutil
import stat
import time
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional
from datetime import datetime
import hashlib
import fnmatch
import tempfile
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileSystemWatcher(FileSystemEventHandler):
    """file system event handler for monitoring changes."""
    
    def __init__(self):
        self.changes: List[Dict[str, Any]] = []
    
    def on_created(self, event):
        if not event.is_directory:
            self.changes.append({
                'type': 'created',
                'path': event.src_path,
                'time': datetime.now()
            })
    
    def on_modified(self, event):
        if not event.is_directory:
            self.changes.append({
                'type': 'modified',
                'path': event.src_path,
                'time': datetime.now()
            })
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.changes.append({
                'type': 'deleted',
                'path': event.src_path,
                'time': datetime.now()
            })

def calculate_file_hash(filename: str, algorithm: str = 'sha256') -> Optional[str]:
    """calculate hash of file contents."""
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"error calculating hash: {e}")
        return None

def find_duplicate_files(directory: str) -> Dict[str, List[str]]:
    """find duplicate files based on content hash."""
    hash_dict: Dict[str, List[str]] = {}
    
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hash_dict.setdefault(file_hash, []).append(filepath)
    
    # return only duplicates
    return {k: v for k, v in hash_dict.items() if len(v) > 1}

def find_files(directory: str, pattern: str) -> Generator[str, None, None]:
    """find files matching pattern recursively."""
    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(root, filename)

def get_file_info(filename: str) -> Dict[str, Any]:
    """get detailed file information."""
    try:
        stat_info = os.stat(filename)
        return {
            'name': os.path.basename(filename),
            'path': os.path.abspath(filename),
            'size': stat_info.st_size,
            'created': datetime.fromtimestamp(stat_info.st_ctime),
            'modified': datetime.fromtimestamp(stat_info.st_mtime),
            'accessed': datetime.fromtimestamp(stat_info.st_atime),
            'permissions': stat.filemode(stat_info.st_mode),
            'is_file': os.path.isfile(filename),
            'is_dir': os.path.isdir(filename),
            'is_link': os.path.islink(filename),
            'hash': calculate_file_hash(filename) if os.path.isfile(filename) else None
        }
    except Exception as e:
        print(f"error getting file info: {e}")
        return {}

def create_hard_link(source: str, link_name: str) -> bool:
    """create a hard link to a file."""
    try:
        os.link(source, link_name)
        return True
    except Exception as e:
        print(f"error creating hard link: {e}")
        return False

def create_symbolic_link(source: str, link_name: str) -> bool:
    """create a symbolic link to a file or directory."""
    try:
        os.symlink(source, link_name)
        return True
    except Exception as e:
        print(f"error creating symbolic link: {e}")
        return False

def set_file_permissions(filename: str, mode: int) -> bool:
    """set file permissions using octal mode."""
    try:
        os.chmod(filename, mode)
        return True
    except Exception as e:
        print(f"error setting permissions: {e}")
        return False

def monitor_directory(directory: str, duration: int = 60) -> List[Dict[str, Any]]:
    """monitor directory for changes for specified duration."""
    event_handler = FileSystemWatcher()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    
    try:
        time.sleep(duration)
    finally:
        observer.stop()
        observer.join()
    
    return event_handler.changes

def create_secure_tempfile(content: str = "") -> str:
    """create a secure temporary file."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            temp.write(content)
            # set restrictive permissions
            os.chmod(temp.name, stat.S_IRUSR | stat.S_IWUSR)
            return temp.name
    except Exception as e:
        print(f"error creating temp file: {e}")
        return ""

def get_disk_usage(path: str = ".") -> Dict[str, int]:
    """get disk usage information."""
    try:
        usage = shutil.disk_usage(path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free
        }
    except Exception as e:
        print(f"error getting disk usage: {e}")
        return {}

# example usage
def main():
    """demonstrate advanced file system operations."""
    # create test directory and files
    test_dir = "test_directory"
    os.makedirs(test_dir, exist_ok=True)
    
    # create some test files
    for i in range(3):
        with open(os.path.join(test_dir, f"file{i}.txt"), 'w') as f:
            f.write(f"This is test file {i}\n")
    
    # create duplicate files
    shutil.copy(os.path.join(test_dir, "file0.txt"),
                os.path.join(test_dir, "file0_duplicate.txt"))
    
    # find duplicate files
    print("finding duplicate files:")
    duplicates = find_duplicate_files(test_dir)
    for hash_value, file_list in duplicates.items():
        print(f"\nhash: {hash_value}")
        for file in file_list:
            print(f"  {file}")
    
    # find files by pattern
    print("\nfinding files by pattern:")
    for file in find_files(test_dir, "*.txt"):
        print(file)
    
    # get file information
    print("\nfile information:")
    file_path = os.path.join(test_dir, "file0.txt")
    info = get_file_info(file_path)
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # create links
    if platform.system() != "Windows":  # hard links not fully supported on Windows
        print("\ncreating links:")
        hard_link = os.path.join(test_dir, "hard_link.txt")
        sym_link = os.path.join(test_dir, "sym_link.txt")
        
        create_hard_link(file_path, hard_link)
        create_symbolic_link(file_path, sym_link)
        
        print(f"created hard link: {hard_link}")
        print(f"created symbolic link: {sym_link}")
    
    # set file permissions
    if platform.system() != "Windows":  # different permission model on Windows
        print("\nsetting file permissions:")
        set_file_permissions(file_path, 0o644)  # rw-r--r--
        print(f"new permissions: {stat.filemode(os.stat(file_path).st_mode)}")
    
    # monitor directory
    print("\nmonitoring directory for 5 seconds...")
    changes = monitor_directory(test_dir, 5)
    for change in changes:
        print(f"{change['type']}: {change['path']} at {change['time']}")
    
    # create secure temporary file
    print("\ncreating secure temporary file:")
    temp_file = create_secure_tempfile("sensitive data")
    print(f"temporary file created: {temp_file}")
    
    # get disk usage
    print("\ndisk usage:")
    usage = get_disk_usage()
    for key, value in usage.items():
        print(f"{key}: {value / (1024**3):.2f} GB")
    
    # cleanup
    shutil.rmtree(test_dir)
    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - implements a file versioning system
#    - tracks file changes
#    - maintains metadata
#    - supports rollback operations

# 2. create a program that:
#    - monitors multiple directories
#    - filters events by type
#    - logs changes to database
#    - sends notifications

# 3. create a program that:
#    - analyzes disk usage patterns
#    - generates reports
#    - identifies large files
#    - suggests cleanup actions 