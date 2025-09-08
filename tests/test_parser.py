import unittest
from src.namae.parser import NamaeParser, Name

class TestNamaeParser(unittest.TestCase):
    def setUp(self):
        self.parser = NamaeParser()
    
    def test_basic_names(self):
        names = self.parser.parse("John Doe")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "John")
        self.assertEqual(names[0].family, "Doe")
        
        names = self.parser.parse("Doe, John")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "John")
        self.assertEqual(names[0].family, "Doe")
    
    def test_suffixes(self):
        names = self.parser.parse("John Doe Jr.")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "John")
        self.assertEqual(names[0].family, "Doe")
        self.assertEqual(names[0].suffix, "jr")
    
    def test_prefixes(self):
        names = self.parser.parse("Dr. John Doe")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "John")
        self.assertEqual(names[0].family, "Doe")
        self.assertEqual(names[0].prefix, "dr")
    
    def test_particles(self):
        names = self.parser.parse("Ludwig van Beethoven")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "Ludwig")
        self.assertEqual(names[0].family, "Beethoven")
        self.assertEqual(names[0].particle, "van")
    
    def test_multiple_names(self):
        names = self.parser.parse("John Doe and Jane Smith")
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0].given, "John")
        self.assertEqual(names[0].family, "Doe")
        self.assertEqual(names[1].given, "Jane")
        self.assertEqual(names[1].family, "Smith")
    
    def test_complex_name(self):
        names = self.parser.parse("Dr. John Michael Doe Jr.")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0].given, "John Michael")
        self.assertEqual(names[0].family, "Doe")
        self.assertEqual(names[0].prefix, "dr")
        self.assertEqual(names[0].suffix, "jr")

if __name__ == "__main__":
    unittest.main()