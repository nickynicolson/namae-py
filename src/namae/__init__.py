"""
Namae-py: A Python port of the Ruby Namae name parser gem.
Parse human names into their component parts.
"""

from .parser import Name, NamaeParser, parse_name, parse_names

__version__ = "0.1.0"
__all__ = ["Name", "NamaeParser", "parse_name", "parse_names"]