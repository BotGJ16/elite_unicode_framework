#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Configuration Management
"""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path


@dataclass
class AttackConfig:
    """Attack configuration"""
    
    # Target settings
    target_url: str
    target_email: str
    
    # Performance settings
    threads: int = 5
    delay: float = 1.0
    timeout: int = 30
    
    # Stealth settings
    stealth_mode: bool = False
    random_user_agents: bool = True
    proxy: Optional[str] = None
    
    # Variant generation settings
    max_variants: int = 100
    include_zero_width: bool = True
    include_homographs: bool = True
    include_punycode: bool = True
    
    # Output settings
    output_dir: Path = field(default_factory=lambda: Path("results"))
    generate_report: bool = True
    report_format: str = "html"  # html, json, csv
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.target_url or not self.target_email:
            return False
        
        if self.threads < 1 or self.threads > 50:
            return False
        
        if self.delay < 0:
            return False
        
        return True


# Default user agents
DEFAULT_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Success patterns for detection
SUCCESS_PATTERNS = [
    r'email.*sent',
    r'check.*email',
    r'reset.*link',
    r'password.*reset',
    r'verification.*email',
    r'recovery.*email',
]

# Failure patterns
FAILURE_PATTERNS = [
    r'user.*not.*found',
    r'email.*not.*found',
    r'invalid.*email',
    r'account.*not.*exist',
]

# Rate limit patterns
RATE_LIMIT_PATTERNS = [
    r'too.*many.*requests',
    r'rate.*limit',
    r'try.*again.*later',
]
