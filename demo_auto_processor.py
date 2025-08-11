#!/usr/bin/env python3
"""
Demo script to showcase the Auto Dataset Processor
"""

import time
from auto_processor import AutoDatasetProcessor
from processor_dashboard import ProcessorDashboard

def demo():
    print("🎬 MCP Auto Dataset Processor Demo")
    print("=" * 50)
    
    print("This demo shows how the auto-processor works:")
    print("1. Monitors your Google Drive folder")
    print("2. Detects new files automatically")
    print("3. Processes them without manual intervention")
    print("4. Organizes all outputs neatly")
    print()
    
    # Show current status
    print("📊 Current Status:")
    dashboard = ProcessorDashboard()
    dashboard.show_status()
    
    print("🔍 Running a single check cycle to demonstrate...")
    
    # Create processor and run once
    processor = AutoDatasetProcessor()
    processed_count = processor.run_once()
    
    if processed_count > 0:
        print(f"✨ Processed {processed_count} file(s)!")
        print("\n📊 Updated Status:")
        dashboard.show_status()
    else:
        print("📭 No new files found to process")
        print("\n💡 To test the auto-processor:")
        print("   1. Upload a CSV or Excel file to your MCP_server Google Drive folder")
        print("   2. Run: python start_auto_processor.py")
        print("   3. Watch it process automatically!")
    
    print("\n🚀 Ready to start automatic monitoring?")
    print("   Run: python start_auto_processor.py")

if __name__ == "__main__":
    demo()