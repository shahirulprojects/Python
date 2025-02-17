# Geometry Utils

A Python package for geometric calculations and shape manipulations.

## Features

- Basic geometric shapes (Circle, Rectangle, Square)
- Area and perimeter calculations
- Shape serialization and deserialization
- Utility functions for shape operations
- Comprehensive test suite
- Type hints and documentation

## Installation

You can install the package using pip:

```bash
pip install geometry-utils
```

Or install with extra features:

```bash
# Install with development dependencies
pip install geometry-utils[dev]

# Install with documentation dependencies
pip install geometry-utils[docs]
```

## Quick Start

```python
from geometry_package import Circle, Square, calculate_area

# Create shapes
circle = Circle(radius=5)
square = Square(side=4)

# Calculate areas
print(f"Circle area: {calculate_area(circle):.2f}")
print(f"Square area: {calculate_area(square):.2f}")

# Generate shape report
from geometry_package.utils import generate_shape_report

shapes = [circle, square]
print(generate_shape_report(shapes))
```

## Command Line Interface

The package includes a command-line interface for basic operations:

```bash
# Calculate circle area
geometry circle --radius 5

# Calculate square area
geometry square --side 4

# Generate shape report
geometry report shapes.json
```

## Development

To set up the development environment:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/geometry-utils.git
   cd geometry-utils
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Documentation

Documentation is available at [https://geometry-utils.readthedocs.io](https://geometry-utils.readthedocs.io).

To build the documentation locally:

```bash
cd docs
make html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure

```
geometry-utils/
├── geometry_package/
│   ├── __init__.py
│   ├── shapes.py
│   ├── utils.py
│   ├── constants.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_shapes.py
│   └── test_utils.py
├── docs/
│   ├── conf.py
│   └── index.rst
├── setup.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Changelog

### 1.0.0 (2024-03-XX)

- Initial release
- Basic shape implementations
- Utility functions
- CLI tool
- Documentation
