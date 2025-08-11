#!/usr/bin/env python3
"""
Local test script to process the dataset without Google Drive upload limitations.
This will download the file, process it, and save artifacts locally in organized folders.
"""

import os
from dotenv import load_dotenv
from dataset_processor import process_dataset_with_organization, list_processed_datasets

# Load environment variables
load_dotenv()

def display_processing_summary(result):
    """Display a comprehensive processing summary."""
    if result["status"] != "success":
        return
        
    metadata = result["metadata"]
    dq_rules = result["dq_rules"]
    
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print(f"Dataset: {metadata['filename']}")
    print(f"Rows: {metadata['row_count']:,}")
    print(f"Columns: {metadata['column_count']}")
    print(f"DQ Rules: {len(dq_rules)}")
    
    print("\nColumn Summary:")
    for col in metadata['columns']:
        print(f"  - {col['name']}: {col['data_type']} ({col['null_percentage']:.1f}% null)")
    
    print("\nData Quality Rules:")
    for rule in dq_rules:
        print(f"  - {rule['rule_type'].upper()}: {rule['description']} [{rule['severity']}]")

if __name__ == "__main__":
    # Test with your file ID
    file_id = "14n9OxaOzOOWuE81IC0J2VzfKvbJH3cYp"
    
    print("🚀 MCP Dataset Onboarding - Local Processing")
    print("=" * 50)
    
    # Process the dataset
    result = process_dataset_with_organization(file_id)
    
    if result["status"] == "success":
        print(f"\n✅ Processing completed successfully!")
        print(f"📁 Output folder: {result['output_folder']}")
        print(f"📄 Files created: {len(result['files_created'])} files")
        for file_path in result['files_created']:
            print(f"   - {os.path.basename(file_path)}")
        
        # Display processing summary
        display_processing_summary(result)
        
        # List all processed datasets
        print(f"\n📊 All Processed Datasets:")
        datasets = list_processed_datasets()
        for i, dataset in enumerate(datasets, 1):
            print(f"  {i}. {dataset['dataset_name']} ({dataset['row_count']:,} rows, {dataset['column_count']} cols)")
        
    else:
        print(f"\n❌ Processing failed: {result['message']}")