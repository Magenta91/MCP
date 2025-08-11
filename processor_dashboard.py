#!/usr/bin/env python3
"""
Dashboard for monitoring the Auto Dataset Processor
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any
from dotenv import load_dotenv
from utils import get_drive_service, list_files_in_folder

load_dotenv()

class ProcessorDashboard:
    def __init__(self, processed_files_log: str = "processed_files.json"):
        self.processed_files_log = processed_files_log
        self.server_folder_id = os.getenv('MCP_SERVER_FOLDER_ID')
    
    def _load_processed_files(self) -> Dict[str, Any]:
        """Load processed files log."""
        if os.path.exists(self.processed_files_log):
            try:
                with open(self.processed_files_log, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _get_folder_stats(self) -> Dict[str, Any]:
        """Get statistics about the monitored folder."""
        try:
            drive_service = get_drive_service()
            all_files = list_files_in_folder(drive_service, self.server_folder_id)
            
            total_files = len(all_files)
            supported_files = len([f for f in all_files if f['name'].lower().endswith(('.csv', '.xlsx', '.xls'))])
            
            return {
                "total_files": total_files,
                "supported_files": supported_files,
                "unsupported_files": total_files - supported_files
            }
        except Exception as e:
            return {"error": str(e)}
    
    def show_status(self):
        """Show current processor status."""
        print("📊 MCP Auto Processor Dashboard")
        print("=" * 50)
        
        # Load processed files
        processed_files = self._load_processed_files()
        
        # Get folder stats
        folder_stats = self._get_folder_stats()
        
        # Basic stats
        print(f"📁 Monitored Folder: {self.server_folder_id}")
        print(f"📋 Processed Files: {len(processed_files)}")
        
        if "error" not in folder_stats:
            print(f"📄 Total Files in Folder: {folder_stats['total_files']}")
            print(f"✅ Supported Files: {folder_stats['supported_files']}")
            print(f"❌ Unsupported Files: {folder_stats['unsupported_files']}")
            
            # Calculate pending files
            pending = folder_stats['supported_files'] - len(processed_files)
            print(f"⏳ Pending Files: {max(0, pending)}")
        else:
            print(f"❌ Error accessing folder: {folder_stats['error']}")
        
        print()
        
        # Recent activity
        if processed_files:
            print("🕐 Recent Activity:")
            print("-" * 30)
            
            # Sort by processed time
            recent_files = sorted(
                processed_files.items(),
                key=lambda x: x[1].get('processed_at', ''),
                reverse=True
            )[:5]  # Last 5 files
            
            for file_id, info in recent_files:
                try:
                    processed_time = datetime.fromisoformat(info['processed_at'])
                    time_ago = datetime.now() - processed_time
                    
                    if time_ago.days > 0:
                        time_str = f"{time_ago.days}d ago"
                    elif time_ago.seconds > 3600:
                        time_str = f"{time_ago.seconds // 3600}h ago"
                    elif time_ago.seconds > 60:
                        time_str = f"{time_ago.seconds // 60}m ago"
                    else:
                        time_str = "just now"
                    
                    print(f"  📄 {info['filename'][:40]:<40} {time_str}")
                    print(f"     📊 {info['row_count']:,} rows × {info['column_count']} cols, {info['dq_rules_count']} rules")
                    
                except Exception as e:
                    print(f"  ❌ Error displaying {info.get('filename', 'unknown')}: {e}")
            
            print()
        else:
            print("📭 No files processed yet")
            print()
    
    def show_detailed_stats(self):
        """Show detailed statistics."""
        processed_files = self._load_processed_files()
        
        if not processed_files:
            print("📭 No processed files to analyze")
            return
        
        print("📈 Detailed Statistics")
        print("=" * 30)
        
        # Calculate stats
        total_rows = sum(info.get('row_count', 0) for info in processed_files.values())
        total_columns = sum(info.get('column_count', 0) for info in processed_files.values())
        total_rules = sum(info.get('dq_rules_count', 0) for info in processed_files.values())
        
        avg_rows = total_rows / len(processed_files) if processed_files else 0
        avg_columns = total_columns / len(processed_files) if processed_files else 0
        avg_rules = total_rules / len(processed_files) if processed_files else 0
        
        print(f"📊 Total Datasets: {len(processed_files)}")
        print(f"📊 Total Rows: {total_rows:,}")
        print(f"📊 Total Columns: {total_columns:,}")
        print(f"📊 Total DQ Rules: {total_rules:,}")
        print()
        print(f"📊 Average Rows per Dataset: {avg_rows:,.1f}")
        print(f"📊 Average Columns per Dataset: {avg_columns:.1f}")
        print(f"📊 Average DQ Rules per Dataset: {avg_rules:.1f}")
        print()
        
        # Processing timeline
        print("📅 Processing Timeline (Last 7 days):")
        print("-" * 40)
        
        # Group by date
        daily_counts = {}
        for info in processed_files.values():
            try:
                processed_date = datetime.fromisoformat(info['processed_at']).date()
                daily_counts[processed_date] = daily_counts.get(processed_date, 0) + 1
            except:
                continue
        
        # Show last 7 days
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).date()
            count = daily_counts.get(date, 0)
            bar = "█" * count if count > 0 else "░"
            print(f"  {date} │ {bar} {count}")
        
        print()
    
    def monitor_live(self, refresh_interval: int = 10):
        """Live monitoring with auto-refresh."""
        print("🔴 Live Monitoring Mode (Press Ctrl+C to exit)")
        print(f"🔄 Refreshing every {refresh_interval} seconds")
        print()
        
        try:
            while True:
                # Clear screen (works on most terminals)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print(f"🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                self.show_status()
                
                print(f"🔄 Next refresh in {refresh_interval} seconds... (Ctrl+C to exit)")
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Live monitoring stopped")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Processor Dashboard")
    parser.add_argument('--live', action='store_true', help='Live monitoring mode')
    parser.add_argument('--stats', action='store_true', help='Show detailed statistics')
    parser.add_argument('--refresh', type=int, default=10, help='Refresh interval for live mode')
    
    args = parser.parse_args()
    
    dashboard = ProcessorDashboard()
    
    if args.live:
        dashboard.monitor_live(args.refresh)
    elif args.stats:
        dashboard.show_detailed_stats()
    else:
        dashboard.show_status()

if __name__ == "__main__":
    main()