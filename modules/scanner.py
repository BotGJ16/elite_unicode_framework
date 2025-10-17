#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Advanced Vulnerability Scanner
Discovers endpoints and analyzes targets
"""

import asyncio
import aiohttp
import re
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from core.logger import get_logger

logger = get_logger("Scanner")


class VulnerabilityScanner:
    """Advanced vulnerability scanner for target reconnaissance"""
    
    # Common endpoints to check
    COMMON_ENDPOINTS = [
        '/forgot-password',
        '/password/reset',
        '/auth/forgot',
        '/account/password/reset',
        '/reset-password',
        '/user/password-reset',
        '/password_reset',
        '/resetpassword',
        '/forgot_password',
        '/recover-password',
        '/password/recover',
        '/api/auth/forgot-password',
        '/api/password/reset',
    ]
    
    # OAuth endpoints
    OAUTH_ENDPOINTS = [
        '/oauth/authorize',
        '/oauth2/authorize',
        '/auth/oauth',
        '/api/oauth',
        '/login/oauth',
        '/oauth/callback',
        '/auth/callback',
    ]
    
    def __init__(self, target_url: str):
        self.target_url = target_url.rstrip('/')
        self.domain = urlparse(target_url).netloc
        self.logger = logger
        self.discovered_endpoints: Set[str] = set()
        self.oauth_providers: Dict[str, List[str]] = {}
    
    async def scan_full(self) -> Dict:
        """
        Execute comprehensive vulnerability scan
        
        Returns:
            Dictionary with scan results
        """
        self.logger.info(f"Starting comprehensive scan on: {self.target_url}")
        
        results = {
            'target': self.target_url,
            'domain': self.domain,
            'forgot_password_endpoints': [],
            'oauth_providers': {},
            'forms_found': [],
            'technology_stack': {},
            'security_headers': {},
        }
        
        # Scan for endpoints
        self.logger.info("Scanning for password reset endpoints...")
        results['forgot_password_endpoints'] = await self._scan_forgot_password_endpoints()
        
        # Scan for OAuth
        self.logger.info("Scanning for OAuth providers...")
        results['oauth_providers'] = await self._scan_oauth_providers()
        
        # Scan for forms
        self.logger.info("Analyzing forms...")
        results['forms_found'] = await self._scan_forms()
        
        # Fingerprint technology
        self.logger.info("Fingerprinting technology stack...")
        results['technology_stack'] = await self._fingerprint_technology()
        
        # Check security headers
        self.logger.info("Checking security headers...")
        results['security_headers'] = await self._check_security_headers()
        
        self.logger.info("Scan complete!")
        return results
    
    async def _scan_forgot_password_endpoints(self) -> List[str]:
        """Discover password reset endpoints"""
        discovered = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for endpoint in self.COMMON_ENDPOINTS:
                url = urljoin(self.target_url, endpoint)
                tasks.append(self._check_endpoint(session, url))
            
            results = await asyncio.gather(*tasks)
            discovered = [url for url, exists in results if exists]
        
        self.logger.info(f"Found {len(discovered)} password reset endpoints")
        return discovered
    
    async def _scan_oauth_providers(self) -> Dict[str, List[str]]:
        """Discover OAuth providers and endpoints"""
        providers = {}
        
        # Try to fetch main page
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for OAuth links/buttons
                    oauth_keywords = ['google', 'facebook', 'github', 'linkedin', 'twitter', 'microsoft', 'apple']
                    
                    for keyword in oauth_keywords:
                        # Search in links
                        links = soup.find_all('a', href=re.compile(keyword, re.I))
                        if links:
                            providers[keyword] = [link.get('href', '') for link in links]
                    
                    # Search for OAuth endpoints
                    for endpoint in self.OAUTH_ENDPOINTS:
                        url = urljoin(self.target_url, endpoint)
                        exists = await self._check_endpoint_exists(session, url)
                        if exists:
                            providers.setdefault('oauth_endpoints', []).append(url)
        
        except Exception as e:
            self.logger.debug(f"OAuth scan error: {e}")
        
        self.logger.info(f"Found {len(providers)} OAuth provider types")
        return providers
    
    async def _scan_forms(self) -> List[Dict]:
        """Scan for forms on the target"""
        forms = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    for form in soup.find_all('form'):
                        form_data = {
                            'action': form.get('action', ''),
                            'method': form.get('method', 'get').upper(),
                            'inputs': []
                        }
                        
                        # Get all inputs
                        for input_tag in form.find_all('input'):
                            form_data['inputs'].append({
                                'name': input_tag.get('name', ''),
                                'type': input_tag.get('type', 'text'),
                            })
                        
                        forms.append(form_data)
        
        except Exception as e:
            self.logger.debug(f"Form scan error: {e}")
        
        self.logger.info(f"Found {len(forms)} forms")
        return forms
    
    async def _fingerprint_technology(self) -> Dict:
        """Fingerprint technology stack"""
        tech_stack = {
            'server': 'Unknown',
            'framework': 'Unknown',
            'cms': 'Unknown',
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    headers = response.headers
                    html = await response.text()
                    
                    # Server detection
                    if 'Server' in headers:
                        tech_stack['server'] = headers['Server']
                    
                    # Framework detection (simplified)
                    if 'X-Powered-By' in headers:
                        tech_stack['framework'] = headers['X-Powered-By']
                    
                    # CMS detection (basic)
                    if 'wp-content' in html:
                        tech_stack['cms'] = 'WordPress'
                    elif 'Joomla' in html:
                        tech_stack['cms'] = 'Joomla'
                    elif 'Drupal' in html:
                        tech_stack['cms'] = 'Drupal'
        
        except Exception as e:
            self.logger.debug(f"Fingerprinting error: {e}")
        
        return tech_stack
    
    async def _check_security_headers(self) -> Dict:
        """Check for security headers"""
        security_headers = {
            'X-Frame-Options': False,
            'X-Content-Type-Options': False,
            'Strict-Transport-Security': False,
            'Content-Security-Policy': False,
            'X-XSS-Protection': False,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    headers = response.headers
                    
                    for header in security_headers.keys():
                        if header in headers:
                            security_headers[header] = True
        
        except Exception as e:
            self.logger.debug(f"Security header check error: {e}")
        
        return security_headers
    
    async def _check_endpoint(self, session: aiohttp.ClientSession, url: str) -> tuple:
        """Check if endpoint exists"""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5), allow_redirects=False) as response:
                # Consider 200, 301, 302 as valid
                if response.status in [200, 301, 302]:
                    return (url, True)
        except:
            pass
        
        return (url, False)
    
    async def _check_endpoint_exists(self, session: aiohttp.ClientSession, url: str) -> bool:
        """Check if endpoint exists (simple boolean)"""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5), allow_redirects=False) as response:
                return response.status in [200, 301, 302]
        except:
            return False
