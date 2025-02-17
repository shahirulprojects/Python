# setup.py for math_utils.geometry.shapes package
from setuptools import setup, find_namespace_packages

setup(
    name="math-utils-geometry-shapes",
    version="1.0.0",
    packages=find_namespace_packages(include=["math_utils.*"]),
    namespace_packages=["math_utils", "math_utils.geometry"],
    install_requires=[
        "numpy>=1.21.0",
    ],
    author="your name",
    author_email="your.email@example.com",
    description="geometric shapes package in math_utils namespace",
    python_requires=">=3.7",
) 