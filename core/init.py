"""
Elite Unicode Attack Framework - Core Module
"""

from .logger import init_logging, get_logger, log_banner
from .config import AttackConfig
from .utils import validate_url, validate_email, normalize_url

__all__ = [
    'init_logging',
    'get_logger',
    'log_banner',
    'AttackConfig',
    'validate_url',
    'validate_email',
    'normalize_url',
]

__version__ = '3.0.0'
__author__ = 'Elite Security Research Team'
__license__ = 'MIT'
