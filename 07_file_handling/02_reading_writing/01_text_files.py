# reading and writing text files in python
from typing import List, Optional, Iterator
import os

def read_entire_file(filename: str) -> Optional[str]:
    """read entire file content at once."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        print(f"error reading file: {e}")
        return None

def read_lines(filename: str) -> Optional[List[str]]:
    """read file line by line into a list."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.readlines()
    except IOError as e:
        print(f"error reading file: {e}")
        return None

def read_lines_iterator(filename: str) -> Iterator[str]:
    """read file line by line using an iterator."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except IOError as e:
        print(f"error reading file: {e}")

def write_text(filename: str, content: str) -> bool:
    """write text content to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"error writing file: {e}")
        return False

def write_lines(filename: str, lines: List[str]) -> bool:
    """write list of lines to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in lines)
        return True
    except IOError as e:
        print(f"error writing file: {e}")
        return False

def append_text(filename: str, content: str) -> bool:
    """append text to existing file."""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"error appending to file: {e}")
        return False

def read_with_context(filename: str, start_line: int, num_lines: int) -> List[str]:
    """read specific lines with context."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # skip to start line
            for _ in range(start_line - 1):
                next(f, None)
            
            # read requested lines
            return [next(f, '').strip() for _ in range(num_lines)]
    except IOError as e:
        print(f"error reading file: {e}")
        return []

def search_text(filename: str, search_term: str) -> List[tuple[int, str]]:
    """search for text in file and return matching lines with line numbers."""
    matches = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if search_term in line:
                    matches.append((i, line.strip()))
        return matches
    except IOError as e:
        print(f"error searching file: {e}")
        return []

def count_words(filename: str) -> dict[str, int]:
    """count word frequency in file."""
    word_count = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().lower().split()
                for word in words:
                    word_count[word] = word_count.get(word, 0) + 1
        return word_count
    except IOError as e:
        print(f"error counting words: {e}")
        return {}

# example usage
def main():
    """demonstrate text file operations."""
    # create a sample file
    content = """This is a test file.
It has multiple lines.
We can read and write text.
This is the last line."""
    
    filename = "sample.txt"
    
    # write content
    print("writing to file...")
    write_text(filename, content)
    
    # read entire file
    print("\nreading entire file:")
    print(read_entire_file(filename))
    
    # read line by line
    print("\nreading line by line:")
    for line in read_lines_iterator(filename):
        print(f"line: {line}")
    
    # search for text
    print("\nsearching for 'line':")
    matches = search_text(filename, "line")
    for line_num, line in matches:
        print(f"line {line_num}: {line}")
    
    # count words
    print("\nword frequency:")
    word_counts = count_words(filename)
    for word, count in sorted(word_counts.items()):
        print(f"{word}: {count}")
    
    # append text
    print("\nappending text...")
    append_text(filename, "\nThis line was appended.")
    
    # read with context
    print("\nreading lines 2-3:")
    context_lines = read_with_context(filename, 2, 2)
    for line in context_lines:
        print(line)
    
    # cleanup
    os.remove(filename)

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - reads a text file
#    - analyzes sentence structure
#    - counts sentences, words per sentence
#    - generates readability statistics

# 2. create a program that:
#    - merges multiple text files
#    - handles different encodings
#    - removes duplicate lines
#    - sorts content

# 3. create a program that:
#    - implements a simple text file diff tool
#    - shows line-by-line differences
#    - highlights changes
#    - generates a summary report 