# memory-mapped file operations in python
# this module demonstrates how to use memory mapping for efficient file handling

import mmap
import os
from pathlib import Path
import tempfile
import struct

def demonstrate_basic_mmap():
    """shows basic memory-mapped file operations
    
    memory mapping allows you to:
    - treat a file as if it were in memory
    - access very large files efficiently
    - share memory between processes
    """
    # create a temporary file for demonstration
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # write some initial content
        content = b"hello, memory-mapped world!\n" * 1000
        temp_file.write(content)
        temp_file.flush()
        
        print("basic memory mapping:")
        
        # open the file and create a memory map
        with open(temp_file.name, "r+b") as file:
            # memory map the file
            with mmap.mmap(file.fileno(), 0) as mm:
                print(f"file size: {len(mm)} bytes")
                
                # read from the memory map
                print("\nreading first line:")
                first_line = mm.readline()
                print(f"content: {first_line.decode().strip()}")
                
                # modify the memory map
                print("\nmodifying content:")
                mm.seek(0)  # go back to start
                mm.write(b"modified content!")
                
                # read modified content
                mm.seek(0)
                modified = mm.readline()
                print(f"modified content: {modified.decode().strip()}")

def work_with_structured_data():
    """demonstrates using memory mapping with structured data
    
    this shows how to:
    - work with binary data structures
    - efficiently access large datasets
    - modify data in-place
    """
    # create a temporary file for our structured data
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # create some structured records (name, age, score)
        records = [
            (b"alice", 25, 95.5),
            (b"bob  ", 30, 85.0),
            (b"carol", 28, 90.5)
        ]
        
        # write records to file
        for name, age, score in records:
            # pack each record: 5 bytes for name, 4 bytes for age, 8 bytes for score
            record = struct.pack('5s i d', name, age, score)
            temp_file.write(record)
        
        temp_file.flush()
        
        print("\nstructured data with memory mapping:")
        
        # open file for memory mapping
        with open(temp_file.name, "r+b") as file:
            # calculate record size
            record_size = struct.calcsize('5s i d')
            
            # create memory map
            with mmap.mmap(file.fileno(), 0) as mm:
                # read and display all records
                print("\noriginal records:")
                for i in range(len(records)):
                    mm.seek(i * record_size)
                    record_bytes = mm.read(record_size)
                    name, age, score = struct.unpack('5s i d', record_bytes)
                    print(f"record {i + 1}: {name.decode().strip()}, {age}, {score}")
                
                # modify a record
                print("\nmodifying bob's score:")
                # locate bob's record
                mm.seek(record_size)  # second record
                # pack and write new data
                new_record = struct.pack('5s i d', b"bob  ", 30, 95.0)
                mm.write(new_record)
                
                # read modified record
                mm.seek(record_size)
                modified_bytes = mm.read(record_size)
                name, age, score = struct.unpack('5s i d', modified_bytes)
                print(f"modified record: {name.decode().strip()}, {age}, {score}")

def demonstrate_large_file_processing():
    """shows how to efficiently process large files using memory mapping
    
    this demonstrates:
    - handling files larger than available RAM
    - efficient searching in large files
    - modifying large files in-place
    """
    # create a large temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # write some repeated content to create a larger file
        line = b"this is a line of text that will be repeated many times.\n"
        for _ in range(10000):  # write 10000 lines
            temp_file.write(line)
        temp_file.flush()
        
        print("\nlarge file processing with memory mapping:")
        
        # get file size
        file_size = os.path.getsize(temp_file.name)
        print(f"file size: {file_size:,} bytes")
        
        # open file for memory mapping
        with open(temp_file.name, "r+b") as file:
            # create memory map
            with mmap.mmap(file.fileno(), 0) as mm:
                # search for a pattern
                pattern = b"line of text"
                print(f"\nsearching for: {pattern.decode()}")
                
                # find all occurrences
                position = 0
                count = 0
                
                while True:
                    position = mm.find(pattern, position)
                    if position == -1:  # pattern not found
                        break
                    count += 1
                    position += 1  # move to next position
                
                print(f"pattern found {count:,} times")
                
                # demonstrate random access
                print("\nrandom access demonstration:")
                # jump to middle of file
                middle = len(mm) // 2
                mm.seek(middle)
                # read a line from middle
                line = mm.readline()
                print(f"line from middle: {line.decode().strip()}")

def main():
    """runs all memory mapping demonstrations"""
    print("python memory-mapped file operations demonstration\n")
    
    demonstrate_basic_mmap()
    work_with_structured_data()
    demonstrate_large_file_processing()

if __name__ == "__main__":
    main() 