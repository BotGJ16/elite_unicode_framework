#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Utility Functions
"""

import re
import time
from typing import List, Dict, Optional
from urllib.parse import urlparse, urljoin


def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def normalize_url(url: str) -> str:
    """Normalize URL (add https if missing)"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    parsed = urlparse(url)
    return parsed.netloc


def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_size(bytes_count: int) -> str:
    """Format bytes in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


class ProgressTracker:
    """Simple progress tracker"""
    
    def __init__(self, total: int, prefix: str = "Progress"):
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.start_time = time.time()
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current += increment
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        elapsed = time.time() - self.start_time
        
        print(f"\r{self.prefix}: {self.current}/{self.total} ({percentage:.1f}%) | Elapsed: {format_duration(elapsed)}", end='', flush=True)
    
    def finish(self):
        """Mark as complete"""
        print()  # New line


class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_call = 0
    
    def wait(self):
        """Wait if needed to respect rate limit"""
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()
