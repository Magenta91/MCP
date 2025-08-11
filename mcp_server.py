#!/usr/bin/env python3
"""
True MCP (Model Context Protocol) Server for Dataset Onboarding
This implements the actual MCP protocol for LLM integration.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Import our existing functions
from dataset_processor import process_dataset_with_organization, list_processed_datasets
from utils import (
    get_drive_service,
    download_file_from_drive,
    list_files_in_folder,
    extract_metadata_from_dataframe,
    suggest_dq_rules,
    generate_dq_report
)
import pandas as pd
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Create MCP server instance
server = Server("dataset-onboarding")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools for the MCP client (LLM)."""
    return [
        Tool(
            name="extract_dataset_metadata",
            description="Extract comprehensive metadata from a dataset file in Google Drive. Returns column information, data types, statistics, and quality metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "Google Drive file ID of the CSV or Excel file to analyze"
                    }
                },
                "required": ["file_id"]
            }
        ),
        Tool(
            name="generate_data_quality_rules",
            description="Generate intelligent data quality rules based on dataset characteristics. Suggests rules for null values, uniqueness, and value ranges.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "Google Drive file ID of the dataset to analyze for quality rules"
                    }
                },
                "required": ["file_id"]
            }
        ),
        Tool(
            name="process_complete_dataset",
            description="Run the complete dataset onboarding pipeline: extract metadata, generate quality rules, create contracts, and organize all artifacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "Google Drive file ID of the dataset to process completely"
                    }
                },
                "required": ["file_id"]
            }
        ),
        Tool(
            name="list_catalog_files",
            description="List all files currently in the data catalog (MCP_client folder). Shows what datasets have been processed and cataloged.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="list_processed_datasets",
            description="List all locally processed datasets with their metadata and processing information.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_dataset_summary",
            description="Get a comprehensive summary of a specific processed dataset including quality metrics and recommendations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_name": {
                        "type": "string",
                        "description": "Name of the processed dataset to summarize"
                    }
                },
                "required": ["dataset_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls from the MCP client (LLM)."""
    
    try:
        if name == "extract_dataset_metadata":
            file_id = arguments["file_id"]
            
            # Download and analyze file
            drive_service = get_drive_service()
            file_content = download_file_from_drive(file_id, drive_service)
            file_info = drive_service.files().get(fileId=file_id).execute()
            filename = file_info['name']
            
            # Read file based on extension
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(BytesIO(file_content))
            elif filename.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(BytesIO(file_content))
            else:
                raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
            
            # Extract metadata
            metadata = extract_metadata_from_dataframe(df, filename)
            
            # Format response for LLM
            summary = f"""Dataset Analysis Complete for: {filename}

📊 **Dataset Overview:**
- Rows: {metadata['row_count']:,}
- Columns: {metadata['column_count']}

📋 **Column Details:**
"""
            for col in metadata['columns']:
                summary += f"\n• **{col['name']}** ({col['data_type']})"
                summary += f"\n  - Null values: {col['null_count']} ({col['null_percentage']:.1f}%)"
                summary += f"\n  - Unique values: {col['unique_count']}"
                if 'min_value' in col:
                    summary += f"\n  - Range: {col['min_value']:.4f} to {col['max_value']:.4f}"
                    summary += f"\n  - Mean: {col['mean_value']:.4f}"
            
            return CallToolResult(
                content=[TextContent(type="text", text=summary)],
                isError=False
            )
        
        elif name == "generate_data_quality_rules":
            file_id = arguments["file_id"]
            
            # First extract metadata
            drive_service = get_drive_service()
            file_content = download_file_from_drive(file_id, drive_service)
            file_info = drive_service.files().get(fileId=file_id).execute()
            filename = file_info['name']
            
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(BytesIO(file_content))
            elif filename.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(BytesIO(file_content))
            else:
                raise ValueError("Unsupported file format")
            
            metadata = extract_metadata_from_dataframe(df, filename)
            dq_rules = suggest_dq_rules(metadata)
            
            # Format response
            summary = f"""Data Quality Rules Generated for: {filename}

🔍 **Generated {len(dq_rules)} Quality Rules:**

"""
            error_rules = [r for r in dq_rules if r['severity'] == 'error']
            warning_rules = [r for r in dq_rules if r['severity'] == 'warning']
            
            if error_rules:
                summary += "🔴 **Critical Rules (Errors):**\n"
                for rule in error_rules:
                    summary += f"• {rule['description']}\n"
                summary += "\n"
            
            if warning_rules:
                summary += "🟡 **Advisory Rules (Warnings):**\n"
                for rule in warning_rules:
                    summary += f"• {rule['description']}\n"
            
            summary += f"\n📊 **Rule Summary:**\n"
            summary += f"- Error-level rules: {len(error_rules)}\n"
            summary += f"- Warning-level rules: {len(warning_rules)}\n"
            summary += f"- Total rules: {len(dq_rules)}"
            
            return CallToolResult(
                content=[TextContent(type="text", text=summary)],
                isError=False
            )
        
        elif name == "process_complete_dataset":
            file_id = arguments["file_id"]
            
            # Run complete processing
            result = process_dataset_with_organization(file_id)
            
            if result["status"] == "success":
                metadata = result["metadata"]
                dq_rules = result["dq_rules"]
                
                summary = f"""✅ Complete Dataset Processing Successful!

📄 **Dataset:** {metadata['filename']}
📊 **Size:** {metadata['row_count']:,} rows × {metadata['column_count']} columns
🔍 **Quality Rules:** {len(dq_rules)} rules generated
📁 **Output Folder:** {result['output_folder']}

📋 **Generated Files:**
"""
                for file_path in result['files_created']:
                    filename = os.path.basename(file_path)
                    summary += f"• {filename}\n"
                
                summary += f"""
🎯 **Next Steps:**
1. Review the generated contract Excel file for schema details
2. Check the README.md for a comprehensive summary
3. Use the DQ report for quality assessment
4. All files are organized in: {result['output_folder']}

The dataset is now fully processed and ready for use!"""
                
                return CallToolResult(
                    content=[TextContent(type="text", text=summary)],
                    isError=False
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"❌ Processing failed: {result.get('message', 'Unknown error')}")],
                    isError=True
                )
        
        elif name == "list_catalog_files":
            drive_service = get_drive_service()
            catalog_folder_id = os.getenv('MCP_CLIENT_FOLDER_ID')
            files = list_files_in_folder(drive_service, catalog_folder_id)
            
            if not files:
                summary = "📭 No files found in the data catalog."
            else:
                summary = f"📋 Data Catalog Contents ({len(files)} files):\n\n"
                for file_info in files:
                    summary += f"📄 **{file_info['name']}**\n"
                    summary += f"   📅 Created: {file_info.get('createdTime', 'Unknown')}\n"
                    summary += f"   📏 Size: {file_info.get('size', 'Unknown')} bytes\n\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=summary)],
                isError=False
            )
        
        elif name == "list_processed_datasets":
            datasets = list_processed_datasets()
            
            if not datasets:
                summary = "📭 No datasets have been processed locally yet."
            else:
                summary = f"📊 Processed Datasets ({len(datasets)} total):\n\n"
                for dataset in datasets:
                    summary += f"📄 **{dataset['dataset_name']}**\n"
                    summary += f"   📊 Size: {dataset['row_count']:,} rows × {dataset['column_count']} columns\n"
                    summary += f"   📁 Location: {dataset['folder_path']}\n\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=summary)],
                isError=False
            )
        
        elif name == "get_dataset_summary":
            dataset_name = arguments["dataset_name"]
            datasets = list_processed_datasets()
            dataset = next((d for d in datasets if d['dataset_name'] == dataset_name), None)
            
            if not dataset:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"❌ Dataset '{dataset_name}' not found.")],
                    isError=True
                )
            
            # Read the README file for comprehensive summary
            readme_path = os.path.join(dataset['folder_path'], "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                summary = f"📋 **Dataset Summary: {dataset_name}**\n\n{readme_content}"
            else:
                summary = f"📄 **{dataset_name}**\n"
                summary += f"📊 Size: {dataset['row_count']:,} rows × {dataset['column_count']} columns\n"
                summary += f"📁 Location: {dataset['folder_path']}\n"
                summary += "❌ Detailed README not found."
            
            return CallToolResult(
                content=[TextContent(type="text", text=summary)],
                isError=False
            )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"❌ Unknown tool: {name}")],
                isError=True
            )
    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ Error executing {name}: {str(e)}")],
            isError=True
        )

async def main():
    """Run the MCP server."""
    # Server options
    options = InitializationOptions(
        server_name="dataset-onboarding",
        server_version="1.0.0"
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options
        )

if __name__ == "__main__":
    asyncio.run(main())