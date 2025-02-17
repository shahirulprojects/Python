# secure module importing practices in python
import importlib
import sys
import os
from typing import Optional
import hashlib

class SecureModuleLoader:
    """demonstrates secure module loading practices
    
    this class shows how to:
    - validate module sources
    - implement allowlists
    - check module integrity
    - handle imports securely
    """
    
    def __init__(self):
        # allowlist of trusted modules
        self.trusted_modules = {
            'json', 'csv', 'datetime', 
            'math', 'random', 'collections'
        }
        
        # store module hashes for integrity checking
        self.module_hashes = {}
    
    def calculate_module_hash(self, module_path: str) -> Optional[str]:
        """calculates a hash of the module file for integrity checking
        
        args:
            module_path: path to the module file
            
        returns:
            sha256 hash of the file contents or None if file not found
        """
        try:
            with open(module_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except FileNotFoundError:
            print(f"warning: module file not found: {module_path}")
            return None
    
    def verify_module_integrity(self, module_name: str, module_path: str) -> bool:
        """verifies the integrity of a module before loading
        
        args:
            module_name: name of the module
            module_path: path to the module file
            
        returns:
            True if module integrity is verified, False otherwise
        """
        current_hash = self.calculate_module_hash(module_path)
        
        if module_name not in self.module_hashes:
            # first time seeing this module, store its hash
            self.module_hashes[module_name] = current_hash
            return True
        
        # verify against stored hash
        return current_hash == self.module_hashes[module_name]
    
    def secure_import(self, module_name: str) -> Optional[object]:
        """securely imports a module after performing security checks
        
        args:
            module_name: name of the module to import
            
        returns:
            imported module object or None if import fails security checks
        """
        # check if module is in allowlist
        if module_name not in self.trusted_modules:
            print(f"security error: module '{module_name}' not in trusted modules list")
            return None
        
        try:
            # find the module specification
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"error: module '{module_name}' not found")
                return None
            
            # verify module integrity if it's a file-based module
            if spec.origin and os.path.isfile(spec.origin):
                if not self.verify_module_integrity(module_name, spec.origin):
                    print(f"security error: module '{module_name}' failed integrity check")
                    return None
            
            # import the module
            return importlib.import_module(module_name)
            
        except ImportError as e:
            print(f"error importing module '{module_name}': {e}")
            return None
        except Exception as e:
            print(f"unexpected error importing module '{module_name}': {e}")
            return None

def main():
    # create secure loader instance
    loader = SecureModuleLoader()
    
    print("demonstrating secure module loading:")
    
    # try loading a trusted module
    print("\nattempting to load trusted module 'json':")
    json_module = loader.secure_import('json')
    if json_module:
        print("successfully loaded json module")
        # demonstrate usage
        data = {'message': 'secure import successful'}
        print(json_module.dumps(data))
    
    # try loading an untrusted module
    print("\nattempting to load untrusted module 'dangerous_module':")
    result = loader.secure_import('dangerous_module')
    if result is None:
        print("successfully blocked untrusted module import")

if __name__ == "__main__":
    main() 