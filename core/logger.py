#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Professional Logging System
Zero duplicate logs, clean output, production-ready
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Global state
_HANDLERS_INITIALIZED = False
_LOG_FILE = None
_LOGGER_CACHE = {}


class EliteFormatter(logging.Formatter):
    """Custom formatter with clean ANSI colors"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green  
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    ICONS = {
        'DEBUG': '🔍',
        'INFO': '✓',
        'WARNING': '⚠',
        'ERROR': '✗',
        'CRITICAL': '🔥'
    }
    
    def format(self, record):
        levelname = record.levelname
        
        # Add icon and color
        if levelname in self.COLORS:
            icon = self.ICONS.get(levelname, '')
            colored = f"{self.COLORS[levelname]}{icon} {levelname}{self.COLORS['RESET']}"
            record.levelname = colored
        
        formatted = super().format(record)
        record.levelname = levelname  # Reset for other handlers
        
        return formatted


def init_logging(log_dir: str = "logs", level: int = logging.INFO) -> Path:
    """
    Initialize logging system (call once at startup)
    
    Args:
        log_dir: Directory for log files
        level: Logging level
        
    Returns:
        Path to log file
    """
    global _HANDLERS_INITIALIZED, _LOG_FILE
    
    if _HANDLERS_INITIALIZED:
        return _LOG_FILE
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Generate timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    _LOG_FILE = log_path / f"elite_unicode_{timestamp}.log"
    
    # Configure root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    
    # File handler (detailed)
    fh = logging.FileHandler(_LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    
    # Console handler (clean)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(EliteFormatter('%(levelname)-10s | %(message)s'))
    
    root.addHandler(fh)
    root.addHandler(ch)
    
    # Suppress noisy libraries
    for lib in ['urllib3', 'requests', 'asyncio', 'aiohttp']:
        logging.getLogger(lib).setLevel(logging.WARNING)
    
    _HANDLERS_INITIALIZED = True
    return _LOG_FILE


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance (cached, no duplicates)
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    global _HANDLERS_INITIALIZED, _LOGGER_CACHE
    
    if not _HANDLERS_INITIALIZED:
        init_logging()
    
    # Normalize name
    if not name.startswith("Elite"):
        name = f"Elite.{name}"
    
    # Return cached logger
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]
    
    # Create new logger
    logger = logging.getLogger(name)
    logger.propagate = True
    logger.setLevel(logging.DEBUG)
    
    # Prevent handler addition
    logger.addHandler = lambda x: None
    
    _LOGGER_CACHE[name] = logger
    return logger


def log_banner():
    """Display elite tool banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║      🚀 ELITE UNICODE ATTACK FRAMEWORK v3.0                          ║
║                                                                        ║
║      Next-Generation Unicode Exploitation Tool                        ║
║      Built for Professional Bug Bounty Hunters                        ║
║                                                                        ║
║      Features:                                                         ║
║      • Advanced Unicode Homograph Generation                           ║
║      • OAuth Provider Exploitation                                     ║
║      • Zero-Width Character Injection                                  ║
║      • Database Collation Attacks                                      ║
║      • Professional Reporting                                          ║
║                                                                        ║
║      ⚠️  Authorized Testing Only                                      ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"""
    print(f"\033[36m{banner}\033[0m")


if __name__ == "__main__":
    init_logging()
    logger = get_logger("test")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
