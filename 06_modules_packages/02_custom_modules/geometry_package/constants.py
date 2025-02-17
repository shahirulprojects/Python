# constants for geometry package
"""
this module contains mathematical and physical constants used in geometric calculations.
"""

# mathematical constants
PI = 3.14159265359
TAU = 2 * PI  # full circle in radians
GOLDEN_RATIO = 1.61803398875
SQRT_2 = 1.41421356237
SQRT_3 = 1.73205080757

# conversion factors
DEGREES_TO_RADIANS = PI / 180
RADIANS_TO_DEGREES = 180 / PI

# common angles in radians
QUARTER_TURN = PI / 2
HALF_TURN = PI
THREE_QUARTER_TURN = 3 * PI / 2
FULL_TURN = TAU

# common angles in degrees
ANGLE_30 = 30
ANGLE_45 = 45
ANGLE_60 = 60
ANGLE_90 = 90
ANGLE_180 = 180
ANGLE_360 = 360

# dimensional constants
DIMENSIONS_2D = 2
DIMENSIONS_3D = 3

# tolerance for floating point comparisons
EPSILON = 1e-10

# dictionary of constants for easy access
CONSTANTS = {
    "pi": PI,
    "tau": TAU,
    "golden_ratio": GOLDEN_RATIO,
    "sqrt_2": SQRT_2,
    "sqrt_3": SQRT_3,
    "deg_to_rad": DEGREES_TO_RADIANS,
    "rad_to_deg": RADIANS_TO_DEGREES,
    "epsilon": EPSILON
} 