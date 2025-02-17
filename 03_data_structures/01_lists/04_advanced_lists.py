# advanced list operations and implementations
# this file covers advanced list concepts and custom list-like structures

# 1. memory views and array slicing
# understanding how lists work in memory
import sys

def demonstrate_list_memory():
    """shows how lists use memory"""
    # empty list starts small
    empty_list = []
    print(f"empty list size: {sys.getsizeof(empty_list)} bytes")
    
    # list grows as elements are added
    numbers = []
    for i in range(5):
        numbers.append(i)
        # shows how memory allocation grows
        print(f"list with {i+1} items: {sys.getsizeof(numbers)} bytes")

# 2. implementing a custom list-like structure
class SmartList:
    """a list-like structure with additional functionality"""
    
    def __init__(self, initial_data=None):
        # internal storage uses regular list
        self._data = list(initial_data) if initial_data else []
        # keeps track of access patterns
        self._access_count = {}
    
    def append(self, item):
        """adds an item to the list"""
        self._data.append(item)
    
    def __getitem__(self, index):
        """gets item at index and tracks access"""
        # record access for statistics
        self._access_count[index] = self._access_count.get(index, 0) + 1
        return self._data[index]
    
    def get_most_accessed(self):
        """returns the most frequently accessed index"""
        if not self._access_count:
            return None
        return max(self._access_count.items(), key=lambda x: x[1])[0]
    
    def __len__(self):
        """returns length of the list"""
        return len(self._data)
    
    def __str__(self):
        """string representation"""
        return str(self._data)

# 3. advanced sorting and custom comparators
from functools import cmp_to_key

class Task:
    def __init__(self, name, priority, duration):
        self.name = name
        self.priority = priority
        self.duration = duration

def compare_tasks(task1, task2):
    """
    custom comparison function for tasks
    
    args:
        task1 (Task): first task
        task2 (Task): second task
    
    returns:
        int: negative if task1 < task2, 0 if equal, positive if task1 > task2
    """
    # first compare by priority (higher priority comes first)
    if task1.priority != task2.priority:
        return task2.priority - task1.priority
    
    # if priorities are equal, shorter duration comes first
    return task1.duration - task2.duration

# 4. implementing a circular buffer
class CircularBuffer:
    """
    fixed-size circular buffer implementation
    useful for streaming data or sliding windows
    """
    
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.head = 0    # where we write next
        self.count = 0    # how many elements we have
    
    def append(self, item):
        """adds item to the buffer"""
        # write item at head position
        self.buffer[self.head] = item
        
        # move head to next position
        self.head = (self.head + 1) % self.size
        
        # update count of elements
        self.count = min(self.count + 1, self.size)
    
    def __getitem__(self, index):
        """gets item at relative position"""
        if not 0 <= index < self.count:
            raise IndexError("buffer index out of range")
        
        # calculate actual position
        pos = (self.head - self.count + index) % self.size
        return self.buffer[pos]
    
    def __len__(self):
        """returns number of items in buffer"""
        return self.count
    
    def __str__(self):
        """string representation of valid items"""
        items = []
        for i in range(self.count):
            items.append(str(self.__getitem__(i)))
        return "[" + ", ".join(items) + "]"

# 5. practical examples

def demonstrate_smart_list():
    """shows usage of SmartList"""
    # create a smart list with initial data
    numbers = SmartList([1, 2, 3, 4, 5])
    
    # access some elements multiple times
    for _ in range(3):
        print(numbers[0])    # access index 0 three times
    for _ in range(2):
        print(numbers[2])    # access index 2 twice
    
    # check access patterns
    most_accessed = numbers.get_most_accessed()
    print(f"most accessed index: {most_accessed}")

def demonstrate_task_sorting():
    """shows custom sorting with tasks"""
    tasks = [
        Task("write report", 2, 60),    # medium priority, long duration
        Task("fix bug", 3, 30),         # high priority, medium duration
        Task("check emails", 1, 15),    # low priority, short duration
        Task("emergency fix", 3, 10)    # high priority, short duration
    ]
    
    # sort tasks using custom comparator
    sorted_tasks = sorted(tasks, key=cmp_to_key(compare_tasks))
    
    # show sorted tasks
    for task in sorted_tasks:
        print(f"{task.name}: priority {task.priority}, duration {task.duration}")

def demonstrate_circular_buffer():
    """shows usage of CircularBuffer"""
    # create buffer for last 3 measurements
    buffer = CircularBuffer(3)
    
    # add some measurements
    temperatures = [22.5, 23.1, 23.8, 24.2, 23.9]
    
    for temp in temperatures:
        buffer.append(temp)
        print(f"buffer after adding {temp}: {buffer}")

# run demonstrations
if __name__ == "__main__":
    print("demonstrating list memory:")
    demonstrate_list_memory()
    
    print("\ndemonstrating smart list:")
    demonstrate_smart_list()
    
    print("\ndemonstrating task sorting:")
    demonstrate_task_sorting()
    
    print("\ndemonstrating circular buffer:")
    demonstrate_circular_buffer() 