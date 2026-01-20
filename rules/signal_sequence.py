"""
Signal Sequence Validation Rule
Verifies that signals occur in the expected order
"""


def validate_signal_sequence(log_data, scenario):
    """
    Validate that signals appear in the expected chronological order
    
    Args:
        log_data: pandas.DataFrame with log entries
        scenario: dict containing test scenario configuration
        
    Returns:
        tuple: (passed: bool, message: str)
    """
    expected_order = scenario['signal_sequence']['expected_order']
    
    # Get first occurrence of each expected signal
    signal_timestamps = {}
    
    for signal_name in expected_order:
        matching_entries = log_data[log_data['signal'] == signal_name]
        
        if matching_entries.empty:
            return False, f"Required signal '{signal_name}' not found in log"
        
        # Record timestamp of first occurrence
        first_occurrence = matching_entries.iloc[0]
        signal_timestamps[signal_name] = first_occurrence['timestamp_ms']
    
    # Verify chronological order
    for i in range(len(expected_order) - 1):
        current_signal = expected_order[i]
        next_signal = expected_order[i + 1]
        
        current_time = signal_timestamps[current_signal]
        next_time = signal_timestamps[next_signal]
        
        if next_time < current_time:
            return False, f"Signal '{next_signal}' occurred at {next_time}ms before '{current_signal}' at {current_time}ms (expected order violated)"
    
    # Build timeline string for success message (use -> for Windows compatibility)
    timeline = " -> ".join([
        f"{sig}({signal_timestamps[sig]}ms)" 
        for sig in expected_order
    ])
    
    return True, f"Signals appeared in correct sequence: {timeline}"