#!/usr/bin/env python3
"""
Configuration and setup for the Auto Dataset Processor
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Auto Processor Configuration
AUTO_PROCESSOR_CONFIG = {
    # How often to check for new files (in seconds)
    "check_interval": 30,
    
    # Minimum age of file before processing (to avoid processing while uploading)
    "min_file_age_minutes": 1,
    
    # Supported file extensions
    "supported_extensions": ['.csv', '.xlsx', '.xls'],
    
    # Log file for tracking processed files
    "processed_files_log": "processed_files.json",
    
    # Output folder for organized datasets
    "output_folder": "processed_datasets",
    
    # Enable detailed logging
    "verbose_logging": True,
    
    # Auto-retry failed files after this many seconds
    "retry_failed_after": 3600,  # 1 hour
    
    # Maximum number of files to process in one cycle
    "max_files_per_cycle": 5
}

def get_config():
    """Get the current configuration."""
    return AUTO_PROCESSOR_CONFIG.copy()

def update_config(**kwargs):
    """Update configuration values."""
    for key, value in kwargs.items():
        if key in AUTO_PROCESSOR_CONFIG:
            AUTO_PROCESSOR_CONFIG[key] = value
            print(f"✅ Updated {key} = {value}")
        else:
            print(f"❌ Unknown config key: {key}")

def print_config():
    """Print current configuration."""
    print("⚙️  Auto Processor Configuration:")
    print("=" * 40)
    for key, value in AUTO_PROCESSOR_CONFIG.items():
        print(f"{key:25}: {value}")
    print()

if __name__ == "__main__":
    print_config()