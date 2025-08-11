#!/usr/bin/env python3
"""
Debug script to troubleshoot Google Drive access and file detection
"""

import os
from dotenv import load_dotenv
from utils import get_drive_service, list_files_in_folder

load_dotenv()

def debug_drive_access():
    print("🔍 MCP Drive Access Diagnostics")
    print("=" * 50)
    
    # Check environment variables
    print("1. Environment Variables:")
    server_folder_id = os.getenv('MCP_SERVER_FOLDER_ID')
    client_folder_id = os.getenv('MCP_CLIENT_FOLDER_ID')
    key_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY_PATH')
    
    print(f"   📁 Server Folder ID: {server_folder_id}")
    print(f"   📁 Client Folder ID: {client_folder_id}")
    print(f"   🔑 Service Account Key: {key_path}")
    
    if not server_folder_id:
        print("   ❌ MCP_SERVER_FOLDER_ID is missing!")
        return
    
    if not key_path or not os.path.exists(key_path):
        print(f"   ❌ Service account key file not found: {key_path}")
        return
    
    print("   ✅ Environment variables look good")
    print()
    
    # Test Google Drive connection
    print("2. Google Drive Connection:")
    try:
        drive_service = get_drive_service()
        print("   ✅ Successfully connected to Google Drive API")
    except Exception as e:
        print(f"   ❌ Failed to connect to Google Drive: {e}")
        return
    
    print()
    
    # Test folder access
    print("3. Folder Access Test:")
    try:
        # Test server folder access
        print(f"   Testing server folder access ({server_folder_id})...")
        folder_info = drive_service.files().get(fileId=server_folder_id).execute()
        print(f"   ✅ Server folder accessible: '{folder_info['name']}'")
        
        # Test client folder access
        print(f"   Testing client folder access ({client_folder_id})...")
        folder_info = drive_service.files().get(fileId=client_folder_id).execute()
        print(f"   ✅ Client folder accessible: '{folder_info['name']}'")
        
    except Exception as e:
        print(f"   ❌ Folder access failed: {e}")
        print("   💡 Make sure the service account has access to both folders")
        return
    
    print()
    
    # List files in server folder
    print("4. Files in Server Folder:")
    try:
        files = list_files_in_folder(drive_service, server_folder_id)
        
        if not files:
            print("   📭 No files found in server folder")
            print("   💡 Try uploading a CSV or Excel file to the folder")
        else:
            print(f"   📄 Found {len(files)} file(s):")
            for i, file_info in enumerate(files, 1):
                file_name = file_info['name']
                file_id = file_info['id']
                file_size = file_info.get('size', 'Unknown')
                created_time = file_info.get('createdTime', 'Unknown')
                
                # Check if supported format
                is_supported = file_name.lower().endswith(('.csv', '.xlsx', '.xls'))
                support_icon = "✅" if is_supported else "❌"
                
                print(f"   {i:2d}. {support_icon} {file_name}")
                print(f"       📄 ID: {file_id}")
                print(f"       📊 Size: {file_size} bytes")
                print(f"       🕐 Created: {created_time}")
                print()
                
    except Exception as e:
        print(f"   ❌ Failed to list files: {e}")
        return
    
    print()
    
    # Test file processing capability
    print("5. Processing Test:")
    if files:
        # Find first supported file
        supported_file = None
        for file_info in files:
            if file_info['name'].lower().endswith(('.csv', '.xlsx', '.xls')):
                supported_file = file_info
                break
        
        if supported_file:
            print(f"   🧪 Testing with file: {supported_file['name']}")
            print(f"   📄 File ID: {supported_file['id']}")
            
            # Test if we can download the file
            try:
                from utils import download_file_from_drive
                file_content = download_file_from_drive(supported_file['id'], drive_service)
                print(f"   ✅ Successfully downloaded file ({len(file_content)} bytes)")
                
                # Test if we can read the file
                import pandas as pd
                from io import BytesIO
                
                filename = supported_file['name']
                if filename.lower().endswith('.csv'):
                    df = pd.read_csv(BytesIO(file_content))
                elif filename.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(BytesIO(file_content))
                
                print(f"   ✅ Successfully parsed file: {len(df)} rows × {len(df.columns)} columns")
                print(f"   📊 Columns: {list(df.columns)}")
                
            except Exception as e:
                print(f"   ❌ Failed to process file: {e}")
        else:
            print("   ⚠️  No supported files found for testing")
    else:
        print("   ⚠️  No files available for testing")
    
    print()
    print("🎯 Diagnosis Complete!")
    print("=" * 30)
    
    if files:
        supported_count = len([f for f in files if f['name'].lower().endswith(('.csv', '.xlsx', '.xls'))])
        if supported_count > 0:
            print(f"✅ Found {supported_count} supported file(s) ready for processing")
            print("💡 The auto-processor should be able to detect and process these files")
        else:
            print("⚠️  Files found but none are in supported formats (CSV, Excel)")
            print("💡 Upload CSV or Excel files to test the auto-processor")
    else:
        print("📭 No files found in the monitored folder")
        print("💡 Upload a CSV or Excel file to your Google Drive folder and try again")

if __name__ == "__main__":
    debug_drive_access()