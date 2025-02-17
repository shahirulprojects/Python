# advanced regular expression patterns in python
import re
from typing import List, Dict, Optional, Match, Pattern, Any
import logging
from datetime import datetime
import json

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_with_lookahead(pattern: str, text: str) -> List[str]:
    """find matches using positive lookahead."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_lookbehind(pattern: str, text: str) -> List[str]:
    """find matches using positive lookbehind."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_negative_lookaround(pattern: str, text: str) -> List[str]:
    """find matches using negative lookaround."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_conditional(pattern: str, text: str) -> List[str]:
    """find matches using conditional patterns."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_atomic_groups(pattern: str, text: str) -> List[str]:
    """find matches using atomic groups."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_backreferences(pattern: str, text: str) -> List[str]:
    """find matches using backreferences."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def find_with_recursion(pattern: str, text: str) -> List[str]:
    """find matches using recursion."""
    matches = re.findall(pattern, text)
    logging.info(f"found {len(matches)} matches for '{pattern}'")
    return matches

def validate_complex_pattern(
    pattern: str,
    text: str,
    flags: int = 0
) -> bool:
    """validate text against complex pattern."""
    try:
        regex = re.compile(pattern, flags)
        match = regex.match(text)
        return bool(match)
    except re.error as e:
        logging.error(f"invalid pattern '{pattern}': {str(e)}")
        return False

def extract_structured_data(pattern: str, text: str) -> List[Dict[str, str]]:
    """extract structured data using named groups."""
    result = []
    for match in re.finditer(pattern, text):
        result.append(match.groupdict())
    logging.info(f"extracted {len(result)} items")
    return result

def replace_with_callback(
    pattern: str,
    callback: callable,
    text: str
) -> str:
    """replace matches using callback function."""
    result = re.sub(pattern, callback, text)
    logging.info("performed replacement with callback")
    return result

def main():
    """demonstrate advanced regular expression patterns."""
    # 1. positive lookahead
    print("1. testing positive lookahead:")
    text = "John Doe, Jane Doe, Jim Smith"
    pattern = r"\w+(?= Doe)"  # names followed by 'Doe'
    matches = find_with_lookahead(pattern, text)
    print(f"matches: {matches}")
    
    # 2. positive lookbehind
    print("\n2. testing positive lookbehind:")
    text = "$100, €200, £300"
    pattern = r"(?<=\$)\d+"  # numbers after dollar sign
    matches = find_with_lookbehind(pattern, text)
    print(f"matches: {matches}")
    
    # 3. negative lookaround
    print("\n3. testing negative lookaround:")
    text = "apple orange apple123 orange456"
    pattern = r"\w+(?!\d)"  # words not followed by numbers
    matches = find_with_negative_lookaround(pattern, text)
    print(f"matches: {matches}")
    
    # 4. conditional patterns
    print("\n4. testing conditional patterns:")
    text = "color colour flavor flavour"
    pattern = r"flavo(u?)r"  # 'u' is optional
    matches = find_with_conditional(pattern, text)
    print(f"matches: {matches}")
    
    # 5. atomic groups
    print("\n5. testing atomic groups:")
    text = "aaa aaaa aaaaa"
    pattern = r"(?>a+)a"  # match 'a's followed by 'a'
    matches = find_with_atomic_groups(pattern, text)
    print(f"matches: {matches}")
    
    # 6. backreferences
    print("\n6. testing backreferences:")
    text = "<b>bold</b> <i>italic</i> <b>more bold</b>"
    pattern = r"<(\w+)>.*?</\1>"  # match HTML tags
    matches = find_with_backreferences(pattern, text)
    print(f"matches: {matches}")
    
    # 7. recursion
    print("\n7. testing recursion:")
    text = "((a+b)*c)"
    pattern = r"\((?:[^()]+|\([^()]*\))*\)"  # match nested parentheses
    matches = find_with_recursion(pattern, text)
    print(f"matches: {matches}")
    
    # 8. complex validation
    print("\n8. testing complex validation:")
    # validate email with specific domain
    email = "user@example.com"
    pattern = r"^[a-zA-Z0-9._%+-]+@example\.com$"
    is_valid = validate_complex_pattern(pattern, email)
    print(f"email is valid: {is_valid}")
    
    # 9. structured data extraction
    print("\n9. testing structured data extraction:")
    text = """
    Name: John Doe
    Age: 30
    Email: john@example.com
    
    Name: Jane Smith
    Age: 25
    Email: jane@example.com
    """
    pattern = r"""
        Name:\s+(?P<name>[\w\s]+)\n
        Age:\s+(?P<age>\d+)\n
        Email:\s+(?P<email>[\w@.]+)
    """
    data = extract_structured_data(pattern, text, re.VERBOSE)
    print(f"extracted data: {json.dumps(data, indent=2)}")
    
    # 10. replacement with callback
    print("\n10. testing replacement with callback:")
    text = "The price is $10.99"
    def price_converter(match: Match) -> str:
        """convert price to euros."""
        price = float(match.group(1))
        return f"€{price * 0.85:.2f}"
    
    pattern = r"\$(\d+\.\d{2})"
    result = replace_with_callback(pattern, price_converter, text)
    print(f"result: {result}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create advanced patterns that:
#    - parse nested XML/HTML
#    - handle comments
#    - extract attributes
#    - validate structure

# 2. create advanced patterns that:
#    - parse complex URLs
#    - extract query parameters
#    - handle special characters
#    - validate protocols

# 3. create advanced patterns that:
#    - parse code blocks
#    - handle nested structures
#    - extract functions
#    - validate syntax 