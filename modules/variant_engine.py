#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Advanced Variant Generator
Generates sophisticated Unicode email variants for testing
"""

from typing import List, Dict, Set
from dataclasses import dataclass
from core.logger import get_logger

logger = get_logger("VariantEngine")


@dataclass
class EmailVariant:
    """Email variant with metadata"""
    original: str
    variant: str
    technique: str
    unicode_points: List[int]
    visual_similarity: float  # 0.0 to 1.0


class VariantEngine:
    """Advanced email variant generation engine"""
    
    # Unicode homograph mappings
    HOMOGRAPHS = {
        'a': ['а', 'ā', 'ă', 'ą', 'ά', 'α', 'а'],  # Cyrillic, Greek, Latin variants
        'e': ['е', 'ē', 'ė', 'ę', 'έ', 'ε', 'е'],
        'i': ['і', 'ī', 'į', 'ί', 'ι', 'і'],
        'o': ['о', 'ō', 'ő', 'ό', 'ο', 'о'],
        'u': ['υ', 'ū', 'ų', 'ύ', 'υ'],
        'c': ['с', 'ć', 'č', 'ċ', 'с'],
        'p': ['р', 'ρ', 'р'],
        'x': ['х', 'χ', 'х'],
        'y': ['у', 'ý', 'ÿ', 'у'],
        's': ['ѕ', 'ś', 'š', 'ș', 'ѕ'],
        'n': ['ո', 'ñ', 'ń', 'ň'],
        'h': ['һ', 'ћ', 'һ'],
        'j': ['ј', 'ј'],
        'k': ['κ', 'ķ', 'ĸ'],
        'l': ['ӏ', 'ĺ', 'ļ', 'ľ'],
        'm': ['м', 'ṁ', 'м'],
        't': ['τ', 'ţ', 'ť'],
        'w': ['ω', 'ŵ', 'ẁ', 'ẃ'],
        'z': ['ζ', 'ź', 'ż', 'ž'],
        'A': ['Α', 'А', 'Ā', 'Ă', 'А'],
        'B': ['В', 'Β', 'В'],
        'C': ['С', 'Ϲ', 'С'],
        'E': ['Е', 'Ε', 'Ē', 'Е'],
        'H': ['Η', 'Н', 'Ң', 'Н'],
        'I': ['Ι', 'І', 'Ӏ', 'І'],
        'J': ['Ј', 'Ј'],
        'K': ['Κ', 'К', 'Ķ', 'К'],
        'M': ['М', 'Μ', 'М'],
        'N': ['Ν', 'Ν'],
        'O': ['Ο', 'О', 'Ō', 'О'],
        'P': ['Ρ', 'Р', 'Р'],
        'S': ['Ѕ', 'Ś', 'Ѕ'],
        'T': ['Τ', 'Т', 'Т'],
        'X': ['Χ', 'Х', 'Х'],
        'Y': ['Υ', 'Ү', 'Ӯ'],
        'Z': ['Ζ', 'Ź', 'Ż'],
    }
    
    # Zero-width characters
    ZERO_WIDTH_CHARS = [
        '\u200B',  # Zero Width Space
        '\u200C',  # Zero Width Non-Joiner
        '\u200D',  # Zero Width Joiner
        '\u2060',  # Word Joiner
        '\uFEFF',  # Zero Width No-Break Space
    ]
    
    def __init__(self):
        self.logger = logger
        self.generated_variants: Set[str] = set()
    
    def generate_all_variants(self, email: str, max_variants: int = 100) -> List[EmailVariant]:
        """
        Generate all types of variants
        
        Args:
            email: Original email address
            max_variants: Maximum variants to generate
            
        Returns:
            List of EmailVariant objects
        """
        self.generated_variants.clear()
        variants = []
        
        # Parse email
        if '@' not in email:
            self.logger.error(f"Invalid email format: {email}")
            return variants
        
        username, domain = email.split('@', 1)
        
        # Generate different variant types
        self.logger.info(f"Generating variants for: {email}")
        
        # 1. Homograph variants
        homograph_variants = self._generate_homograph_variants(username, domain)
        variants.extend(homograph_variants[:max_variants//3])
        self.logger.info(f"Generated {len(homograph_variants)} homograph variants")
        
        # 2. Zero-width variants
        zw_variants = self._generate_zero_width_variants(username, domain)
        variants.extend(zw_variants[:max_variants//3])
        self.logger.info(f"Generated {len(zw_variants)} zero-width variants")
        
        # 3. Mixed variants
        mixed_variants = self._generate_mixed_variants(username, domain)
        variants.extend(mixed_variants[:max_variants//3])
        self.logger.info(f"Generated {len(mixed_variants)} mixed variants")
        
        # 4. Punycode variants
        punycode_variants = self._generate_punycode_variants(username, domain)
        variants.extend(punycode_variants)
        self.logger.info(f"Generated {len(punycode_variants)} punycode variants")
        
        self.logger.info(f"Total variants generated: {len(variants)}")
        return variants[:max_variants]
    
    def _generate_homograph_variants(self, username: str, domain: str) -> List[EmailVariant]:
        """Generate homograph character substitution variants"""
        variants = []
        
        for i, char in enumerate(username):
            if char.lower() in self.HOMOGRAPHS:
                for homograph in self.HOMOGRAPHS[char.lower()]:
                    if char.isupper():
                        homograph = homograph.upper() if homograph.upper() in self.HOMOGRAPHS else homograph
                    
                    variant_username = username[:i] + homograph + username[i+1:]
                    variant_email = f"{variant_username}@{domain}"
                    
                    if variant_email not in self.generated_variants:
                        self.generated_variants.add(variant_email)
                        variants.append(EmailVariant(
                            original=f"{username}@{domain}",
                            variant=variant_email,
                            technique="homograph",
                            unicode_points=[ord(homograph)],
                            visual_similarity=0.95
                        ))
        
        return variants
    
    def _generate_zero_width_variants(self, username: str, domain: str) -> List[EmailVariant]:
        """Generate zero-width character injection variants"""
        variants = []
        original_email = f"{username}@{domain}"
        
        # Insert zero-width chars at different positions
        for i in range(len(username)):
            for zw_char in self.ZERO_WIDTH_CHARS:
                variant_username = username[:i] + zw_char + username[i:]
                variant_email = f"{variant_username}@{domain}"
                
                if variant_email not in self.generated_variants:
                    self.generated_variants.add(variant_email)
                    variants.append(EmailVariant(
                        original=original_email,
                        variant=variant_email,
                        technique="zero_width",
                        unicode_points=[ord(zw_char)],
                        visual_similarity=1.0  # Invisible
                    ))
        
        return variants
    
    def _generate_mixed_variants(self, username: str, domain: str) -> List[EmailVariant]:
        """Generate mixed technique variants"""
        variants = []
        original_email = f"{username}@{domain}"
        
        # Combine homograph + zero-width
        for i, char in enumerate(username[:3]):  # Limit to first 3 chars
            if char.lower() in self.HOMOGRAPHS:
                homograph = self.HOMOGRAPHS[char.lower()][0]
                for zw_char in self.ZERO_WIDTH_CHARS[:2]:  # Limit zero-width
                    variant_username = username[:i] + homograph + zw_char + username[i+1:]
                    variant_email = f"{variant_username}@{domain}"
                    
                    if variant_email not in self.generated_variants:
                        self.generated_variants.add(variant_email)
                        variants.append(EmailVariant(
                            original=original_email,
                            variant=variant_email,
                            technique="mixed",
                            unicode_points=[ord(homograph), ord(zw_char)],
                            visual_similarity=0.90
                        ))
        
        return variants
    
    def _generate_punycode_variants(self, username: str, domain: str) -> List[EmailVariant]:
        """Generate punycode domain variants"""
        variants = []
        original_email = f"{username}@{domain}"
        
        # Apply homographs to domain
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            subdomain = domain_parts[0]
            
            for i, char in enumerate(subdomain[:3]):
                if char.lower() in self.HOMOGRAPHS:
                    homograph = self.HOMOGRAPHS[char.lower()][0]
                    variant_subdomain = subdomain[:i] + homograph + subdomain[i+1:]
                    variant_domain = '.'.join([variant_subdomain] + domain_parts[1:])
                    
                    # Encode to punycode
                    try:
                        punycode_domain = variant_domain.encode('idna').decode('ascii')
                        variant_email = f"{username}@{punycode_domain}"
                        
                        if variant_email not in self.generated_variants:
                            self.generated_variants.add(variant_email)
                            variants.append(EmailVariant(
                                original=original_email,
                                variant=variant_email,
                                technique="punycode",
                                unicode_points=[ord(homograph)],
                                visual_similarity=0.85
                            ))
                    except Exception as e:
                        self.logger.debug(f"Punycode encoding failed: {e}")
        
        return variants
    
    def get_variant_stats(self, variants: List[EmailVariant]) -> Dict:
        """Get statistics about generated variants"""
        stats = {
            'total': len(variants),
            'by_technique': {},
            'avg_similarity': 0.0,
            'unique_unicode_points': set()
        }
        
        for variant in variants:
            # Count by technique
            stats['by_technique'][variant.technique] = stats['by_technique'].get(variant.technique, 0) + 1
            
            # Track unicode points
            stats['unique_unicode_points'].update(variant.unicode_points)
            
            # Average similarity
            stats['avg_similarity'] += variant.visual_similarity
        
        if variants:
            stats['avg_similarity'] /= len(variants)
        
        stats['unique_unicode_points'] = len(stats['unique_unicode_points'])
        
        return stats
