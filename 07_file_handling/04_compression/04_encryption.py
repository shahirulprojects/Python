# file encryption and security in python
# this module demonstrates how to securely handle sensitive file data

from cryptography.fernet import Fernet
from pathlib import Path
import base64
import os
import tempfile
from typing import Optional

class SecureFileHandler:
    """handles secure file operations with encryption
    
    this class demonstrates:
    - generating encryption keys
    - encrypting file contents
    - decrypting file contents
    - secure file deletion
    """
    
    def __init__(self, key_file: Optional[Path] = None):
        """initializes the secure file handler
        
        args:
            key_file: path to the encryption key file
                     if None, a new key will be generated
        """
        if key_file and key_file.exists():
            # load existing key
            self.key = self.load_key(key_file)
        else:
            # generate new key
            self.key = Fernet.generate_key()
            if key_file:
                self.save_key(key_file)
        
        # create the Fernet instance for encryption/decryption
        self.fernet = Fernet(self.key)
    
    def save_key(self, key_file: Path):
        """saves the encryption key to a file
        
        args:
            key_file: path where to save the key
        """
        key_file.write_bytes(self.key)
        # set restrictive permissions
        os.chmod(key_file, 0o600)  # only owner can read/write
    
    @staticmethod
    def load_key(key_file: Path) -> bytes:
        """loads an encryption key from a file
        
        args:
            key_file: path to the key file
            
        returns:
            the encryption key as bytes
        """
        return key_file.read_bytes()
    
    def encrypt_file(self, input_file: Path, output_file: Path):
        """encrypts a file
        
        args:
            input_file: path to the file to encrypt
            output_file: path where to save the encrypted file
        """
        # read the input file
        data = input_file.read_bytes()
        
        # encrypt the data
        encrypted_data = self.fernet.encrypt(data)
        
        # write the encrypted data
        output_file.write_bytes(encrypted_data)
        print(f"encrypted {input_file} to {output_file}")
    
    def decrypt_file(self, input_file: Path, output_file: Path):
        """decrypts a file
        
        args:
            input_file: path to the encrypted file
            output_file: path where to save the decrypted file
        """
        # read the encrypted file
        encrypted_data = input_file.read_bytes()
        
        # decrypt the data
        decrypted_data = self.fernet.decrypt(encrypted_data)
        
        # write the decrypted data
        output_file.write_bytes(decrypted_data)
        print(f"decrypted {input_file} to {output_file}")
    
    @staticmethod
    def secure_delete(file_path: Path):
        """securely deletes a file by overwriting its contents
        
        args:
            file_path: path to the file to delete
        """
        if not file_path.exists():
            return
        
        # get file size
        file_size = file_path.stat().st_size
        
        # overwrite file contents multiple times
        for _ in range(3):  # DoD standard suggests 3 passes
            with open(file_path, 'wb') as f:
                # write random data
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
        # finally delete the file
        file_path.unlink()
        print(f"securely deleted {file_path}")

def demonstrate_file_encryption():
    """shows how to use the secure file handler
    
    demonstrates:
    - key generation and management
    - file encryption and decryption
    - secure file handling
    """
    # create temporary directory for our demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # create paths for our files
        key_file = temp_path / 'encryption.key'
        original_file = temp_path / 'secret.txt'
        encrypted_file = temp_path / 'secret.encrypted'
        decrypted_file = temp_path / 'secret.decrypted'
        
        # create a test file with sensitive data
        original_file.write_text("this is sensitive information that needs to be protected")
        
        print("file encryption demonstration:")
        print(f"created test file: {original_file}")
        
        # create secure file handler
        handler = SecureFileHandler(key_file)
        
        # encrypt the file
        print("\nencrypting file...")
        handler.encrypt_file(original_file, encrypted_file)
        
        # show encrypted content (will be unreadable)
        print("\nencrypted content (base64):")
        print(base64.b64encode(encrypted_file.read_bytes()).decode()[:50] + "...")
        
        # decrypt the file
        print("\ndecrypting file...")
        handler.decrypt_file(encrypted_file, decrypted_file)
        
        # verify decrypted content
        print("\nverifying decryption:")
        print(f"original content: {original_file.read_text()}")
        print(f"decrypted content: {decrypted_file.read_text()}")
        
        # secure deletion
        print("\ndemonstrating secure deletion:")
        handler.secure_delete(original_file)
        handler.secure_delete(encrypted_file)
        handler.secure_delete(decrypted_file)
        handler.secure_delete(key_file)

def main():
    """runs the file encryption demonstration"""
    print("python file encryption demonstration\n")
    demonstrate_file_encryption()

if __name__ == "__main__":
    main() 