"""
Report Generator Module
Creates HTML validation reports
"""

from datetime import datetime
import yaml


class ReportGenerator:
    """Generates HTML validation reports"""
    
    def generate(self, results, scenario_file, output_file):
        """
        Generate HTML report from validation results
        
        Args:
            results: List of validation results
            scenario_file: Path to scenario file (for metadata)
            output_file: Path to save HTML report
        """
        # Load scenario metadata
        with open(scenario_file, 'r', encoding='utf-8') as f:
            scenario = yaml.safe_load(f)
        
        scenario_name = scenario.get('name', 'Unknown Scenario')
        scenario_desc = scenario.get('description', '')
        
        # Calculate summary stats
        total = len(results)
        passed = sum(1 for r in results if r['passed'])
        failed = total - passed
        
        # Generate HTML
        html = self._generate_html(
            scenario_name, 
            scenario_desc, 
            results, 
            total, 
            passed, 
            failed
        )
        
        # Write to file with UTF-8 encoding (fixes Windows encoding issues)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _generate_html(self, scenario_name, scenario_desc, results, total, passed, failed):
        """Generate complete HTML document"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECU Validation Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e1e4e8;
        }}
        .summary-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 6px;
            border: 2px solid #e1e4e8;
        }}
        .summary-card .label {{
            color: #6c757d;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
            margin-top: 8px;
        }}
        .summary-card.total .value {{ color: #667eea; }}
        .summary-card.passed .value {{ color: #28a745; }}
        .summary-card.failed .value {{ color: #dc3545; }}
        .metadata {{
            padding: 30px;
            border-bottom: 1px solid #e1e4e8;
        }}
        .metadata-item {{
            margin-bottom: 12px;
            font-size: 14px;
        }}
        .metadata-item strong {{
            color: #495057;
            display: inline-block;
            width: 140px;
        }}
        .results {{
            padding: 30px;
        }}
        .result-item {{
            margin-bottom: 20px;
            padding: 20px;
            border-left: 4px solid;
            border-radius: 4px;
        }}
        .result-item.pass {{
            border-left-color: #28a745;
            background: #f0fdf4;
        }}
        .result-item.fail {{
            border-left-color: #dc3545;
            background: #fef2f2;
        }}
        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .result-name {{
            font-size: 18px;
            font-weight: 600;
            color: #212529;
        }}
        .badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge.pass {{
            background: #28a745;
            color: white;
        }}
        .badge.fail {{
            background: #dc3545;
            color: white;
        }}
        .result-message {{
            color: #495057;
            line-height: 1.6;
        }}
        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Transmission ECU Validation Report</h1>
            <p>Automated validation results for transmission ECU behavior</p>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <div class="label">Total Checks</div>
                <div class="value">{total}</div>
            </div>
            <div class="summary-card passed">
                <div class="label">Passed</div>
                <div class="value">{passed}</div>
            </div>
            <div class="summary-card failed">
                <div class="label">Failed</div>
                <div class="value">{failed}</div>
            </div>
        </div>
        
        <div class="metadata">
            <div class="metadata-item">
                <strong>Test Scenario:</strong> {scenario_name}
            </div>
            <div class="metadata-item">
                <strong>Description:</strong> {scenario_desc}
            </div>
            <div class="metadata-item">
                <strong>Validation Time:</strong> {timestamp}
            </div>
        </div>
        
        <div class="results">
"""
        
        # Add each result
        for result in results:
            status = "pass" if result['passed'] else "fail"
            badge_text = "PASS" if result['passed'] else "FAIL"
            
            html += f"""
            <div class="result-item {status}">
                <div class="result-header">
                    <div class="result-name">{result['rule_name']}</div>
                    <span class="badge {status}">{badge_text}</span>
                </div>
                <div class="result-message">{result['message']}</div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            Generated by Transmission ECU Log Validator
        </div>
    </div>
</body>
</html>
"""
        
        return html