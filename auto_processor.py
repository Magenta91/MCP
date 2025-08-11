#!/usr/bin/env python3
"""
Automated Dataset Processor - Watches Google Drive folder for new files
and automatically processes them without manual intervention.
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Set, Dict, List, Any
from dotenv import load_dotenv
from dataset_processor import process_dataset_with_organization
from utils import get_drive_service, list_files_in_folder

load_dotenv()

class AutoDatasetProcessor:
    def __init__(self, 
                 server_folder_id: str = None,
                 check_interval: int = 30,
                 processed_files_log: str = "processed_files.json"):
        """
        Initialize the auto processor.
        
        Args:
            server_folder_id: Google Drive folder ID to monitor
            check_interval: How often to check for new files (seconds)
            processed_files_log: File to track already processed files
        """
        self.server_folder_id = server_folder_id or os.getenv('MCP_SERVER_FOLDER_ID')
        self.check_interval = check_interval
        self.processed_files_log = processed_files_log
        self.drive_service = None
        self.processed_files = self._load_processed_files()
        
        if not self.server_folder_id:
            raise ValueError("MCP_SERVER_FOLDER_ID not found in environment variables")
    
    def _load_processed_files(self) -> Dict[str, Dict[str, Any]]:
        """Load the list of already processed files."""
        if os.path.exists(self.processed_files_log):
            try:
                with open(self.processed_files_log, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load processed files log: {e}")
        return {}
    
    def _save_processed_files(self):
        """Save the list of processed files."""
        try:
            with open(self.processed_files_log, 'w') as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save processed files log: {e}")
    
    def _is_supported_file(self, filename: str) -> bool:
        """Check if the file is a supported format."""
        return filename.lower().endswith(('.csv', '.xlsx', '.xls'))
    
    def _get_new_files(self) -> List[Dict[str, Any]]:
        """Get list of new files that haven't been processed yet."""
        try:
            if not self.drive_service:
                self.drive_service = get_drive_service()
            
            # Get all files in the server folder
            all_files = list_files_in_folder(self.drive_service, self.server_folder_id)
            
            new_files = []
            for file_info in all_files:
                file_id = file_info['id']
                filename = file_info['name']
                
                # Skip if not supported format
                if not self._is_supported_file(filename):
                    continue
                
                # Skip if already processed
                if file_id in self.processed_files:
                    continue
                
                # Skip if file is too recent (might still be uploading)
                try:
                    created_time = datetime.fromisoformat(file_info['createdTime'].replace('Z', '+00:00'))
                    if datetime.now().astimezone() - created_time < timedelta(minutes=1):
                        print(f"⏳ Skipping {filename} - too recent, might still be uploading")
                        continue
                except:
                    pass  # If we can't parse time, process anyway
                
                new_files.append(file_info)
            
            return new_files
            
        except Exception as e:
            print(f"❌ Error checking for new files: {e}")
            return []
    
    def _process_file(self, file_info: Dict[str, Any]) -> bool:
        """Process a single file."""
        file_id = file_info['id']
        filename = file_info['name']
        
        try:
            print(f"\n🚀 Auto-processing new file: {filename}")
            print(f"📄 File ID: {file_id}")
            print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Process the dataset
            result = process_dataset_with_organization(file_id)
            
            if result["status"] == "success":
                # Mark as processed
                self.processed_files[file_id] = {
                    "filename": filename,
                    "processed_at": datetime.now().isoformat(),
                    "output_folder": result["output_folder"],
                    "row_count": result["metadata"]["row_count"],
                    "column_count": result["metadata"]["column_count"],
                    "dq_rules_count": len(result["dq_rules"])
                }
                self._save_processed_files()
                
                print(f"✅ Successfully processed {filename}")
                print(f"📁 Output: {result['output_folder']}")
                print(f"📊 Data: {result['metadata']['row_count']:,} rows × {result['metadata']['column_count']} columns")
                print(f"🔍 Generated {len(result['dq_rules'])} quality rules")
                return True
            else:
                print(f"❌ Failed to process {filename}: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            return False
    
    def _print_status(self):
        """Print current monitoring status."""
        print(f"\n📊 Monitoring Status:")
        print(f"   📁 Folder ID: {self.server_folder_id}")
        print(f"   ⏱️  Check interval: {self.check_interval} seconds")
        print(f"   📋 Processed files: {len(self.processed_files)}")
        print(f"   🕐 Last check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def run_once(self) -> int:
        """Run one check cycle and return number of files processed."""
        print(f"\n🔍 Checking for new files...")
        
        new_files = self._get_new_files()
        
        if not new_files:
            print("📭 No new files found")
            return 0
        
        print(f"🆕 Found {len(new_files)} new file(s) to process:")
        for file_info in new_files:
            print(f"   - {file_info['name']} (ID: {file_info['id']})")
        
        processed_count = 0
        for file_info in new_files:
            if self._process_file(file_info):
                processed_count += 1
            
            # Small delay between files
            if len(new_files) > 1:
                time.sleep(2)
        
        return processed_count
    
    def run_continuous(self):
        """Run continuous monitoring."""
        print("🤖 MCP Auto Dataset Processor Started")
        print("=" * 50)
        print(f"📁 Monitoring folder: {self.server_folder_id}")
        print(f"⏱️  Check interval: {self.check_interval} seconds")
        print(f"🛑 Press Ctrl+C to stop")
        
        try:
            while True:
                try:
                    processed_count = self.run_once()
                    
                    if processed_count > 0:
                        print(f"\n✨ Processed {processed_count} file(s) in this cycle")
                    
                    self._print_status()
                    
                    # Wait before next check
                    print(f"\n💤 Waiting {self.check_interval} seconds before next check...")
                    time.sleep(self.check_interval)
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"❌ Error in monitoring cycle: {e}")
                    print("⏳ Waiting 60 seconds before retry...")
                    time.sleep(60)
                    
        except KeyboardInterrupt:
            print(f"\n\n🛑 Auto processor stopped by user")
            print(f"📊 Total files processed: {len(self.processed_files)}")
    
    def list_processed_files(self):
        """List all processed files."""
        if not self.processed_files:
            print("📭 No files have been processed yet.")
            return
        
        print(f"📋 Processed Files ({len(self.processed_files)} total):")
        print("-" * 80)
        
        for file_id, info in self.processed_files.items():
            processed_time = datetime.fromisoformat(info['processed_at']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"📄 {info['filename']}")
            print(f"   🕐 Processed: {processed_time}")
            print(f"   📊 Size: {info['row_count']:,} rows × {info['column_count']} columns")
            print(f"   🔍 DQ Rules: {info['dq_rules_count']}")
            print(f"   📁 Output: {info['output_folder']}")
            print()
    
    def reset_processed_files(self):
        """Reset the processed files log (for testing)."""
        self.processed_files = {}
        self._save_processed_files()
        print("🔄 Processed files log has been reset.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Auto Dataset Processor")
    parser.add_argument('--interval', type=int, default=30, 
                       help='Check interval in seconds (default: 30)')
    parser.add_argument('--once', action='store_true', 
                       help='Run once instead of continuous monitoring')
    parser.add_argument('--list', action='store_true', 
                       help='List all processed files')
    parser.add_argument('--reset', action='store_true', 
                       help='Reset processed files log')
    
    args = parser.parse_args()
    
    try:
        processor = AutoDatasetProcessor(check_interval=args.interval)
        
        if args.list:
            processor.list_processed_files()
        elif args.reset:
            processor.reset_processed_files()
        elif args.once:
            print("🔍 Running single check cycle...")
            processed_count = processor.run_once()
            print(f"\n✨ Processed {processed_count} file(s)")
        else:
            processor.run_continuous()
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()