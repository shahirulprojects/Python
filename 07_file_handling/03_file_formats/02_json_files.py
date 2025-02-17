# working with JSON files in python
import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    """custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def write_json(filename: str, data: Any, indent: int = 4) -> bool:
    """write data to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, cls=DateTimeEncoder)
        return True
    except IOError as e:
        print(f"error writing JSON: {e}")
        return False

def read_json(filename: str) -> Optional[Any]:
    """read data from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except IOError as e:
        print(f"error reading JSON: {e}")
        return None

def update_json(filename: str, updates: Dict[str, Any]) -> bool:
    """update existing JSON file with new data."""
    try:
        # read existing data
        data = read_json(filename) or {}
        
        # update data
        if isinstance(data, dict):
            data.update(updates)
            return write_json(filename, data)
        return False
    except Exception as e:
        print(f"error updating JSON: {e}")
        return False

def merge_json_files(files: List[str], output_file: str) -> bool:
    """merge multiple JSON files into one."""
    try:
        merged_data = []
        for file in files:
            data = read_json(file)
            if data:
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    merged_data.append(data)
        return write_json(output_file, merged_data)
    except Exception as e:
        print(f"error merging JSON files: {e}")
        return False

def validate_json_schema(data: Any, schema: Dict[str, Any]) -> bool:
    """validate JSON data against a schema."""
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(f"validation error: {e}")
        return False

def format_json(data: Any) -> str:
    """format JSON data with proper indentation."""
    try:
        return json.dumps(data, indent=4, cls=DateTimeEncoder)
    except Exception as e:
        print(f"error formatting JSON: {e}")
        return str(data)

def search_json(data: Any, key: str) -> List[Any]:
    """recursively search for a key in JSON data."""
    results = []
    
    def _search(obj: Any, search_key: str):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == search_key:
                    results.append(v)
                _search(v, search_key)
        elif isinstance(obj, list):
            for item in obj:
                _search(item, search_key)
    
    _search(data, key)
    return results

# example usage
def main():
    """demonstrate JSON file operations."""
    # sample data
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "timestamp": datetime.now(),
        "hobbies": ["reading", "hiking", "photography"],
        "contact": {
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    }
    
    # write JSON file
    filename = "person.json"
    print("writing JSON file...")
    write_json(filename, data)
    
    # read JSON file
    print("\nreading JSON file:")
    loaded_data = read_json(filename)
    print(format_json(loaded_data))
    
    # update JSON
    updates = {
        "age": 31,
        "hobbies": ["reading", "hiking", "photography", "cooking"]
    }
    print("\nupdating JSON file...")
    update_json(filename, updates)
    
    # search in JSON
    print("\nsearching for 'email':")
    email_results = search_json(loaded_data, "email")
    print(f"found: {email_results}")
    
    # JSON schema validation
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"},
            "city": {"type": "string"},
            "hobbies": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["name", "age"]
    }
    
    print("\nvalidating against schema:")
    is_valid = validate_json_schema(loaded_data, schema)
    print(f"validation result: {is_valid}")
    
    # merge JSON files
    data2 = {
        "name": "Jane Doe",
        "age": 28,
        "city": "London"
    }
    
    filename2 = "person2.json"
    write_json(filename2, data2)
    
    merged_file = "merged.json"
    print("\nmerging JSON files...")
    merge_json_files([filename, filename2], merged_file)
    
    # cleanup
    for file in [filename, filename2, merged_file]:
        Path(file).unlink()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - reads a complex JSON configuration file
#    - validates it against a schema
#    - applies default values
#    - handles environment variables

# 2. create a program that:
#    - converts between different data formats
#    - supports JSON, YAML, and TOML
#    - preserves data types
#    - handles circular references

# 3. create a program that:
#    - implements a JSON patch system
#    - tracks changes to JSON documents
#    - allows rollback of changes
#    - generates diff reports 