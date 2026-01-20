# Transmission ECU Log Validator

A Python-based validation tool for automotive transmission ECU testing that automates the analysis of CAN/ECU logs against predefined test scenarios.

## Problem Statement

In automotive transmission development, engineers test ECU behavior by analyzing CAN/ECU logs generated during test runs. Currently, validation is performed manually by scanning log files to verify:

- Gear shifts happened at the correct time
- RPM stayed within safe limits  
- Signals occurred in the correct order

This manual process is time-consuming, error-prone, and difficult to repeat consistently across test cycles.

## Solution

This tool provides automated, repeatable validation by:

1. Reading ECU/CAN logs from CSV files
2. Comparing log data against test scenarios defined in YAML
3. Applying rule-based validation checks
4. Generating clear HTML reports with pass/fail results

## How It Works

### Architecture

```
Test Scenario (YAML) → ECU Log (CSV) → Rule Engine (Python) → HTML Report
```

### Validation Rules

The tool implements three core validation rules:

1. **Shift Timing Rule**: Verifies gear changes occur within maximum delay after shift request
2. **RPM Safety Rule**: Ensures engine RPM remains within safe operating limits
3. **Signal Sequence Rule**: Validates signals appear in expected chronological order

Each rule returns a pass/fail status with a human-readable explanation.

## Project Structure

```
transmission-ecu-log-validator/
├── logs/
│   └── sample_log.csv              # Sample ECU log data
├── scenarios/
│   └── gear_shift_2_to_3.yaml      # Test scenario definition
├── rules/
│   ├── shift_timing.py             # Shift timing validation
│   ├── rpm_safety.py               # RPM safety validation
│   └── signal_sequence.py          # Signal sequence validation
├── reports/
│   └── report.html                 # Generated validation report
├── validator/
│   ├── log_parser.py               # CSV log parser
│   ├── rule_engine.py              # Validation orchestrator
│   └── report_generator.py         # HTML report generator
├── main.py                         # Entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the validation tool:

```bash
python main.py
```

This will:
- Load the ECU log from `logs/sample_log.csv`
- Validate against the scenario in `scenarios/gear_shift_2_to_3.yaml`
- Generate an HTML report at `reports/report.html`

### Expected Output

```
============================================================
Transmission ECU Log Validator
============================================================

[1/3] Loading ECU log: logs/sample_log.csv
      ✓ Loaded 16 log entries

[2/3] Running validation against: scenarios/gear_shift_2_to_3.yaml
      ✓ Validation complete: 3/3 checks passed

[3/3] Generating HTML report: reports/report.html
      ✓ Report saved successfully

============================================================
✓ ALL VALIDATIONS PASSED
============================================================

View full report: reports/report.html
```

## Sample Data

### Log Format (CSV)

```csv
timestamp_ms,signal,value
0,shift_request,2
50,gear_change,2
100,engine_rpm,1500
150,torque_stabilized,1
```

### Scenario Format (YAML)

```yaml
name: Gear Shift 2 to 3 Validation
description: Validates gear shift from 2nd to 3rd gear behavior

shift_timing:
  max_delay_ms: 100
  
rpm_safety:
  min_rpm: 1000
  max_rpm: 6000
  
signal_sequence:
  expected_order:
    - shift_request
    - gear_change
    - torque_stabilized
```

## Extending the Tool

### Adding New Validation Rules

1. Create a new file in `rules/` (e.g., `rules/temperature_check.py`)
2. Implement a validation function that returns `(bool, str)`:
   ```python
   def validate_temperature(log_data, scenario):
       # Your validation logic
       return True, "Temperature within limits"
   ```
3. Register the rule in `validator/rule_engine.py`

### Adding New Scenarios

Create a new YAML file in `scenarios/` with the required configuration for your test case.

## Future Enhancements

This MVP is designed to support future extensions:

- HIL (Hardware-in-the-Loop) automation integration
- ASPICE traceability linking
- Severity scoring for failures
- Command-line arguments for batch processing
- Support for additional log formats (DBC, ASC)

## Technical Details

- **Language**: Python 3.8+
- **Dependencies**: pandas, PyYAML
- **Design Philosophy**: Clean, modular, maintainable code suitable for production environments

## Author Notes

This tool demonstrates:
- Automotive domain knowledge (ECU testing, CAN protocols)
- Software engineering best practices (modularity, separation of concerns)
- Real-world problem-solving in validation engineering
- Clear documentation and user-facing outputs

Built as a minimal viable product focused on correctness and extensibility over feature completeness.