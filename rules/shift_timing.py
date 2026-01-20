"""
Shift Timing Validation Rule
Verifies that gear shifts occur within maximum allowed delay
"""


def validate_shift_timing(log_data, scenario):
    """
    Validate that gear changes occur within time limit after shift request
    
    Args:
        log_data: pandas.DataFrame with log entries
        scenario: dict containing test scenario configuration
        
    Returns:
        tuple: (passed: bool, message: str)
    """
    max_delay_ms = scenario['shift_timing']['max_delay_ms']
    
    # Extract shift requests and gear changes
    shift_requests = log_data[log_data['signal'] == 'shift_request']
    gear_changes = log_data[log_data['signal'] == 'gear_change']
    
    if shift_requests.empty:
        return False, "No shift requests found in log"
    
    if gear_changes.empty:
        return False, "No gear changes found in log"
    
    # Check timing for each shift request
    for idx, request in shift_requests.iterrows():
        request_time = request['timestamp_ms']
        target_gear = request['value']
        
        # Find corresponding gear change after this request
        subsequent_changes = gear_changes[
            (gear_changes['timestamp_ms'] > request_time) &
            (gear_changes['value'] == target_gear)
        ]
        
        if subsequent_changes.empty:
            return False, f"No gear change to gear {target_gear} found after shift request at {request_time}ms"
        
        # Get first matching gear change
        change = subsequent_changes.iloc[0]
        delay = change['timestamp_ms'] - request_time
        
        if delay > max_delay_ms:
            return False, f"Shift delay of {delay}ms exceeds maximum allowed {max_delay_ms}ms (request at {request_time}ms, change at {change['timestamp_ms']}ms)"
    
    return True, f"All {len(shift_requests)} gear shifts completed within {max_delay_ms}ms limit"