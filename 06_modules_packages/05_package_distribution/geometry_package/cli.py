# command-line interface for geometry package
import argparse
import json
import sys
from typing import List, Dict, Any

from .shapes import Circle, Square, Rectangle
from .utils import (
    create_shape,
    serialize_shape,
    calculate_area,
    calculate_perimeter,
    generate_shape_report
)

def create_parser() -> argparse.ArgumentParser:
    """create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="geometry utilities command-line interface"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="available commands")
    
    # circle command
    circle_parser = subparsers.add_parser("circle", help="circle operations")
    circle_parser.add_argument("--radius", type=float, required=True, help="circle radius")
    
    # square command
    square_parser = subparsers.add_parser("square", help="square operations")
    square_parser.add_argument("--side", type=float, required=True, help="square side length")
    
    # rectangle command
    rect_parser = subparsers.add_parser("rectangle", help="rectangle operations")
    rect_parser.add_argument("--width", type=float, required=True, help="rectangle width")
    rect_parser.add_argument("--height", type=float, required=True, help="rectangle height")
    
    # report command
    report_parser = subparsers.add_parser("report", help="generate shape report")
    report_parser.add_argument("file", help="JSON file containing shape data")
    report_parser.add_argument("--output", help="output file for report")
    
    # export command
    export_parser = subparsers.add_parser("export", help="export shape to JSON")
    export_parser.add_argument("shape", choices=["circle", "square", "rectangle"], help="shape type")
    export_parser.add_argument("--params", required=True, help="shape parameters as JSON string")
    export_parser.add_argument("--output", help="output file for JSON")
    
    return parser

def handle_shape_command(shape_type: str, args: argparse.Namespace) -> None:
    """handle commands for individual shapes."""
    try:
        if shape_type == "circle":
            shape = Circle(args.radius)
        elif shape_type == "square":
            shape = Square(args.side)
        elif shape_type == "rectangle":
            shape = Rectangle(args.width, args.height)
        else:
            raise ValueError(f"unknown shape type: {shape_type}")
        
        print(f"\nShape: {shape}")
        print(f"Area: {calculate_area(shape):.2f}")
        print(f"Perimeter: {calculate_perimeter(shape):.2f}")
        
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_report_command(args: argparse.Namespace) -> None:
    """handle the report generation command."""
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        shapes = []
        for shape_data in data:
            shape_type = shape_data.pop("type").lower()
            shape = create_shape(shape_type, **shape_data)
            shapes.append(shape)
        
        report = generate_shape_report(shapes)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"report written to {args.output}")
        else:
            print(report)
            
    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_export_command(args: argparse.Namespace) -> None:
    """handle the shape export command."""
    try:
        params = json.loads(args.params)
        shape = create_shape(args.shape, **params)
        json_data = serialize_shape(shape)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_data)
            print(f"shape data written to {args.output}")
        else:
            print(json_data)
            
    except (json.JSONDecodeError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command in ["circle", "square", "rectangle"]:
        handle_shape_command(args.command, args)
    elif args.command == "report":
        handle_report_command(args)
    elif args.command == "export":
        handle_export_command(args)

if __name__ == "__main__":
    main() 