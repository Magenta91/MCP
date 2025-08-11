import os
import tempfile
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import json
from io import BytesIO

from utils import (
    get_drive_service,
    download_file_from_drive,
    upload_to_drive,
    upload_to_drive_file,
    list_files_in_folder,
    extract_metadata_from_dataframe,
    suggest_dq_rules,
    create_contract_excel,
    generate_dq_report,
    publish_to_mock_catalog
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="MCP Dataset Onboarding Server",
    description="FastAPI-based MCP server for automating dataset onboarding with Google Drive integration",
    version="1.0.0"
)

# Pydantic models
class FileMetadataRequest(BaseModel):
    file_id: str

class DQRulesRequest(BaseModel):
    metadata: Dict[str, Any]

class ContractUpdateRequest(BaseModel):
    metadata: Dict[str, Any]
    dq_rules: List[Dict[str, Any]]

class PublishRequest(BaseModel):
    metadata: Dict[str, Any]
    contract_file_id: str
    dq_report: Dict[str, Any]

class ProcessDatasetRequest(BaseModel):
    file_id: str


@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "message": "MCP Dataset Onboarding Server",
        "version": "1.0.0",
        "endpoints": [
            "/tool/extract_metadata",
            "/tool/apply_dq_rules", 
            "/tool/update_contract",
            "/tool/publish_to_catalog",
            "/tool/list_catalog",
            "/process_dataset"
        ]
    }


