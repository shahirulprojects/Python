# setup.py for package distribution
from setuptools import setup, find_packages

# read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="geometry-utils",
    version="1.0.0",
    author="your name",
    author_email="your.email@example.com",
    description="a package for geometric calculations and shape manipulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geometry-utils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.1",
            "black>=21.7b0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.1.2",
            "sphinx-rtd-theme>=0.5.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "geometry=geometry_package.cli:main",
        ],
    },
    package_data={
        "geometry_package": ["py.typed", "data/*.json"],
    },
    include_package_data=True,
    zip_safe=False,
) 