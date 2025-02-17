# geometry package initialization
"""
this package provides utilities for geometric calculations and shape manipulations.
it demonstrates proper package structure and initialization.
"""

from .shapes import Circle, Square, Rectangle
from .utils import calculate_area, calculate_perimeter
from .constants import PI, GOLDEN_RATIO

__version__ = "1.0.0"
__author__ = "your name"
__all__ = [
    'Circle', 'Square', 'Rectangle',
    'calculate_area', 'calculate_perimeter',
    'PI', 'GOLDEN_RATIO'
]

# package initialization code
def initialize():
    """initialize the package with any necessary setup."""
    print(f"initializing geometry package v{__version__}")

# cleanup code
def cleanup():
    """cleanup resources when package is unloaded."""
    print("cleaning up geometry package resources") 