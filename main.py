"""
Transmission ECU Log Validator - Main Entry Point
Validates ECU logs against predefined test scenarios
"""

import os
from validator.log_parser import LogParser
from validator.rule_engine import RuleEngine
from validator.report_generator import ReportGenerator


def main():
    """Main validation workflow"""
    print("=" * 60)
    print("Transmission ECU Log Validator")
    print("=" * 60)
    
    # Define paths
    log_file = "logs/sample_log.csv"
    scenario_file = "scenarios/gear_shift_2_to_3.yaml"
    report_file = "reports/report.html"
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Step 1: Parse log file
    print(f"\n[1/3] Loading ECU log: {log_file}")
    parser = LogParser()
    log_data = parser.load_csv(log_file)
    print(f"      ✓ Loaded {len(log_data)} log entries")
    
    # Step 2: Run validation
    print(f"\n[2/3] Running validation against: {scenario_file}")
    engine = RuleEngine()
    results = engine.validate(log_data, scenario_file)
    
    passed = sum(1 for r in results if r['passed'])
    print(f"      ✓ Validation complete: {passed}/{len(results)} checks passed")
    
    # Step 3: Generate report
    print(f"\n[3/3] Generating HTML report: {report_file}")
    generator = ReportGenerator()
    generator.generate(results, scenario_file, report_file)
    print(f"      ✓ Report saved successfully")
    
    # Summary
    print("\n" + "=" * 60)
    if passed == len(results):
        print("✓ ALL VALIDATIONS PASSED")
    else:
        print(f"✗ {len(results) - passed} validation(s) failed")
    print("=" * 60)
    print(f"\nView full report: {report_file}\n")


if __name__ == "__main__":
    main()