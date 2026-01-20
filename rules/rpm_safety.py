"""
RPM Safety Validation Rule
Verifies that engine RPM stays within safe operating limits
"""


def validate_rpm_safety(log_data, scenario):
    """
    Validate that engine RPM remains within safe limits
    
    Args:
        log_data: pandas.DataFrame with log entries
        scenario: dict containing test scenario configuration
        
    Returns:
        tuple: (passed: bool, message: str)
    """
    min_rpm = scenario['rpm_safety']['min_rpm']
    max_rpm = scenario['rpm_safety']['max_rpm']
    
    # Extract RPM readings
    rpm_entries = log_data[log_data['signal'] == 'engine_rpm']
    
    if rpm_entries.empty:
        return False, "No RPM data found in log"
    
    # Convert RPM values to numeric
    rpm_entries = rpm_entries.copy()
    rpm_entries['value'] = rpm_entries['value'].astype(float)
    
    # Check for violations
    violations = rpm_entries[
        (rpm_entries['value'] < min_rpm) | 
        (rpm_entries['value'] > max_rpm)
    ]
    
    if not violations.empty:
        first_violation = violations.iloc[0]
        rpm_value = first_violation['value']
        timestamp = first_violation['timestamp_ms']
        
        if rpm_value < min_rpm:
            return False, f"RPM {rpm_value} below minimum safe limit {min_rpm} at {timestamp}ms"
        else:
            return False, f"RPM {rpm_value} above maximum safe limit {max_rpm} at {timestamp}ms"
    
    # Calculate statistics
    min_observed = rpm_entries['value'].min()
    max_observed = rpm_entries['value'].max()
    
    return True, f"All {len(rpm_entries)} RPM readings within safe range [{min_rpm}, {max_rpm}] (observed range: [{min_observed}, {max_observed}])"