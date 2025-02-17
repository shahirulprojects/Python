# regular expression optimization in python
import re
from typing import List, Dict, Optional, Match, Pattern, Any, Tuple
import logging
import time
from datetime import datetime
import random
import string

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RegexBenchmark:
    """class for benchmarking regular expressions."""
    def __init__(self):
        self.results: Dict[str, float] = {}
    
    def benchmark(
        self,
        name: str,
        pattern: str,
        text: str,
        iterations: int = 1000
    ) -> float:
        """benchmark pattern performance."""
        # compile pattern
        try:
            regex = re.compile(pattern)
        except re.error as e:
            logging.error(f"invalid pattern '{pattern}': {str(e)}")
            return 0.0
        
        # measure time
        start = time.time()
        for _ in range(iterations):
            regex.findall(text)
        duration = time.time() - start
        
        # store result
        self.results[name] = duration
        logging.info(
            f"pattern '{name}' took {duration:.4f} seconds "
            f"for {iterations} iterations"
        )
        return duration
    
    def compare(self, patterns: Dict[str, str], text: str) -> Dict[str, float]:
        """compare multiple patterns."""
        for name, pattern in patterns.items():
            self.benchmark(name, pattern, text)
        return self.results

def optimize_pattern(pattern: str) -> Tuple[str, List[str]]:
    """optimize regular expression pattern."""
    optimizations = []
    
    # 1. use raw strings
    if not pattern.startswith('r'):
        pattern = 'r' + pattern
        optimizations.append("used raw string")
    
    # 2. use non-capturing groups
    if '(' in pattern and '?:' not in pattern:
        pattern = pattern.replace('(', '(?:')
        optimizations.append("used non-capturing groups")
    
    # 3. minimize backtracking
    if '.*' in pattern:
        pattern = pattern.replace('.*', '.*?')
        optimizations.append("minimized backtracking")
    
    # 4. use character classes
    if '[0-9]' in pattern:
        pattern = pattern.replace('[0-9]', r'\d')
        optimizations.append("used character class shorthand")
    
    # 5. anchor patterns when possible
    if not pattern.startswith('^') and not pattern.endswith('$'):
        if pattern.startswith(r'\b'):
            pattern = '^' + pattern[2:]
            optimizations.append("anchored pattern start")
        if pattern.endswith(r'\b'):
            pattern = pattern[:-2] + '$'
            optimizations.append("anchored pattern end")
    
    return pattern, optimizations

def generate_test_data(
    size: int,
    pattern: str = r'\w+'
) -> Tuple[str, List[str]]:
    """generate test data for regex testing."""
    # generate random text
    chars = string.ascii_letters + string.digits + string.punctuation
    text = ''.join(random.choice(chars) for _ in range(size))
    
    # find matches
    matches = re.findall(pattern, text)
    
    return text, matches

def analyze_pattern(pattern: str) -> Dict[str, Any]:
    """analyze regular expression pattern."""
    analysis = {
        'length': len(pattern),
        'groups': 0,
        'character_classes': 0,
        'quantifiers': 0,
        'anchors': 0,
        'backreferences': 0,
        'complexity': 0
    }
    
    # count groups
    analysis['groups'] = pattern.count('(')
    
    # count character classes
    analysis['character_classes'] = (
        pattern.count('[') +
        pattern.count(r'\d') +
        pattern.count(r'\w') +
        pattern.count(r'\s')
    )
    
    # count quantifiers
    analysis['quantifiers'] = (
        pattern.count('*') +
        pattern.count('+') +
        pattern.count('?') +
        pattern.count('{')
    )
    
    # count anchors
    analysis['anchors'] = (
        pattern.count('^') +
        pattern.count('$') +
        pattern.count(r'\b')
    )
    
    # count backreferences
    analysis['backreferences'] = len(re.findall(r'\\[1-9]', pattern))
    
    # calculate complexity
    analysis['complexity'] = (
        analysis['groups'] * 2 +
        analysis['character_classes'] +
        analysis['quantifiers'] * 3 +
        analysis['backreferences'] * 4
    )
    
    return analysis

