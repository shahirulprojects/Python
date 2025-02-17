# file compression and archiving in python
import zipfile
import tarfile
import gzip
import bz2
import lzma
from pathlib import Path
from typing import List, Optional, Union, BinaryIO
import os
import shutil

def compress_file_zip(source: str, output: str, compression: int = zipfile.ZIP_DEFLATED) -> bool:
    """compress a file using ZIP format."""
    try:
        with zipfile.ZipFile(output, 'w', compression=compression) as zf:
            zf.write(source, Path(source).name)
        return True
    except Exception as e:
        print(f"error compressing file: {e}")
        return False

def extract_zip(zip_file: str, extract_path: str = ".") -> bool:
    """extract contents of a ZIP file."""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(extract_path)
        return True
    except Exception as e:
        print(f"error extracting ZIP: {e}")
        return False

def create_zip_archive(files: List[str], output: str, compression: int = zipfile.ZIP_DEFLATED) -> bool:
    """create ZIP archive containing multiple files."""
    try:
        with zipfile.ZipFile(output, 'w', compression=compression) as zf:
            for file in files:
                if os.path.isfile(file):
                    zf.write(file, Path(file).name)
                elif os.path.isdir(file):
                    for root, _, filenames in os.walk(file):
                        for filename in filenames:
                            file_path = os.path.join(root, filename)
                            arcname = os.path.relpath(file_path, os.path.dirname(file))
                            zf.write(file_path, arcname)
        return True
    except Exception as e:
        print(f"error creating ZIP archive: {e}")
        return False

def compress_file_gzip(source: str, output: Optional[str] = None) -> bool:
    """compress a file using gzip."""
    try:
        output = output or f"{source}.gz"
        with open(source, 'rb') as f_in:
            with gzip.open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return True
    except Exception as e:
        print(f"error compressing with gzip: {e}")
        return False

def decompress_gzip(source: str, output: Optional[str] = None) -> bool:
    """decompress a gzip file."""
    try:
        output = output or source.removesuffix('.gz')
        with gzip.open(source, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return True
    except Exception as e:
        print(f"error decompressing gzip: {e}")
        return False

def create_tar_archive(files: List[str], output: str, compression: Optional[str] = None) -> bool:
    """create TAR archive with optional compression."""
    try:
        mode = 'w:' + (compression or '')
        with tarfile.open(output, mode) as tar:
            for file in files:
                tar.add(file, arcname=Path(file).name)
        return True
    except Exception as e:
        print(f"error creating TAR archive: {e}")
        return False

def extract_tar(tar_file: str, extract_path: str = ".") -> bool:
    """extract contents of a TAR archive."""
    try:
        with tarfile.open(tar_file, 'r:*') as tar:
            tar.extractall(extract_path)
        return True
    except Exception as e:
        print(f"error extracting TAR: {e}")
        return False

class CompressedFileHandler:
    """context manager for handling compressed files."""
    
    def __init__(self, filename: str, mode: str = 'rb'):
        self.filename = filename
        self.mode = mode
        self.file: Optional[BinaryIO] = None
        
        # determine compression type from extension
        if filename.endswith('.gz'):
            self.open_func = gzip.open
        elif filename.endswith('.bz2'):
            self.open_func = bz2.open
        elif filename.endswith('.xz'):
            self.open_func = lzma.open
        else:
            raise ValueError("unsupported compression format")
    
    def __enter__(self) -> BinaryIO:
        self.file = self.open_func(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

def compare_compression_methods(filename: str) -> dict:
    """compare different compression methods."""
    results = {}
    original_size = os.path.getsize(filename)
    results['original'] = original_size
    
    # ZIP compression
    zip_file = f"{filename}.zip"
    compress_file_zip(filename, zip_file)
    results['zip'] = os.path.getsize(zip_file)
    os.remove(zip_file)
    
    # GZIP compression
    gzip_file = f"{filename}.gz"
    compress_file_gzip(filename, gzip_file)
    results['gzip'] = os.path.getsize(gzip_file)
    os.remove(gzip_file)
    
    # BZIP2 compression
    bz2_file = f"{filename}.bz2"
    with open(filename, 'rb') as f_in:
        with bz2.open(bz2_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    results['bzip2'] = os.path.getsize(bz2_file)
    os.remove(bz2_file)
    
    # LZMA compression
    xz_file = f"{filename}.xz"
    with open(filename, 'rb') as f_in:
        with lzma.open(xz_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    results['lzma'] = os.path.getsize(xz_file)
    os.remove(xz_file)
    
    return results

# example usage
def main():
    """demonstrate compression and archiving operations."""
    # create sample files
    text_file = "sample.txt"
    with open(text_file, 'w') as f:
        f.write("This is a sample text file.\n" * 100)
    
    binary_file = "sample.bin"
    with open(binary_file, 'wb') as f:
        f.write(os.urandom(1000))
    
    # ZIP operations
    print("ZIP operations:")
    zip_file = "archive.zip"
    create_zip_archive([text_file, binary_file], zip_file)
    print(f"created ZIP archive: {zip_file}")
    
    extract_dir = "extracted"
    os.makedirs(extract_dir, exist_ok=True)
    extract_zip(zip_file, extract_dir)
    print(f"extracted to: {extract_dir}")
    
    # GZIP operations
    print("\nGZIP operations:")
    gzip_file = "sample.txt.gz"
    compress_file_gzip(text_file, gzip_file)
    print(f"compressed with GZIP: {gzip_file}")
    
    # TAR operations
    print("\nTAR operations:")
    tar_file = "archive.tar.gz"
    create_tar_archive([text_file, binary_file], tar_file, compression="gz")
    print(f"created TAR archive: {tar_file}")
    
    # compression comparison
    print("\ncompression comparison:")
    results = compare_compression_methods(text_file)
    for method, size in results.items():
        ratio = (1 - size/results['original']) * 100
        print(f"{method}: {size} bytes ({ratio:.1f}% reduction)")
    
    # using compressed file handler
    print("\nusing compressed file handler:")
    with CompressedFileHandler(gzip_file, 'rb') as f:
        content = f.read()
        print(f"read {len(content)} bytes from compressed file")
    
    # cleanup
    for file in [text_file, binary_file, zip_file, gzip_file, tar_file]:
        os.remove(file)
    shutil.rmtree(extract_dir)

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - implements incremental backup
#    - compresses changed files only
#    - maintains version history
#    - supports different compression methods

# 2. create a program that:
#    - processes large files in chunks
#    - applies custom compression
#    - shows progress information
#    - validates compressed data

# 3. create a program that:
#    - manages a compressed file database
#    - indexes file contents
#    - supports searching compressed files
#    - handles multiple compression formats 