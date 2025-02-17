# comprehensions and generator expressions in python
# this file explains powerful ways to create lists, sets, and dictionaries

# 1. list comprehensions
# these are concise ways to create lists based on existing sequences

# traditional way vs list comprehension
numbers = [1, 2, 3, 4, 5]

# traditional way using a for loop
squares_traditional = []
for num in numbers:
    # adds square of each number
    squares_traditional.append(num ** 2)

# same thing using list comprehension
squares_comprehension = [num ** 2 for num in numbers]    # [1, 4, 9, 16, 25]

# 2. filtering with list comprehensions
# we can add conditions to filter elements

# get only even numbers
# traditional way
even_traditional = []
for num in numbers:
    if num % 2 == 0:
        # adds only even numbers
        even_traditional.append(num)

# same thing with list comprehension
even_comprehension = [num for num in numbers if num % 2 == 0]    # [2, 4]

# 3. nested list comprehensions
# we can create more complex structures

# create a multiplication table
# each inner list is a row of the table
multiplication_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]

# example output:
# [[1, 2, 3, 4, 5],     # 1 times 1,2,3,4,5
#  [2, 4, 6, 8, 10],    # 2 times 1,2,3,4,5
#  [3, 6, 9, 12, 15],   # and so on...
#  [4, 8, 12, 16, 20],
#  [5, 10, 15, 20, 25]]

# 4. set and dictionary comprehensions
# similar syntax works for sets and dictionaries

# set comprehension (removes duplicates)
numbers_with_duplicates = [1, 2, 2, 3, 3, 3]
unique_squares = {num ** 2 for num in numbers_with_duplicates}    # {1, 4, 9}

# dictionary comprehension
# creates a dictionary of number: square pairs
number_squares = {num: num ** 2 for num in range(1, 6)}
# result: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 5. generator expressions
# like list comprehensions but more memory efficient
# they generate values one at a time instead of creating the whole list

# list comprehension (creates whole list in memory)
sum_squares_list = sum([x ** 2 for x in range(1000)])

# generator expression (generates values as needed)
sum_squares_gen = sum(x ** 2 for x in range(1000))    # notice no square brackets

# 6. practical examples

def get_valid_emails(emails):
    """
    filters a list of emails to get only valid ones
    
    args:
        emails (list): list of email strings
    
    returns:
        list: valid email addresses
    """
    # checks for basic email format using comprehension
    return [email for email in emails if '@' in email and '.' in email]

# example usage
email_list = ['user@example.com', 'invalid.email', 'another@domain.com']
valid_emails = get_valid_emails(email_list)    # ['user@example.com', 'another@domain.com']

def word_lengths(sentence):
    """
    creates a dictionary of words and their lengths
    
    args:
        sentence (str): input sentence
    
    returns:
        dict: word-length pairs
    """
    # splits sentence into words and creates word: length pairs
    return {word: len(word) for word in sentence.split()}

# example usage
text = "python is amazing"
lengths = word_lengths(text)    # {'python': 6, 'is': 2, 'amazing': 7}

# 7. advanced examples

def matrix_operations():
    """demonstrates advanced matrix operations using comprehensions"""
    
    # create two 2x2 matrices
    matrix_a = [[1, 2],
                [3, 4]]
    
    matrix_b = [[5, 6],
                [7, 8]]
    
    # matrix addition using nested comprehensions
    matrix_sum = [[a + b for a, b in zip(row_a, row_b)]
                  for row_a, row_b in zip(matrix_a, matrix_b)]
    
    # transpose matrix (swap rows and columns)
    transpose = [[row[i] for row in matrix_a]
                 for i in range(len(matrix_a[0]))]
    
    return matrix_sum, transpose

# 8. memory efficient data processing
def process_large_file(filename):
    """
    processes a large file line by line using generator expression
    
    args:
        filename (str): file to process
    """
    # reads and processes file without loading it entirely into memory
    with open(filename, 'r') as file:
        # generator expression to process lines
        processed_lines = (line.strip().upper() for line in file)
        
        # process one line at a time
        for processed_line in processed_lines:
            # do something with each line
            print(processed_line)

# 9. conditional comprehensions
def categorize_numbers(numbers):
    """
    categorizes numbers as 'even' or 'odd'
    
    args:
        numbers (list): list of numbers
    
    returns:
        dict: number categorization
    """
    return {num: 'even' if num % 2 == 0 else 'odd'
            for num in numbers}

# example usage
nums = [1, 2, 3, 4, 5]
categories = categorize_numbers(nums)
# result: {1: 'odd', 2: 'even', 3: 'odd', 4: 'even', 5: 'odd'} 