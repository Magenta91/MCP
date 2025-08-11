#!/usr/bin/env python3
"""
Centralized dataset processing module for both local and server use.
"""

import os
import json
import pandas as pd
from io import BytesIO
from typing import Dict, List, Any, Tuple
from utils import (
    get_drive_service,
    download_file_from_drive,
    extract_metadata_from_dataframe,
    suggest_dq_rules,
    create_contract_excel,
    generate_dq_report
)

def create_dataset_readme(metadata: Dict[str, Any], dq_rules: List[Dict[str, Any]], 
                         dq_report: Dict[str, Any], readme_path: str):
    """Create a comprehensive README file for the processed dataset."""
    content = f"""# Dataset Processing Report

## Dataset Information
- **Filename**: {metadata['filename']}
- **Rows**: {metadata['row_count']:,}
- **Columns**: {metadata['column_count']}
- **Processing Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Column Details
| Column Name | Data Type | Null Count | Null % | Unique Count | Min Value | Max Value | Mean |
|-------------|-----------|------------|--------|--------------|-----------|-----------|------|
"""
    
    for col in metadata['columns']:
        min_val = f"{col.get('min_value', 'N/A'):.4f}" if col.get('min_value') is not None else "N/A"
        max_val = f"{col.get('max_value', 'N/A'):.4f}" if col.get('max_value') is not None else "N/A"
        mean_val = f"{col.get('mean_value', 'N/A'):.4f}" if col.get('mean_value') is not None else "N/A"
        
        content += f"| {col['name']} | {col['data_type']} | {col['null_count']} | {col['null_percentage']:.1f}% | {col['unique_count']} | {min_val} | {max_val} | {mean_val} |\n"
    
    content += f"""
## Data Quality Summary
- **Total Rules**: {dq_report['data_quality_summary']['total_rules']}
- **Error Rules**: {dq_report['data_quality_summary']['error_rules']}
- **Warning Rules**: {dq_report['data_quality_summary']['warning_rules']}

## Data Quality Rules
"""
    
    for rule in dq_rules:
        severity_icon = "🔴" if rule['severity'] == 'error' else "🟡"
        content += f"- {severity_icon} **{rule['rule_type'].upper()}**: {rule['description']}\n"
    
    content += f"""
## Column Quality Metrics
"""
    
    for col_quality in dq_report['column_quality']:
        content += f"- **{col_quality['column_name']}**: {col_quality['completeness']:.1f}% complete, {col_quality['uniqueness']:.1f}% unique\n"
    
    content += f"""
## Files Generated
- `{metadata['filename']}` - Original dataset
- `{metadata['filename'].split('.')[0]}_metadata.json` - Detailed metadata
- `{metadata['filename'].split('.')[0]}_contract.xlsx` - Data contract with schema and DQ rules
- `{metadata['filename'].split('.')[0]}_dq_report.json` - Comprehensive data quality report
- `README.md` - This summary document

## Usage
This dataset has been processed through the MCP Dataset Onboarding pipeline. All artifacts are ready for catalog publication or further analysis.
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_dataset_with_organization(file_id: str, output_folder: str = "processed_datasets") -> Dict[str, Any]:
    """
    Process dataset and organize all artifacts in a dedicated folder structure.
    
    Args:
        file_id: Google Drive file ID
        output_folder: Base folder for organizing processed datasets
        
    Returns:
        Dictionary with processing results and file paths
    """
    try:
        print(f"Processing file ID: {file_id}")
        
        # Step 1: Download and extract metadata
        print("Step 1: Downloading file and extracting metadata...")
        drive_service = get_drive_service()
        
        # Download file
        file_content = download_file_from_drive(file_id, drive_service)
        
        # Get file info
        file_info = drive_service.files().get(fileId=file_id).execute()
        filename = file_info['name']
        print(f"Downloaded: {filename}")
        
        # Create output directory structure
        base_name = filename.split('.')[0]
        dataset_folder = os.path.join(output_folder, base_name)
        os.makedirs(dataset_folder, exist_ok=True)
        print(f"Created output folder: {dataset_folder}")
        
        # Read file based on extension
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        elif filename.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(file_content))
        else:
            raise Exception("Unsupported file format")
        
        # Extract metadata
        metadata = extract_metadata_from_dataframe(df, filename)
        print(f"[OK] Extracted metadata: {metadata['row_count']} rows, {metadata['column_count']} columns")
        
        # Step 2: Generate DQ rules
        print("Step 2: Generating data quality rules...")
        dq_rules = suggest_dq_rules(metadata)
        print(f"[OK] Generated {len(dq_rules)} DQ rules")
        
        # Step 3: Create contract Excel
        print("Step 3: Creating contract Excel file...")
        contract_filename = os.path.join(dataset_folder, f"{base_name}_contract.xlsx")
        create_contract_excel(metadata, dq_rules, contract_filename)
        print(f"[OK] Created contract: {contract_filename}")
        
        # Step 4: Generate DQ report
        print("Step 4: Generating DQ report...")
        dq_report = generate_dq_report(metadata, dq_rules)
        
        # Save artifacts in organized folder
        metadata_filename = os.path.join(dataset_folder, f"{base_name}_metadata.json")
        dq_report_filename = os.path.join(dataset_folder, f"{base_name}_dq_report.json")
        
        # Save original dataset for reference
        original_filename = os.path.join(dataset_folder, filename)
        with open(original_filename, 'wb') as f:
            f.write(file_content)
        
        with open(metadata_filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        with open(dq_report_filename, 'w') as f:
            json.dump(dq_report, f, indent=2)
        
        # Create a summary README for the dataset
        readme_filename = os.path.join(dataset_folder, "README.md")
        create_dataset_readme(metadata, dq_rules, dq_report, readme_filename)
        
        print(f"[OK] Saved artifacts in folder: {dataset_folder}")
        print(f"  - {os.path.basename(original_filename)} (original dataset)")
        print(f"  - {os.path.basename(metadata_filename)} (metadata)")
        print(f"  - {os.path.basename(contract_filename)} (contract)")
        print(f"  - {os.path.basename(dq_report_filename)} (DQ report)")
        print(f"  - {os.path.basename(readme_filename)} (summary)")
        
        return {
            "status": "success",
            "output_folder": dataset_folder,
            "files_created": [
                original_filename,
                metadata_filename, 
                contract_filename, 
                dq_report_filename,
                readme_filename
            ],
            "metadata": metadata,
            "dq_rules": dq_rules,
            "dq_report": dq_report
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

def list_processed_datasets(output_folder: str = "processed_datasets") -> List[Dict[str, Any]]:
    """List all processed datasets in the output folder."""
    datasets = []
    
    if not os.path.exists(output_folder):
        return datasets
    
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        if os.path.isdir(item_path):
            # Check if it's a valid dataset folder
            readme_path = os.path.join(item_path, "README.md")
            metadata_path = os.path.join(item_path, f"{item}_metadata.json")
            
            if os.path.exists(readme_path) and os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    datasets.append({
                        "dataset_name": item,
                        "folder_path": item_path,
                        "filename": metadata.get('filename', 'Unknown'),
                        "row_count": metadata.get('row_count', 0),
                        "column_count": metadata.get('column_count', 0),
                        "processed_date": os.path.getctime(item_path)
                    })
                except Exception as e:
                    print(f"Error reading metadata for {item}: {e}")
    
    return sorted(datasets, key=lambda x: x['processed_date'], reverse=True)