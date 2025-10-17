#!/usr/bin/env python3
"""
Elite Unicode Attack Framework - Professional Report Generator
Generates beautiful HTML, JSON, and CSV reports
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from core.logger import get_logger

logger = get_logger("Reporter")


class Reporter:
    """Professional report generator"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.logger = logger
    
    def generate_html_report(self, results: Dict, filename: str = None) -> Path:
        """Generate professional HTML report"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # Calculate statistics
        stats = results.get('statistics', {})
        attack_results = results.get('attack_results', [])
        scan_results = results.get('scan_results', {})
        
        # Generate HTML
        html_content = self._generate_html_template(results, stats, attack_results, scan_results)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report generated: {filepath}")
        return filepath
    
    def generate_json_report(self, results: Dict, filename: str = None) -> Path:
        """Generate JSON report"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Write JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON report generated: {filepath}")
        return filepath
    
    def generate_csv_report(self, attack_results: List[Dict], filename: str = None) -> Path:
        """Generate CSV report of attack results"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        if not attack_results:
            self.logger.warning("No attack results to export")
            return filepath
        
        # Write CSV
        fieldnames = list(attack_results[0].keys())
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(attack_results)
        
        self.logger.info(f"CSV report generated: {filepath}")
        return filepath
    
    def _generate_html_template(self, results: Dict, stats: Dict, 
                                attack_results: List[Dict], scan_results: Dict) -> str:
        """Generate HTML template"""
        
        target = results.get('target', 'Unknown')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build successful attacks section
        successful_attacks = [r for r in attack_results if r.get('success', False)]
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elite Unicode Attack Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            font-size: 1em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .info-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        .info-box strong {{
            color: #667eea;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-top: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .success {{
            color: #28a745;
            font-weight: bold;
        }}
        
        .failure {{
            color: #dc3545;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-success {{
            background: #28a745;
            color: white;
        }}
        
        .badge-danger {{
            background: #dc3545;
            color: white;
        }}
        
        .badge-info {{
            background: #17a2b8;
            color: white;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Elite Unicode Attack Report</h1>
            <p class="subtitle">Professional Security Assessment</p>
            <p style="margin-top: 15px; font-size: 0.9em;">Generated: {timestamp}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="info-box">
                    <p><strong>Target:</strong> {target}</p>
                    <p><strong>Scan Date:</strong> {timestamp}</p>
                    <p><strong>Report Type:</strong> Unicode Exploitation Assessment</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Attacks</h3>
                        <div class="value">{stats.get('total_attacks', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Successful</h3>
                        <div class="value">{stats.get('successful', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Success Rate</h3>
                        <div class="value">{stats.get('success_rate', 0):.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>Unique Variants</h3>
                        <div class="value">{stats.get('unique_variants', 0)}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 Successful Attacks</h2>
                {self._generate_success_table_html(successful_attacks)}
            </div>
            
            <div class="section">
                <h2>🔍 Scan Results</h2>
                {self._generate_scan_results_html(scan_results)}
            </div>
            
            <div class="warning">
                <strong>⚠️ Legal Notice:</strong> This report is for authorized security testing only. 
                All testing was conducted with proper authorization. Unauthorized use is illegal.
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Elite Unicode Attack Framework v3.0</strong></p>
            <p>Professional Security Assessment Tool</p>
            <p style="margin-top: 10px; font-size: 0.85em;">© 2025 - For Authorized Testing Only</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_success_table_html(self, successful_attacks: List[Dict]) -> str:
        """Generate HTML table for successful attacks"""
        
        if not successful_attacks:
            return "<p>No successful attacks detected.</p>"
        
        rows = ""
        for attack in successful_attacks[:20]:  # Limit to top 20
            variant = attack.get('variant', 'N/A')
            technique = attack.get('technique', 'N/A')
            response_time = attack.get('response_time', 0)
            
            rows += f"""
            <tr>
                <td>{variant}</td>
                <td><span class="badge badge-info">{technique}</span></td>
                <td>{response_time:.2f}s</td>
                <td><span class="badge badge-success">Success</span></td>
            </tr>
            """
        
        return f"""
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Email Variant</th>
                        <th>Technique</th>
                        <th>Response Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_scan_results_html(self, scan_results: Dict) -> str:
        """Generate HTML for scan results"""
        
        endpoints = scan_results.get('forgot_password_endpoints', [])
        oauth = scan_results.get('oauth_providers', {})
        tech = scan_results.get('technology_stack', {})
        
        html = "<div class='info-box'>"
        html += f"<p><strong>Password Reset Endpoints Found:</strong> {len(endpoints)}</p>"
        html += f"<p><strong>OAuth Providers Detected:</strong> {len(oauth)}</p>"
        html += f"<p><strong>Server:</strong> {tech.get('server', 'Unknown')}</p>"
        html += f"<p><strong>Framework:</strong> {tech.get('framework', 'Unknown')}</p>"
        html += "</div>"
        
        if endpoints:
            html += "<h3>Discovered Endpoints:</h3><ul>"
            for ep in endpoints[:10]:
                html += f"<li>{ep}</li>"
            html += "</ul>"
        
        return html
