# working with CSV files in python
import csv
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd

def write_csv(filename: str, data: List[List[Any]], headers: Optional[List[str]] = None) -> bool:
    """write data to CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)
        return True
    except IOError as e:
        print(f"error writing CSV: {e}")
        return False

def read_csv(filename: str) -> List[List[str]]:
    """read data from CSV file."""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
    except IOError as e:
        print(f"error reading CSV: {e}")
        return []

def write_csv_dict(filename: str, data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> bool:
    """write dictionary data to CSV file."""
    try:
        if not fieldnames and data:
            fieldnames = list(data[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except IOError as e:
        print(f"error writing CSV: {e}")
        return False

def read_csv_dict(filename: str) -> List[Dict[str, str]]:
    """read CSV file into list of dictionaries."""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data
    except IOError as e:
        print(f"error reading CSV: {e}")
        return []

def append_to_csv(filename: str, row: List[Any]) -> bool:
    """append a row to existing CSV file."""
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return True
    except IOError as e:
        print(f"error appending to CSV: {e}")
        return False

def filter_csv(filename: str, column: str, value: Any) -> List[Dict[str, str]]:
    """filter CSV data based on column value."""
    try:
        data = read_csv_dict(filename)
        return [row for row in data if row.get(column) == str(value)]
    except Exception as e:
        print(f"error filtering CSV: {e}")
        return []

# using pandas for advanced CSV operations
def pandas_csv_operations(filename: str):
    """demonstrate CSV operations using pandas."""
    try:
        # read CSV into DataFrame
        df = pd.read_csv(filename)
        
        # basic information
        print("\nDataFrame Info:")
        print(df.info())
        
        # summary statistics
        print("\nSummary Statistics:")
        print(df.describe())
        
        # value counts for a column
        if 'category' in df.columns:
            print("\nCategory Counts:")
            print(df['category'].value_counts())
        
        # group by operations
        if 'category' in df.columns and 'value' in df.columns:
            print("\nMean Values by Category:")
            print(df.groupby('category')['value'].mean())
        
        return df
    except Exception as e:
        print(f"error in pandas operations: {e}")
        return None

# example usage
def main():
    """demonstrate CSV file operations."""
    # sample data
    headers = ['name', 'age', 'city']
    data = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'London'],
        ['Charlie', 35, 'Paris']
    ]
    
    # write CSV file
    filename = "people.csv"
    print("writing CSV file...")
    write_csv(filename, data, headers)
    
    # read CSV file
    print("\nreading CSV file:")
    csv_data = read_csv(filename)
    for row in csv_data:
        print(row)
    
    # dictionary data
    dict_data = [
        {'name': 'Alice', 'age': 25, 'city': 'New York'},
        {'name': 'Bob', 'age': 30, 'city': 'London'},
        {'name': 'Charlie', 'age': 35, 'city': 'Paris'}
    ]
    
    # write dictionary CSV
    dict_filename = "people_dict.csv"
    print("\nwriting dictionary CSV...")
    write_csv_dict(dict_filename, dict_data)
    
    # read dictionary CSV
    print("\nreading dictionary CSV:")
    dict_csv_data = read_csv_dict(dict_filename)
    for row in dict_csv_data:
        print(row)
    
    # filter data
    print("\nfiltering by city 'London':")
    london_people = filter_csv(dict_filename, 'city', 'London')
    for person in london_people:
        print(person)
    
    # pandas operations
    print("\npandas operations:")
    df = pandas_csv_operations(dict_filename)
    if df is not None:
        print("\nDataFrame head:")
        print(df.head())
    
    # cleanup
    Path(filename).unlink()
    Path(dict_filename).unlink()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - reads multiple CSV files
#    - merges them based on a common key
#    - handles missing data
#    - outputs a combined report

# 2. create a program that:
#    - validates CSV data against a schema
#    - checks data types and constraints
#    - generates error reports
#    - fixes common issues

# 3. create a program that:
#    - processes large CSV files in chunks
#    - performs data transformations
#    - handles memory efficiently
#    - shows progress updates 