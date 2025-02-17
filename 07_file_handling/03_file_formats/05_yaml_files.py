# working with YAML files in python
import yaml
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, date

class CustomYAMLDumper(yaml.Dumper):
    """custom YAML dumper with additional type support."""
    
    def represent_datetime(self, data):
        return self.represent_scalar('tag:yaml.org,2002:timestamp', data.isoformat())
    
    def represent_date(self, data):
        return self.represent_scalar('tag:yaml.org,2002:timestamp', data.isoformat())

# register custom representers
CustomYAMLDumper.add_representer(datetime, CustomYAMLDumper.represent_datetime)
CustomYAMLDumper.add_representer(date, CustomYAMLDumper.represent_date)

def write_yaml(filename: str, data: Any, flow_style: bool = False) -> bool:
    """write data to YAML file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, Dumper=CustomYAMLDumper, 
                     default_flow_style=flow_style,
                     allow_unicode=True,
                     sort_keys=False)
        return True
    except Exception as e:
        print(f"error writing YAML: {e}")
        return False

def read_yaml(filename: str) -> Optional[Any]:
    """read data from YAML file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"error reading YAML: {e}")
        return None

def update_yaml(filename: str, updates: Dict[str, Any], create: bool = True) -> bool:
    """update existing YAML file with new data."""
    try:
        data = read_yaml(filename) if Path(filename).exists() else {}
        if data is None and not create:
            return False
        
        data = data or {}
        _deep_update(data, updates)
        return write_yaml(filename, data)
    except Exception as e:
        print(f"error updating YAML: {e}")
        return False

def _deep_update(target: Dict[str, Any], source: Dict[str, Any]):
    """recursively update nested dictionary."""
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            _deep_update(target[key], value)
        else:
            target[key] = value

def merge_yaml_files(files: List[str], output_file: str) -> bool:
    """merge multiple YAML files into one."""
    try:
        merged_data = {}
        for file in files:
            data = read_yaml(file)
            if isinstance(data, dict):
                _deep_update(merged_data, data)
            elif isinstance(data, list):
                merged_data.setdefault('items', []).extend(data)
        
        return write_yaml(output_file, merged_data)
    except Exception as e:
        print(f"error merging YAML files: {e}")
        return False

def validate_yaml_schema(data: Any, schema: Dict[str, Any]) -> bool:
    """validate YAML data against schema."""
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(f"validation error: {e}")
        return False

def yaml_to_json(yaml_file: str, json_file: str) -> bool:
    """convert YAML file to JSON."""
    try:
        import json
        data = read_yaml(yaml_file)
        if data is not None:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        return False
    except Exception as e:
        print(f"error converting YAML to JSON: {e}")
        return False

def json_to_yaml(json_file: str, yaml_file: str) -> bool:
    """convert JSON file to YAML."""
    try:
        import json
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return write_yaml(yaml_file, data)
    except Exception as e:
        print(f"error converting JSON to YAML: {e}")
        return False

# example usage
def main():
    """demonstrate YAML file operations."""
    # sample data
    data = {
        "config": {
            "app_name": "My Application",
            "version": "1.0.0",
            "created_at": datetime.now(),
            "settings": {
                "debug": True,
                "max_connections": 100,
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "credentials": {
                        "username": "admin",
                        "password": "secret"
                    }
                }
            },
            "features": ["auth", "api", "admin"],
            "environments": [
                {
                    "name": "development",
                    "url": "http://localhost:8000"
                },
                {
                    "name": "production",
                    "url": "https://example.com"
                }
            ]
        }
    }
    
    # write YAML file
    filename = "config.yaml"
    print("writing YAML file...")
    write_yaml(filename, data)
    
    # read YAML file
    print("\nreading YAML file:")
    loaded_data = read_yaml(filename)
    print(f"loaded data: {loaded_data}")
    
    # update YAML
    updates = {
        "config": {
            "version": "1.0.1",
            "settings": {
                "max_connections": 200
            }
        }
    }
    
    print("\nupdating YAML file...")
    update_yaml(filename, updates)
    
    # YAML schema validation
    schema = {
        "type": "object",
        "properties": {
            "config": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string"},
                    "version": {"type": "string"},
                    "settings": {"type": "object"}
                },
                "required": ["app_name", "version"]
            }
        }
    }
    
    print("\nvalidating against schema:")
    is_valid = validate_yaml_schema(loaded_data, schema)
    print(f"validation result: {is_valid}")
    
    # convert to JSON and back
    json_file = "config.json"
    yaml_file = "config_converted.yaml"
    
    print("\nconverting YAML to JSON...")
    yaml_to_json(filename, json_file)
    
    print("converting JSON back to YAML...")
    json_to_yaml(json_file, yaml_file)
    
    # merge YAML files
    data2 = {
        "config": {
            "features": ["notifications"],
            "new_setting": "value"
        }
    }
    
    filename2 = "config2.yaml"
    write_yaml(filename2, data2)
    
    merged_file = "merged_config.yaml"
    print("\nmerging YAML files...")
    merge_yaml_files([filename, filename2], merged_file)
    
    # cleanup
    for file in [filename, filename2, merged_file, json_file, yaml_file]:
        Path(file).unlink()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - manages application configuration
#    - supports multiple environments
#    - handles sensitive data
#    - validates configuration schema

# 2. create a program that:
#    - generates documentation from YAML
#    - supports templates
#    - includes code examples
#    - produces formatted output

# 3. create a program that:
#    - implements a data migration tool
#    - converts between formats
#    - preserves data types
#    - handles complex structures 