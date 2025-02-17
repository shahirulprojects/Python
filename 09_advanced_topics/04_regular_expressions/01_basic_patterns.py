# basic regular expression patterns in python
import re
from typing import List, Optional, Match, Pattern
import logging
from datetime import datetime

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_literal_matches(pattern: str, text: str) -> List[str]:
    """find literal matches in text."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_wildcards(pattern: str, text: str) -> List[str]:
    """find matches using wildcards."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_character_classes(pattern: str, text: str) -> List[str]:
    """find matches using character classes."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_quantifiers(pattern: str, text: str) -> List[str]:
    """find matches using quantifiers."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_anchors(pattern: str, text: str) -> List[str]:
    """find matches using anchors."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_groups(pattern: str, text: str) -> List[tuple]:
    """find matches using groups."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def validate_pattern(pattern: str) -> bool:
    """validate regular expression pattern."""
    try:
        re.compile(pattern)
        return True
    except re.error as e:
        logging.error(f"invalid pattern '{pattern}': {str(e)}")
        return False

def replace_with_pattern(
    pattern: str,
    replacement: str,
    text: str
) -> str:
    """replace matches using pattern."""
    result = re.sub(pattern, replacement, text)
    logging.info(f"replaced pattern '{pattern}' with '{replacement}'")
    return result

def split_with_pattern(pattern: str, text: str) -> List[str]:
    """split text using pattern."""
    parts = re.split(pattern, text)
    logging.info(f"split text into {len(parts)} parts using '{pattern}'")
    return parts

def main():
    """demonstrate regular expression patterns."""
    # 1. literal matches
    print("1. testing literal matches:")
    text = "The quick brown fox jumps over the lazy dog"
    pattern = "the"
    matches = find_literal_matches(pattern, text)
    print(f"matches: {matches}")
    
    # case-insensitive
    pattern = re.compile("the", re.IGNORECASE)
    matches = pattern.findall(text)
    print(f"case-insensitive matches: {matches}")
    
    # 2. wildcards
    print("\n2. testing wildcards:")
    text = "cat hat rat bat"
    pattern = ".at"  # any character followed by 'at'
    matches = find_with_wildcards(pattern, text)
    print(f"matches: {matches}")
    
    # 3. character classes
    print("\n3. testing character classes:")
    text = "The year was 1999"
    pattern = "[0-9]+"  # one or more digits
    matches = find_with_character_classes(pattern, text)
    print(f"matches: {matches}")
    
    # word characters
    pattern = r"\w+"  # one or more word characters
    matches = find_with_character_classes(pattern, text)
    print(f"word matches: {matches}")
    
    # 4. quantifiers
    print("\n4. testing quantifiers:")
    text = "The price is $19.99"
    pattern = r"\$\d+\.\d{2}"  # price format
    matches = find_with_quantifiers(pattern, text)
    print(f"matches: {matches}")
    
    # optional characters
    text = "color colour"
    pattern = "colou?r"  # optional 'u'
    matches = find_with_quantifiers(pattern, text)
    print(f"matches: {matches}")
    
    # 5. anchors
    print("\n5. testing anchors:")
    text = "The end is near\nThe end"
    pattern = r"^The"  # 'The' at start of line
    matches = find_with_anchors(pattern, text)
    print(f"matches: {matches}")
    
    pattern = r"end$"  # 'end' at end of line
    matches = find_with_anchors(pattern, text)
    print(f"matches: {matches}")
    
    # 6. groups
    print("\n6. testing groups:")
    text = "John Doe, Jane Doe"
    pattern = r"(\w+) (\w+)"  # first and last name
    matches = find_with_groups(pattern, text)
    print(f"matches: {matches}")
    
    # named groups
    pattern = r"(?P<first>\w+) (?P<last>\w+)"
    for match in re.finditer(pattern, text):
        print(f"named groups: {match.groupdict()}")
    
    # 7. pattern validation
    print("\n7. testing pattern validation:")
    patterns = [
        r"\d+",      # valid pattern
        r"[a-z",     # invalid pattern (unclosed bracket)
        r"(\w+))",   # invalid pattern (unmatched parenthesis)
    ]
    
    for pattern in patterns:
        is_valid = validate_pattern(pattern)
        print(f"pattern '{pattern}' is valid: {is_valid}")
    
    # 8. replacement
    print("\n8. testing replacement:")
    text = "John Doe"
    pattern = r"(\w+) (\w+)"
    replacement = r"\2, \1"  # swap first and last name
    result = replace_with_pattern(pattern, replacement, text)
    print(f"result: {result}")
    
    # 9. splitting
    print("\n9. testing splitting:")
    text = "apple,banana;orange,grape"
    pattern = r"[,;]"  # split on comma or semicolon
    parts = split_with_pattern(pattern, text)
    print(f"parts: {parts}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create patterns that:
#    - validate email addresses
#    - extract domain names
#    - handle international formats
#    - support comments

# 2. create patterns that:
#    - parse log files
#    - extract timestamps
#    - identify error messages
#    - group related entries

# 3. create patterns that:
#    - validate phone numbers
#    - handle different formats
#    - support extensions
#    - parse country codes 