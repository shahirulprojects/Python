# working with binary files in python
import struct
from typing import List, Optional, BinaryIO
import pickle
from pathlib import Path
import io

def write_binary_numbers(filename: str, numbers: List[int]) -> bool:
    """write list of integers to binary file."""
    try:
        with open(filename, 'wb') as f:
            # write length of list first
            f.write(struct.pack('I', len(numbers)))
            # write each number as 4-byte integer
            for num in numbers:
                f.write(struct.pack('i', num))
        return True
    except IOError as e:
        print(f"error writing binary file: {e}")
        return False

def read_binary_numbers(filename: str) -> Optional[List[int]]:
    """read list of integers from binary file."""
    try:
        numbers = []
        with open(filename, 'rb') as f:
            # read length of list
            length = struct.unpack('I', f.read(4))[0]
            # read each number
            for _ in range(length):
                num = struct.unpack('i', f.read(4))[0]
                numbers.append(num)
        return numbers
    except IOError as e:
        print(f"error reading binary file: {e}")
        return None

def write_binary_struct(filename: str, data: dict) -> bool:
    """write structured data to binary file."""
    try:
        with open(filename, 'wb') as f:
            # write string with length prefix
            name = data.get('name', '').encode('utf-8')
            f.write(struct.pack('I', len(name)))
            f.write(name)
            
            # write integers
            f.write(struct.pack('i', data.get('age', 0)))
            f.write(struct.pack('i', data.get('score', 0)))
            
            # write float
            f.write(struct.pack('f', data.get('weight', 0.0)))
        return True
    except IOError as e:
        print(f"error writing binary struct: {e}")
        return False

def read_binary_struct(filename: str) -> Optional[dict]:
    """read structured data from binary file."""
    try:
        with open(filename, 'rb') as f:
            # read string with length prefix
            name_length = struct.unpack('I', f.read(4))[0]
            name = f.read(name_length).decode('utf-8')
            
            # read integers
            age = struct.unpack('i', f.read(4))[0]
            score = struct.unpack('i', f.read(4))[0]
            
            # read float
            weight = struct.unpack('f', f.read(4))[0]
            
            return {
                'name': name,
                'age': age,
                'score': score,
                'weight': weight
            }
    except IOError as e:
        print(f"error reading binary struct: {e}")
        return None

def write_pickle(filename: str, data: Any) -> bool:
    """write data to pickle file."""
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        return True
    except IOError as e:
        print(f"error writing pickle file: {e}")
        return False

def read_pickle(filename: str) -> Optional[Any]:
    """read data from pickle file."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except IOError as e:
        print(f"error reading pickle file: {e}")
        return None

class BinaryFileHandler:
    """class for handling binary file operations."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.file: Optional[BinaryIO] = None
    
    def __enter__(self) -> 'BinaryFileHandler':
        self.file = open(self.filename, 'wb+')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
    
    def write_int(self, value: int) -> bool:
        """write single integer."""
        if self.file:
            self.file.write(struct.pack('i', value))
            return True
        return False
    
    def write_float(self, value: float) -> bool:
        """write single float."""
        if self.file:
            self.file.write(struct.pack('f', value))
            return True
        return False
    
    def write_string(self, value: str) -> bool:
        """write string with length prefix."""
        if self.file:
            encoded = value.encode('utf-8')
            self.file.write(struct.pack('I', len(encoded)))
            self.file.write(encoded)
            return True
        return False
    
    def seek_to_start(self):
        """seek to start of file."""
        if self.file:
            self.file.seek(0)
    
    def read_int(self) -> Optional[int]:
        """read single integer."""
        if self.file:
            try:
                return struct.unpack('i', self.file.read(4))[0]
            except struct.error:
                return None
        return None
    
    def read_float(self) -> Optional[float]:
        """read single float."""
        if self.file:
            try:
                return struct.unpack('f', self.file.read(4))[0]
            except struct.error:
                return None
        return None
    
    def read_string(self) -> Optional[str]:
        """read string with length prefix."""
        if self.file:
            try:
                length = struct.unpack('I', self.file.read(4))[0]
                return self.file.read(length).decode('utf-8')
            except (struct.error, UnicodeDecodeError):
                return None
        return None

# example usage
def main():
    """demonstrate binary file operations."""
    # write and read numbers
    numbers = [1, 2, 3, 4, 5]
    numbers_file = "numbers.bin"
    
    print("writing numbers to binary file...")
    write_binary_numbers(numbers_file, numbers)
    
    print("\nreading numbers from binary file:")
    read_numbers = read_binary_numbers(numbers_file)
    print(f"numbers: {read_numbers}")
    
    # write and read struct
    person = {
        'name': 'John Doe',
        'age': 30,
        'score': 95,
        'weight': 75.5
    }
    struct_file = "person.bin"
    
    print("\nwriting struct to binary file...")
    write_binary_struct(struct_file, person)
    
    print("\nreading struct from binary file:")
    read_person = read_binary_struct(struct_file)
    print(f"person: {read_person}")
    
    # using binary file handler
    handler_file = "handler.bin"
    print("\nusing binary file handler:")
    with BinaryFileHandler(handler_file) as handler:
        handler.write_int(42)
        handler.write_float(3.14)
        handler.write_string("hello")
        
        handler.seek_to_start()
        print(f"int: {handler.read_int()}")
        print(f"float: {handler.read_float()}")
        print(f"string: {handler.read_string()}")
    
    # pickle example
    data = {
        'numbers': numbers,
        'person': person,
        'extra': [1, 2, 3],
        'nested': {'a': 1, 'b': 2}
    }
    pickle_file = "data.pickle"
    
    print("\nwriting pickle file...")
    write_pickle(pickle_file, data)
    
    print("\nreading pickle file:")
    loaded_data = read_pickle(pickle_file)
    print(f"loaded data: {loaded_data}")
    
    # cleanup
    for file in [numbers_file, struct_file, handler_file, pickle_file]:
        Path(file).unlink()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - implements a simple binary file format
#    - supports different data types
#    - includes checksums
#    - handles endianness

# 2. create a program that:
#    - reads and writes image data
#    - manipulates pixel values
#    - applies filters
#    - handles different image formats

# 3. create a program that:
#    - implements a binary file compressor
#    - uses basic compression algorithms
#    - maintains file integrity
#    - provides progress updates 