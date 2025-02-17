# specialized dictionary types and implementations
# this file covers advanced dictionary types from collections module

# 1. defaultdict - dictionaries with default values
from collections import defaultdict

# creating a defaultdict that defaults to list
def demonstrate_defaultdict():
    """shows how defaultdict automatically handles missing keys"""
    # groups words by their first letter
    word_groups = defaultdict(list)
    
    words = ["apple", "banana", "avocado", "berry", "cherry"]
    
    for word in words:
        # no need to check if key exists
        word_groups[word[0]].append(word)
    
    # print groups
    for letter, words in word_groups.items():
        print(f"words starting with '{letter}': {words}")

# 2. ordereddict - dictionaries that remember insertion order
from collections import OrderedDict

def demonstrate_ordereddict():
    """shows how OrderedDict maintains insertion order"""
    # create ordered dictionary
    scores = OrderedDict()
    
    # add items in specific order
    scores['alice'] = 95
    scores['bob'] = 89
    scores['charlie'] = 92
    
    # items remain in insertion order
    print("scores in order of entry:")
    for name, score in scores.items():
        print(f"{name}: {score}")
    
    # moving an item to the end
    scores.move_to_end('bob')
    print("\nafter moving bob to end:")
    for name, score in scores.items():
        print(f"{name}: {score}")

# 3. counter - dictionary for counting items
from collections import Counter

def demonstrate_counter():
    """shows how Counter helps count occurrences"""
    # count characters in text
    text = "mississippi"
    char_counts = Counter(text)
    
    print("character counts:")
    for char, count in char_counts.items():
        print(f"'{char}': {count}")
    
    # find most common characters
    print("\nmost common characters:")
    for char, count in char_counts.most_common(2):
        print(f"'{char}' appears {count} times")

# 4. chainmap - combine multiple dictionaries
from collections import ChainMap

def demonstrate_chainmap():
    """shows how ChainMap combines multiple dictionaries"""
    # different levels of settings
    defaults = {'theme': 'dark', 'language': 'en', 'font_size': 12}
    user_settings = {'theme': 'light'}
    
    # combine settings with precedence
    settings = ChainMap(user_settings, defaults)
    
    print("effective settings:")
    for key, value in settings.items():
        print(f"{key}: {value}")
    
    # show where each setting comes from
    print("\nsetting sources:")
    print(f"theme from user settings: {settings['theme']}")
    print(f"language from defaults: {settings['language']}")

# 5. implementing a cache with timeout
import time

class TimedCache:
    """dictionary-like structure with automatic timeout"""
    
    def __init__(self, timeout_seconds):
        self._cache = {}
        self.timeout = timeout_seconds
    
    def __setitem__(self, key, value):
        """sets item with current timestamp"""
        self._cache[key] = (value, time.time())
    
    def __getitem__(self, key):
        """gets item if it hasn't expired"""
        if key not in self._cache:
            raise KeyError(key)
        
        value, timestamp = self._cache[key]
        if time.time() - timestamp > self.timeout:
            # remove expired item
            del self._cache[key]
            raise KeyError(f"key {key} has expired")
        
        return value
    
    def __contains__(self, key):
        """checks if key exists and hasn't expired"""
        try:
            self[key]
            return True
        except KeyError:
            return False

# 6. implementing a bidirectional dictionary
class BiDict:
    """
    bidirectional dictionary that allows lookup by key or value
    assumes values are unique
    """
    
    def __init__(self):
        self._forward = {}
        self._backward = {}
    
    def __setitem__(self, key, value):
        """sets mapping in both directions"""
        # remove any existing mappings
        if key in self._forward:
            del self._backward[self._forward[key]]
        if value in self._backward:
            del self._forward[self._backward[value]]
        
        # add new mappings
        self._forward[key] = value
        self._backward[value] = key
    
    def __getitem__(self, key):
        """gets forward mapping"""
        return self._forward[key]
    
    def get_key(self, value):
        """gets reverse mapping"""
        return self._backward[value]

# 7. practical examples

def demonstrate_timed_cache():
    """shows usage of TimedCache"""
    # create cache with 2 second timeout
    cache = TimedCache(2)
    
    # store some values
    cache['key1'] = 'value1'
    print("stored key1")
    
    # immediate access works
    print(f"immediate access: {cache['key1']}")
    
    # wait for timeout
    print("waiting for timeout...")
    time.sleep(3)
    
    # access after timeout
    try:
        print(cache['key1'])
    except KeyError:
        print("key1 has expired")

def demonstrate_bidict():
    """shows usage of BiDict"""
    # create mapping of countries to capitals
    capitals = BiDict()
    
    # add some mappings
    capitals['france'] = 'paris'
    capitals['japan'] = 'tokyo'
    capitals['italy'] = 'rome'
    
    # lookup in both directions
    print(f"capital of france: {capitals['france']}")
    print(f"country with capital tokyo: {capitals.get_key('tokyo')}")
    
    # update mapping
    capitals['italy'] = 'roma'    # changes both directions
    print(f"updated capital: {capitals['italy']}")
    print(f"country with capital roma: {capitals.get_key('roma')}")

# run demonstrations
if __name__ == "__main__":
    print("demonstrating defaultdict:")
    demonstrate_defaultdict()
    
    print("\ndemonstrating ordereddict:")
    demonstrate_ordereddict()
    
    print("\ndemonstrating counter:")
    demonstrate_counter()
    
    print("\ndemonstrating chainmap:")
    demonstrate_chainmap()
    
    print("\ndemonstrating timed cache:")
    demonstrate_timed_cache()
    
    print("\ndemonstrating bidirectional dictionary:")
    demonstrate_bidict() 