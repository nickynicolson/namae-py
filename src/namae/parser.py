import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import os

class NamePart(Enum):
    GIVEN = "given"
    FAMILY = "family"
    SUFFIX = "suffix"
    DROPPING_PARTICLE = "dropping_particle"
    NON_DROPPING_PARTICLE = "non_dropping_particle"
    PREFIX = "prefix"
    PARTICLE = "particle"
    APPENDIX = "appendix"

@dataclass
class Name:
    family: Optional[str] = None
    given: Optional[str] = None
    suffix: Optional[str] = None
    dropping_particle: Optional[str] = None
    non_dropping_particle: Optional[str] = None
    prefix: Optional[str] = None
    particle: Optional[str] = None
    appendix: Optional[str] = None
    
    def __str__(self) -> str:
        parts = []
        if self.given:
            parts.append(self.given)
        if self.family:
            parts.append(self.family)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)
    
    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            'family': self.family,
            'given': self.given,
            'suffix': self.suffix,
            'dropping_particle': self.dropping_particle,
            'non_dropping_particle': self.non_dropping_particle,
            'prefix': self.prefix,
            'particle': self.particle,
            'appendix': self.appendix
        }

class NamaeParser:
    def __init__(self):
        # Load particles from data file
        self.particles = self._load_particles()
        
        # Common suffixes and prefixes
        self.suffixes = {
            'jr', 'sr', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
            'junior', 'senior', 'phd', 'md', 'dds', 'dvm', 'esq'
        }
        
        self.prefixes = {
            'dr', 'prof', 'professor', 'rev', 'reverend', 'fr', 'father', 'brother',
            'sister', 'mr', 'mrs', 'ms', 'miss', 'madam', 'sir', 'lord', 'lady',
            'hon', 'honorable', 'rep', 'representative', 'sen', 'senator', 'gov', 'governor',
            'pres', 'president', 'vp', 'vice president', 'gen', 'general', 'adm', 'admiral',
            'capt', 'captain', 'col', 'colonel', 'lt', 'lieutenant', 'sgt', 'sergeant',
            'det', 'detective', 'insp', 'inspector'
        }
        
        # Compile regex patterns
        self._compile_patterns()
    
    def _load_particles(self):
        """Load particles from data file"""
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        particles_file = os.path.join(data_dir, 'particles.txt')
        
        particles = set()
        try:
            with open(particles_file, 'r', encoding='utf-8') as f:
                for line in f:
                    particle = line.strip()
                    if particle and not particle.startswith('#'):
                        particles.add(particle)
        except FileNotFoundError:
            # Fallback to default particles
            particles = {
                'de', 'del', 'della', 'der', 'des', 'du', 'van', 'von', 'vom', 'zu', 'zum', 'zur',
                'af', 'av', 'da', 'dal', 'dall', 'dalla', 'dei', 'del', 'della', 'dell', 'delle',
                'di', 'do', 'dos', 'la', 'le', 'los', 'ter', 'ten', 'op', "'t", 'al', 'bin', 'ibn'
            }
        
        return particles
    
    def _compile_patterns(self):
        # Pattern for suffixes (Jr., III, etc.)
        self.suffix_pattern = re.compile(
            r'\b(jr|sr|i{1,3}v?|vi{0,3}|ix|xi{0,3}|junior|senior|ph\.?d\.?|m\.?d\.?|'
            r'd\.?d\.?s\.?|d\.?v\.?m\.?|esq\.?)(\.?)$', 
            re.IGNORECASE
        )
        
        # Pattern for prefixes (Dr., Prof., etc.)
        self.prefix_pattern = re.compile(
            r'^(dr|prof|professor|rev|reverend|fr|father|brother|sister|'
            r'mr|mrs|ms|miss|madam|sir|lord|lady|hon|honorable|rep|representative|'
            r'sen|senator|gov|governor|pres|president|vp|vice president|gen|general|'
            r'adm|admiral|capt|captain|col|colonel|lt|lieutenant|sgt|sergeant|'
            r'det|detective|insp|inspector)\.?\s+',
            re.IGNORECASE
        )
        
        # Pattern for particles
        particle_regex = r'\b(' + '|'.join(re.escape(p) for p in self.particles) + r')\b'
        self.particle_pattern = re.compile(particle_regex, re.IGNORECASE)
    
    def parse(self, name_string: str) -> List[Name]:
        """Parse a name string into one or more Name objects"""
        if not name_string or not name_string.strip():
            return []
        
        # Handle multiple names separated by semicolons or 'and'
        names = self._split_names(name_string)
        results = []
        
        for name_part in names:
            name_part = name_part.strip()
            if not name_part:
                continue
                
            name_obj = Name()
            
            # Extract prefix if present
            prefix_match = self.prefix_pattern.match(name_part)
            if prefix_match:
                name_obj.prefix = prefix_match.group(1).lower()
                name_part = name_part[prefix_match.end():].strip()
            
            # Extract suffix if present
            suffix_match = self.suffix_pattern.search(name_part)
            if suffix_match:
                name_obj.suffix = suffix_match.group(1).lower()
                name_part = name_part[:suffix_match.start()].strip()
            
            # Handle different name formats
            if ',' in name_part:
                # Format: "Family, Given" or "Family, Given Middle"
                parts = [p.strip() for p in name_part.split(',', 1)]
                if len(parts) == 2:
                    name_obj.family = parts[0]
                    name_obj.given = parts[1]
            else:
                # Format: "Given Family" or "Given Middle Family"
                parts = name_part.split()
                if len(parts) == 1:
                    # Single name - assume family name
                    name_obj.family = parts[0]
                else:
                    # Multiple parts - last is family, rest are given
                    name_obj.family = parts[-1]
                    name_obj.given = ' '.join(parts[:-1])
            
            # Extract particles from family name
            if name_obj.family:
                name_obj.family, particles = self._extract_particles(name_obj.family)
                if particles:
                    name_obj.particle = ' '.join(particles)
            
            results.append(name_obj)
        
        return results
    
    def _split_names(self, name_string: str) -> List[str]:
        """Split a string containing multiple names"""
        # Split by semicolons or 'and'
        names = re.split(r'[;]|\band\b', name_string, flags=re.IGNORECASE)
        return [name.strip() for name in names if name.strip()]
    
    def _extract_particles(self, name: str) -> tuple:
        """Extract particles from a name and return cleaned name and particles"""
        parts = name.split()
        particles = []
        cleaned_parts = []
        
        for part in parts:
            if self.particle_pattern.match(part.lower()):
                particles.append(part)
            else:
                cleaned_parts.append(part)
        
        return ' '.join(cleaned_parts), particles
    
    def parse_list(self, name_list: List[str]) -> List[List[Name]]:
        """Parse a list of name strings"""
        return [self.parse(name) for name in name_list]


# Convenience functions
def parse_name(name_string: str) -> List[Name]:
    """Parse a single name string"""
    return NamaeParser().parse(name_string)

def parse_names(name_list: List[str]) -> List[List[Name]]:
    """Parse a list of name strings"""
    return NamaeParser().parse_list(name_list)