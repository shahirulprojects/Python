# file handling in python
# this file covers reading, writing, and managing files safely

# 1. reading files
# using with statement ensures file is properly closed after use
def read_entire_file(filename):
    """
    reads and returns the entire contents of a file
    
    args:
        filename (str): path to the file
    
    returns:
        str: file contents or None if error occurs
    """
    try:
        with open(filename, 'r') as file:
            # reads all content at once
            return file.read()
    except FileNotFoundError:
        print(f"sorry, the file '{filename}' was not found")
        return None
    except Exception as e:
        print(f"an error occurred: {str(e)}")
        return None

# reading file line by line
def read_file_lines(filename):
    """
    reads a file line by line to save memory
    
    args:
        filename (str): path to the file
    
    yields:
        str: each line from the file
    """
    try:
        with open(filename, 'r') as file:
            # reads one line at a time
            for line in file:
                # removes trailing newline
                yield line.strip()
    except FileNotFoundError:
        print(f"sorry, the file '{filename}' was not found")
    except Exception as e:
        print(f"an error occurred: {str(e)}")

# 2. writing files
def write_to_file(filename, content):
    """
    writes content to a file (overwrites existing content)
    
    args:
        filename (str): path to the file
        content (str): content to write
    
    returns:
        bool: true if writing was successful
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"failed to write to file: {str(e)}")
        return False

def append_to_file(filename, content):
    """
    appends content to the end of a file
    
    args:
        filename (str): path to the file
        content (str): content to append
    
    returns:
        bool: true if appending was successful
    """
    try:
        with open(filename, 'a') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"failed to append to file: {str(e)}")
        return False

# 3. practical examples

# example: simple note-taking application
class NoteManager:
    def __init__(self, filename):
        self.filename = filename
    
    def add_note(self, note):
        """adds a new note with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_note = f"[{timestamp}] {note}\n"
        return append_to_file(self.filename, formatted_note)
    
    def read_notes(self):
        """reads and prints all notes"""
        print("your notes:")
        print("-" * 40)
        for line in read_file_lines(self.filename):
            print(line)
        print("-" * 40)

# example usage
notes = NoteManager("my_notes.txt")
notes.add_note("remember to learn python file handling")
notes.add_note("practice makes perfect")
notes.read_notes()

# 4. working with csv files
import csv

def save_user_data(filename, users):
    """
    saves user data to a csv file
    
    args:
        filename (str): path to the csv file
        users (list): list of user dictionaries
    """
    try:
        with open(filename, 'w', newline='') as file:
            # get field names from first user dictionary
            if users:
                fieldnames = users[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # write header and data
                writer.writeheader()
                writer.writerows(users)
                return True
        return False
    except Exception as e:
        print(f"failed to save csv: {str(e)}")
        return False

def read_user_data(filename):
    """
    reads user data from a csv file
    
    args:
        filename (str): path to the csv file
    
    returns:
        list: list of user dictionaries
    """
    users = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
        return users
    except Exception as e:
        print(f"failed to read csv: {str(e)}")
        return []

# example usage
users = [
    {"name": "alice", "age": "25", "city": "new york"},
    {"name": "bob", "age": "30", "city": "san francisco"}
]

# save and read user data
save_user_data("users.csv", users)
loaded_users = read_user_data("users.csv")

# 5. file and directory operations
import os

def create_directory(directory):
    """
    creates a directory if it doesn't exist
    
    args:
        directory (str): path to create
    
    returns:
        bool: true if directory exists or was created
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        print(f"failed to create directory: {str(e)}")
        return False

def list_files(directory):
    """
    lists all files in a directory
    
    args:
        directory (str): directory to list
    
    returns:
        list: list of filenames
    """
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"failed to list directory: {str(e)}")
        return []

# 6. safe file operations
def safe_delete_file(filename):
    """
    safely deletes a file if it exists
    
    args:
        filename (str): file to delete
    
    returns:
        bool: true if file was deleted or didn't exist
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
        return True
    except Exception as e:
        print(f"failed to delete file: {str(e)}")
        return False

# example usage of file operations
create_directory("data")
write_to_file("data/test.txt", "hello, python!")
files = list_files("data")
print(f"files in data directory: {files}")
safe_delete_file("data/test.txt") 