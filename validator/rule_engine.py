"""
Rule Engine Module
Orchestrates execution of all validation rules
"""

import yaml
from rules.shift_timing import validate_shift_timing
from rules.rpm_safety import validate_rpm_safety
from rules.signal_sequence import validate_signal_sequence


class RuleEngine:
    """Executes validation rules against log data"""
    
    def validate(self, log_data, scenario_file):
        """
        Run all validation rules
        
        Args:
            log_data: pandas.DataFrame containing log entries
            scenario_file: Path to YAML scenario file
            
        Returns:
            List of validation results, each containing:
            - rule_name: Name of the rule
            - passed: Boolean pass/fail status
            - message: Human-readable explanation
        """
        # Load scenario configuration
        with open(scenario_file, 'r') as f:
            scenario = yaml.safe_load(f)
        
        results = []
        
        # Execute each validation rule
        rules = [
            ("Shift Timing", validate_shift_timing),
            ("RPM Safety", validate_rpm_safety),
            ("Signal Sequence", validate_signal_sequence)
        ]
        
        for rule_name, rule_func in rules:
            passed, message = rule_func(log_data, scenario)
            results.append({
                'rule_name': rule_name,
                'passed': passed,
                'message': message
            })
        
        return results