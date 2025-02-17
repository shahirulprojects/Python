# common built-in python modules
import os  # operating system interface
import sys  # system-specific parameters and functions
import datetime  # basic date and time types
import math  # mathematical functions
import random  # generate random numbers
import json  # JSON encoder and decoder
import csv  # CSV file reading and writing
import argparse  # parser for command-line options
import collections  # specialized container datatypes

# os module examples
print("os module examples:")
print(f"current directory: {os.getcwd()}")
print(f"directory contents: {os.listdir('.')}")
print(f"os name: {os.name}")
print(f"path separator: {os.path.sep}")

# creating and removing directories
try:
    os.mkdir("test_dir")
    print("\ncreated test directory")
    os.rmdir("test_dir")
    print("removed test directory")
except FileExistsError:
    print("\ntest directory already exists")

# path manipulation
file_path = os.path.join("folder", "subfolder", "file.txt")
print(f"\njoined path: {file_path}")
print(f"base name: {os.path.basename(file_path)}")
print(f"directory name: {os.path.dirname(file_path)}")

# sys module examples
print("\nsys module examples:")
print(f"python version: {sys.version}")
print(f"platform: {sys.platform}")
print(f"python path: {sys.path}")

# datetime module examples
print("\ndatetime module examples:")
now = datetime.datetime.now()
print(f"current datetime: {now}")
print(f"formatted date: {now.strftime('%Y-%m-%d')}")
print(f"formatted time: {now.strftime('%H:%M:%S')}")

# date arithmetic
future_date = now + datetime.timedelta(days=7)
print(f"date after 7 days: {future_date.date()}")

# math module examples
print("\nmath module examples:")
print(f"pi: {math.pi}")
print(f"square root of 16: {math.sqrt(16)}")
print(f"ceil of 3.7: {math.ceil(3.7)}")
print(f"floor of 3.7: {math.floor(3.7)}")
print(f"factorial of 5: {math.factorial(5)}")

# random module examples
print("\nrandom module examples:")
print(f"random float: {random.random()}")
print(f"random integer (1-10): {random.randint(1, 10)}")
numbers = [1, 2, 3, 4, 5]
print(f"original list: {numbers}")
random.shuffle(numbers)
print(f"shuffled list: {numbers}")
print(f"random choice: {random.choice(numbers)}")

# json module examples
print("\njson module examples:")
data = {
    "name": "alice",
    "age": 25,
    "city": "new york"
}

# converting to JSON string
json_string = json.dumps(data, indent=2)
print("json string:")
print(json_string)

# parsing JSON string
parsed_data = json.loads(json_string)
print("\nparsed data:")
print(f"name: {parsed_data['name']}")

# csv module examples
print("\ncsv module examples:")
# writing CSV
csv_data = [
    ["name", "age", "city"],
    ["alice", "25", "new york"],
    ["bob", "30", "london"]
]

with open("example.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
print("wrote data to example.csv")

# reading CSV
with open("example.csv", "r") as file:
    reader = csv.reader(file)
    print("\nreading from csv:")
    for row in reader:
        print(row)

# cleanup
os.remove("example.csv")

# argparse module examples
def setup_argument_parser():
    parser = argparse.ArgumentParser(description="example argument parser")
    parser.add_argument("--name", default="user", help="your name")
    parser.add_argument("--count", type=int, default=1, help="number of greetings")
    return parser

# collections module examples
print("\ncollections module examples:")
# Counter
words = ["apple", "banana", "apple", "cherry", "date", "banana"]
counter = collections.Counter(words)
print(f"word counts: {counter}")

# defaultdict
dd = collections.defaultdict(list)
for word in words:
    dd[len(word)].append(word)
print("\nwords grouped by length:")
for length, words_list in dd.items():
    print(f"length {length}: {words_list}")

# deque (double-ended queue)
queue = collections.deque([1, 2, 3])
queue.append(4)  # add to right
queue.appendleft(0)  # add to left
print(f"\ndeque: {queue}")
print(f"pop right: {queue.pop()}")
print(f"pop left: {queue.popleft()}")
print(f"final deque: {queue}")

# practice exercises:
# 1. create a program that:
#    - uses os.walk to traverse a directory tree
#    - counts files by extension
#    - calculates total size of files
#    - generates a report

# 2. create a program that:
#    - reads a JSON configuration file
#    - validates the configuration
#    - applies defaults for missing values
#    - saves the updated configuration

# 3. create a program that:
#    - processes a CSV file with data
#    - performs calculations on numeric columns
#    - generates summary statistics
#    - writes results to a new CSV file

# example solution for #1:
def analyze_directory(path: str) -> dict:
    """analyze directory contents recursively."""
    stats = {
        'extensions': collections.Counter(),
        'total_size': 0,
        'file_count': 0,
        'dir_count': 0
    }
    
    for root, dirs, files in os.walk(path):
        stats['dir_count'] += len(dirs)
        stats['file_count'] += len(files)
        
        for file in files:
            file_path = os.path.join(root, file)
            # get file extension
            _, ext = os.path.splitext(file)
            stats['extensions'][ext or 'no_extension'] += 1
            # get file size
            try:
                stats['total_size'] += os.path.getsize(file_path)
            except OSError:
                continue
    
    return stats

# test the directory analyzer
if __name__ == "__main__":
    current_dir = os.getcwd()
    print("\ndirectory analysis:")
    stats = analyze_directory(current_dir)
    print(f"\ntotal directories: {stats['dir_count']}")
    print(f"total files: {stats['file_count']}")
    print(f"total size: {stats['total_size']:,} bytes")
    print("\nfiles by extension:")
    for ext, count in stats['extensions'].most_common():
        print(f"{ext}: {count} files") 