@app.post("/tool/extract_metadata")
async def extract_metadata(request: FileMetadataRequest):
    """Extract metadata from CSV/Excel file in MCP_server folder."""
    try:
        drive_service = get_drive_service()
        
        # Download file from Google Drive
        file_content = download_file_from_drive(request.file_id, drive_service)
        
        # Get file info to determine type
        file_info = drive_service.files().get(fileId=request.file_id).execute()
        filename = file_info['name']
        
        # Read file based on extension
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        elif filename.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(file_content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Only CSV and Excel files are supported.")
        
        # Extract metadata
        metadata = extract_metadata_from_dataframe(df, filename)
        
        return {
            "status": "success",
            "metadata": metadata,
            "message": f"Successfully extracted metadata from {filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract metadata: {str(e)}")


@app.post("/tool/apply_dq_rules")
async def apply_dq_rules(request: DQRulesRequest):
    """Suggest data quality rules based on metadata."""
    try:
        dq_rules = suggest_dq_rules(request.metadata)
        
        return {
            "status": "success",
            "dq_rules": dq_rules,
            "total_rules": len(dq_rules),
            "message": f"Generated {len(dq_rules)} data quality rules"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate DQ rules: {str(e)}")


@app.post("/tool/update_contract")
async def update_contract(request: ContractUpdateRequest):
    """Create/update contract Excel file with schema and DQ information."""
    try:
        drive_service = get_drive_service()
        
        # Create temporary file for contract
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            contract_path = tmp_file.name
        
        # Create contract Excel file
        create_contract_excel(request.metadata, request.dq_rules, contract_path)
        
        # Upload to MCP_server folder (temporary storage)
        server_folder_id = os.getenv('MCP_SERVER_FOLDER_ID')
        contract_filename = f"{request.metadata['filename']}_contract.xlsx"
        
        file_id = upload_to_drive_file(contract_path, drive_service, server_folder_id)
        
        # Clean up temporary file
        os.unlink(contract_path)
        
        return {
            "status": "success",
            "contract_file_id": file_id,
            "filename": contract_filename,
            "message": "Contract file created and uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update contract: {str(e)}")


@app.post("/tool/publish_to_catalog")
async def publish_to_catalog(request: PublishRequest):
    """Upload metadata, contract, and DQ report to MCP_client catalog folder."""
    try:
        drive_service = get_drive_service()
        catalog_folder_id = os.getenv('MCP_CLIENT_FOLDER_ID')
        
        # Create temporary contract file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            contract_path = tmp_file.name
        
        # Download contract file from drive and save locally
        contract_content = download_file_from_drive(request.contract_file_id, drive_service)
        with open(contract_path, 'wb') as f:
            f.write(contract_content)
        
        # Publish all artifacts to catalog
        uploaded_files = publish_to_mock_catalog(
            request.metadata,
            contract_path,
            request.dq_report,
            drive_service,
            catalog_folder_id
        )
        
        # Clean up temporary file
        os.unlink(contract_path)
        
        return {
            "status": "success",
            "uploaded_files": uploaded_files,
            "message": "Successfully published all artifacts to catalog"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish to catalog: {str(e)}")


@app.get("/tool/list_catalog")
async def list_catalog():
    """List all files in the MCP_client catalog folder."""
    try:
        drive_service = get_drive_service()
        catalog_folder_id = os.getenv('MCP_CLIENT_FOLDER_ID')
        
        files = list_files_in_folder(drive_service, catalog_folder_id)
        
        return {
            "status": "success",
            "files": files,
            "total_files": len(files),
            "message": f"Found {len(files)} files in catalog"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list catalog: {str(e)}")


@app.post("/process_dataset")
async def process_dataset(request: ProcessDatasetRequest):
    """Complete workflow: extract metadata, apply DQ rules, create contract, and publish to catalog."""
    try:
        # Step 1: Extract metadata
        print(f"Step 1: Extracting metadata for file {request.file_id}")
        metadata_response = await extract_metadata(FileMetadataRequest(file_id=request.file_id))
        metadata = metadata_response["metadata"]
        print(f"[OK] Metadata extracted for {metadata['filename']}")
        
        # Step 2: Apply DQ rules
        print("Step 2: Applying DQ rules")
        dq_response = await apply_dq_rules(DQRulesRequest(metadata=metadata))
        dq_rules = dq_response["dq_rules"]
        print(f"[OK] Generated {len(dq_rules)} DQ rules")
        
        # Step 3: Update contract
        print("Step 3: Creating contract")
        contract_response = await update_contract(ContractUpdateRequest(
            metadata=metadata,
            dq_rules=dq_rules
        ))
        contract_file_id = contract_response["contract_file_id"]
        print(f"[OK] Contract created with ID {contract_file_id}")
        
        # Step 4: Generate DQ report
        print("Step 4: Generating DQ report")
        dq_report = generate_dq_report(metadata, dq_rules)
        print("[OK] DQ report generated")
        
        # Step 5: Publishing to catalog
        print("Step 5: Publishing to catalog")
        publish_response = await publish_to_catalog(PublishRequest(
            metadata=metadata,
            contract_file_id=contract_file_id,
            dq_report=dq_report
        ))
        print("[OK] Published to catalog successfully")
        
        return {
            "status": "success",
            "workflow_results": {
                "metadata_extracted": True,
                "dq_rules_applied": len(dq_rules),
                "contract_created": contract_file_id,
                "published_files": publish_response["uploaded_files"]
            },
            "message": f"Successfully processed dataset {metadata['filename']} through complete workflow"
        }
        
    except HTTPException as he:
        print(f"HTTP Exception in process_dataset: {he.detail}")
        raise he
    except Exception as e:
        print(f"Exception in process_dataset: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process dataset: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test Google Drive connection
        drive_service = get_drive_service()
        
        # Verify folder IDs are accessible
        server_folder_id = os.getenv('MCP_SERVER_FOLDER_ID')
        client_folder_id = os.getenv('MCP_CLIENT_FOLDER_ID')
        
        if not server_folder_id or not client_folder_id:
            raise Exception("Missing folder IDs in environment variables")
        
        # Test access to folders
        drive_service.files().get(fileId=server_folder_id).execute()
        drive_service.files().get(fileId=client_folder_id).execute()
        
        return {
            "status": "healthy",
            "google_drive": "connected",
            "folders": {
                "server_folder": server_folder_id,
                "client_folder": client_folder_id
            }
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)