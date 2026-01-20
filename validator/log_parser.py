"""
Log Parser Module
Loads and parses ECU log files from CSV format
"""

import pandas as pd


class LogParser:
    """Handles parsing of ECU log files"""
    
    def load_csv(self, filepath):
        """
        Load ECU log from CSV file
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            pandas.DataFrame with columns: timestamp_ms, signal, value
        """
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_cols = ['timestamp_ms', 'signal', 'value']
        missing = set(required_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Ensure timestamp is integer
        df['timestamp_ms'] = df['timestamp_ms'].astype(int)
        
        # Sort by timestamp for sequential processing
        df = df.sort_values('timestamp_ms').reset_index(drop=True)
        
        return df