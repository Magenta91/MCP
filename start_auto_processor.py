#!/usr/bin/env python3
"""
Easy startup script for the MCP Auto Dataset Processor
"""

import os
import sys
from dotenv import load_dotenv
from auto_processor import AutoDatasetProcessor
from auto_config import get_config, print_config

load_dotenv()

def check_setup():
    """Check if everything is properly configured."""
    print("🔧 Checking setup...")
    
    # Check environment variables
    required_vars = ['GOOGLE_SERVICE_ACCOUNT_KEY_PATH', 'MCP_SERVER_FOLDER_ID', 'MCP_CLIENT_FOLDER_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please check your .env file")
        return False
    
    # Check service account key file
    key_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY_PATH')
    if not os.path.exists(key_path):
        print(f"❌ Service account key file not found: {key_path}")
        return False
    
    print("✅ Setup looks good!")
    return True

def main():
    print("🤖 MCP Auto Dataset Processor Startup")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        sys.exit(1)
    
    # Print configuration
    print_config()
    
    # Get configuration
    config = get_config()
    
    print("🚀 Starting Auto Processor...")
    print(f"📁 Monitoring folder: {os.getenv('MCP_SERVER_FOLDER_ID')}")
    print(f"⏱️  Check interval: {config['check_interval']} seconds")
    print(f"📋 Supported formats: {', '.join(config['supported_extensions'])}")
    print(f"🛑 Press Ctrl+C to stop\n")
    
    try:
        # Create and start the processor
        processor = AutoDatasetProcessor(
            check_interval=config['check_interval'],
            processed_files_log=config['processed_files_log']
        )
        
        # Run continuous monitoring
        processor.run_continuous()
        
    except KeyboardInterrupt:
        print("\n\n👋 Auto processor stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()