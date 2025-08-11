#!/usr/bin/env python3
"""
Dataset Manager CLI - Manage processed datasets
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from dataset_processor import process_dataset_with_organization, list_processed_datasets

load_dotenv()

def list_datasets():
    """List all processed datasets."""
    datasets = list_processed_datasets()
    
    if not datasets:
        print("📭 No processed datasets found.")
        return
    
    print(f"📊 Found {len(datasets)} processed dataset(s):")
    print("-" * 80)
    
    for i, dataset in enumerate(datasets, 1):
        print(f"{i:2d}. {dataset['dataset_name']}")
        print(f"    📄 File: {dataset['filename']}")
        print(f"    📊 Size: {dataset['row_count']:,} rows × {dataset['column_count']} columns")
        print(f"    📁 Path: {dataset['folder_path']}")
        print()

def process_new_dataset(file_id: str):
    """Process a new dataset."""
    print(f"🚀 Processing dataset with file ID: {file_id}")
    result = process_dataset_with_organization(file_id)
    
    if result["status"] == "success":
        print(f"\n✅ Processing completed successfully!")
        print(f"📁 Output folder: {result['output_folder']}")
        print(f"📄 Files created: {len(result['files_created'])} files")
    else:
        print(f"\n❌ Processing failed: {result['message']}")

def show_dataset_info(dataset_name: str):
    """Show detailed information about a specific dataset."""
    datasets = list_processed_datasets()
    dataset = next((d for d in datasets if d['dataset_name'] == dataset_name), None)
    
    if not dataset:
        print(f"❌ Dataset '{dataset_name}' not found.")
        return
    
    readme_path = os.path.join(dataset['folder_path'], "README.md")
    if os.path.exists(readme_path):
        print(f"📋 Dataset Information: {dataset_name}")
        print("=" * 50)
        with open(readme_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print(f"❌ README file not found for dataset '{dataset_name}'")

def clean_datasets():
    """Remove all processed datasets."""
    datasets = list_processed_datasets()
    
    if not datasets:
        print("📭 No datasets to clean.")
        return
    
    confirm = input(f"⚠️  Are you sure you want to delete {len(datasets)} dataset(s)? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Operation cancelled.")
        return
    
    import shutil
    try:
        shutil.rmtree("processed_datasets")
        print(f"✅ Successfully removed {len(datasets)} dataset(s).")
    except Exception as e:
        print(f"❌ Error cleaning datasets: {e}")

def main():
    parser = argparse.ArgumentParser(description="MCP Dataset Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    subparsers.add_parser('list', help='List all processed datasets')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a new dataset')
    process_parser.add_argument('file_id', help='Google Drive file ID')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show dataset information')
    info_parser.add_argument('dataset_name', help='Dataset name')
    
    # Clean command
    subparsers.add_parser('clean', help='Remove all processed datasets')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🔧 MCP Dataset Manager")
    print("=" * 30)
    
    if args.command == 'list':
        list_datasets()
    elif args.command == 'process':
        process_new_dataset(args.file_id)
    elif args.command == 'info':
        show_dataset_info(args.dataset_name)
    elif args.command == 'clean':
        clean_datasets()

if __name__ == "__main__":
    main()