def suggest_optimizations(pattern: str) -> List[str]:
    """suggest pattern optimizations."""
    suggestions = []
    
    # check for unanchored patterns
    if not pattern.startswith('^') and not pattern.endswith('$'):
        suggestions.append(
            "consider anchoring pattern with ^ and $ if matching whole string"
        )
    
    # check for greedy quantifiers
    if '.*' in pattern or '.+' in pattern:
        suggestions.append(
            "consider using non-greedy quantifiers .*? or .+? to minimize backtracking"
        )
    
    # check for unnecessary groups
    if '(' in pattern and '?:' not in pattern:
        suggestions.append(
            "use non-capturing groups (?:...) when capture groups aren't needed"
        )
    
    # check for character class optimization
    if '[0-9]' in pattern:
        suggestions.append("use \\d instead of [0-9] for digits")
    if '[a-zA-Z]' in pattern:
        suggestions.append("use \\w instead of [a-zA-Z] for word characters")
    
    # check for repeated character classes
    if r'\d+\d+' in pattern:
        suggestions.append("combine consecutive identical character classes")
    
    return suggestions

def main():
    """demonstrate regex optimization techniques."""
    # 1. benchmark different patterns
    print("1. testing pattern benchmarks:")
    benchmark = RegexBenchmark()
    
    patterns = {
        'simple': r'\w+',
        'complex': r'[a-zA-Z0-9_]+',
        'greedy': r'.*\d+',
        'non_greedy': r'.*?\d+'
    }
    
    text = 'a' * 1000 + '123'  # text to match
    results = benchmark.compare(patterns, text)
    
    for name, duration in results.items():
        print(f"{name}: {duration:.4f} seconds")
    
    # 2. pattern optimization
    print("\n2. testing pattern optimization:")
    pattern = '([0-9]+).*([a-zA-Z]+)'
    optimized, changes = optimize_pattern(pattern)
    print(f"original: {pattern}")
    print(f"optimized: {optimized}")
    print("changes:", changes)
    
    # 3. test data generation
    print("\n3. testing data generation:")
    text, matches = generate_test_data(100, r'\d+')
    print(f"generated text length: {len(text)}")
    print(f"found {len(matches)} matches")
    
    # 4. pattern analysis
    print("\n4. testing pattern analysis:")
    patterns = {
        'simple': r'\w+',
        'medium': r'^\d+[a-z]+$',
        'complex': r'(?:\w+\s*)+\d+\.\d+\s*(?:[A-Z][a-z]*\s*)*$'
    }
    
    for name, pattern in patterns.items():
        analysis = analyze_pattern(pattern)
        print(f"\n{name} pattern analysis:")
        for key, value in analysis.items():
            print(f"{key}: {value}")
    
    # 5. optimization suggestions
    print("\n5. testing optimization suggestions:")
    patterns = {
        'unanchored': r'hello.*world',
        'greedy': r'.*\d+.*',
        'capturing': r'(\w+)\s+(\d+)',
        'verbose': r'[0-9]+[a-zA-Z_]+[0-9]+'
    }
    
    for name, pattern in patterns.items():
        print(f"\n{name} pattern suggestions:")
        suggestions = suggest_optimizations(pattern)
        for suggestion in suggestions:
            print(f"- {suggestion}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create optimization tools that:
#    - analyze pattern complexity
#    - suggest improvements
#    - measure performance impact
#    - handle edge cases

# 2. create benchmarking tools that:
#    - compare pattern variations
#    - measure memory usage
#    - analyze bottlenecks
#    - generate reports

# 3. create analysis tools that:
#    - detect common mistakes
#    - suggest alternatives
#    - measure efficiency
#    - provide examples 