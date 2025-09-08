# Namae-py

A Python port of the Ruby [Namae](https://github.com/berkmancenter/namae) name parser gem.

## Installation

```bash
pip install namae-py
```

## Usage

```python
from namae import parse_name, parse_names

# Parse a single name
names = parse_name("Dr. John Michael Doe Jr.")
for name in names:
    print(f"Given: {name.given}")
    print(f"Family: {name.family}")
    print(f"Prefix: {name.prefix}")
    print(f"Suffix: {name.suffix}")

# Parse multiple names
name_list = ["John Doe", "Jane Smith", "Dr. Robert Johnson PhD"]
parsed_names = parse_names(name_list)

# Parse a string with multiple names
names = parse_name("John Doe and Jane Smith PhD")
for name in names:
    print(f"Given: {name.given}")
    print(f"Family: {name.family}")
    print(f"Prefix: {name.prefix}")
    print(f"Suffix: {name.suffix}")
```

## Features

- Parse names into components: given, family, prefix, suffix, particles
- Handle multiple name formats: "John Doe", "Doe, John"
- Support for name particles: van, von, de, etc.
- Support for prefixes: Dr., Prof., Mr., etc.
- Support for suffixes: Jr., III, PhD, etc.
- Handle multiple names in a single string

## License

AGPL-3.0 License - see LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Acknowledgements
This project is inspired by the Ruby Namae gem by the Berkman Klein Center for Internet & Society - [@berkmancenter](https://github.com/berkmancenter)(github) and [cyber.harvard.edu](http://cyber.harvard.edu/)(www).