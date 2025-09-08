#!/usr/bin/env python3
"""
Basic usage example for namae-py library
"""

from namae import parse_name, parse_names

# Parse a single name
names = parse_name("Dr. John Michael Doe Jr.")
print("Single name parsing:")
for i, name in enumerate(names):
    print(f"  Name {i+1}: {name}")
    print(f"  Details: {name.to_dict()}")
    print()

# Parse multiple names
name_list = ["John Doe", "Jane Smith", "Dr. Robert Johnson PhD"]
parsed_names = parse_names(name_list)
print("Multiple names parsing:")
for i, names in enumerate(parsed_names):
    for j, name in enumerate(names):
        print(f"  Input {i+1}, Name {j+1}: {name}")
        print(f"  Details: {name.to_dict()}")
        print()

# Parse a string with multiple names
multi_name_string = "John Doe and Jane Smith PhD"
names = parse_name(multi_name_string)
print(f"Multi-name string '{multi_name_string}':")
for i, name in enumerate(names):
    print(f"  Name {i+1}: {name}")
    print(f"  Details: {name.to_dict()}")
    print()