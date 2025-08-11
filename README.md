# 🤖 MCP Dataset Onboarding Server

A FastAPI-based MCP (Model-Compatible Protocol) server for automating dataset onboarding using Google Drive as both input source and mock catalog.

## 🔒 **SECURITY FIRST - READ THIS BEFORE SETUP**

⚠️ **This repository contains template files only. You MUST configure your own credentials before use.**

📖 **Read [SECURITY_SETUP.md](SECURITY_SETUP.md) for complete security instructions.**

🚨 **Never commit service account keys or real folder IDs to version control!**

## Features

- **Automated Dataset Processing**: Complete workflow from raw CSV/Excel files to cataloged datasets
- **Google Drive Integration**: Uses Google Drive folders as input source and catalog storage
- **Metadata Extraction**: Automatically extracts column information, data types, and basic statistics
- **Data Quality Rules**: Suggests DQ rules based on data characteristics
- **Contract Generation**: Creates Excel contracts with schema and DQ information
- **Mock Catalog**: Publishes processed artifacts to a catalog folder
- **🤖 Automated Processing**: Watches folders and processes files automatically
- **🌐 Multiple Interfaces**: FastAPI server, MCP server, CLI tools, and dashboards

## Project Structure

```
├── main.py                    # FastAPI server and endpoints
├── mcp_server.py             # True MCP protocol server for LLM integration
├── utils.py                   # Google Drive helpers and DQ functions
├── dataset_processor.py       # Centralized dataset processing logic
├── auto_processor.py         # 🤖 Automated file monitoring
├── start_auto_processor.py   # 🚀 Easy startup for auto-processor
├── processor_dashboard.py    # 📊 Monitoring dashboard
├── dataset_manager.py        # CLI tool for managing datasets
├── local_test.py             # Local processing script
├── auto_config.py           # ⚙️ Configuration management
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── .env.template            # Environment variables template
├── .gitignore               # Security: excludes sensitive files
├── SECURITY_SETUP.md        # 🔒 Security configuration guide
├── processed_datasets/      # Organized output folder
│   └── [dataset_name]/      # Individual dataset folders
│       ├── [dataset].csv    # Original dataset
│       ├── [dataset]_metadata.json
│       ├── [dataset]_contract.xlsx
│       ├── [dataset]_dq_report.json
│       └── README.md        # Dataset summary
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Security Setup (REQUIRED)

```bash
# 1. Read the security guide
cat SECURITY_SETUP.md

# 2. Set up your Google service account (outside this repo)
# 3. Configure your environment variables
cp .env.template .env
# Edit .env with your actual values

# 4. Verify no sensitive files will be committed
git status
```

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Test the setup
python local_test.py
```

### 3. Choose Your Interface

#### 🤖 Fully Automated (Recommended)
```bash
# Start auto-processor - upload files and walk away!
python start_auto_processor.py
```

#### 🌐 API Server
```bash
# Start FastAPI server
python main.py
```

#### 🧠 LLM Integration (MCP)
```bash
# Start MCP server for Claude Desktop, etc.
python mcp_server.py
```

#### 🖥️ Command Line
```bash
# Manual dataset management
python dataset_manager.py list
python dataset_manager.py process YOUR_FILE_ID
```

## 🎯 Usage Scenarios

### Scenario 1: Set-and-Forget Automation
1. `python start_auto_processor.py`
2. Upload files to Google Drive
3. Files processed automatically within 30 seconds
4. Monitor with `python processor_dashboard.py --live`

### Scenario 2: LLM-Powered Data Analysis
1. Configure MCP server in Claude Desktop
2. Chat: "Analyze the dataset I just uploaded"
3. Claude uses MCP tools to process and explain your data

### Scenario 3: API Integration
1. `python main.py`
2. Integrate with your data pipelines via REST API
3. Programmatic dataset onboarding

## 📊 What You Get

For each processed dataset:
- **📄 Original File**: Preserved in organized folder
- **📋 Metadata JSON**: Column info, types, statistics
- **📊 Excel Contract**: Professional multi-sheet contract
- **🔍 Quality Report**: Data quality assessment
- **📖 README**: Human-readable summary

## 🛠️ Available Tools

### FastAPI Endpoints
- `/tool/extract_metadata` - Analyze dataset structure
- `/tool/apply_dq_rules` - Generate quality rules
- `/process_dataset` - Complete workflow
- `/health` - System health check

### MCP Tools (for LLMs)
- `extract_dataset_metadata` - Dataset analysis
- `generate_data_quality_rules` - Quality assessment
- `process_complete_dataset` - Full pipeline
- `list_catalog_files` - Catalog browsing

### CLI Commands
- `dataset_manager.py list` - Show processed datasets
- `auto_processor.py --once` - Single check cycle
- `processor_dashboard.py --live` - Real-time monitoring

## 🔧 Configuration

### Environment Variables (.env)
```env
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=path/to/your/key.json
MCP_SERVER_FOLDER_ID=your_input_folder_id
MCP_CLIENT_FOLDER_ID=your_output_folder_id
```

### Auto-Processor Settings (auto_config.py)
- Check interval: 30 seconds
- Supported formats: CSV, Excel
- File age threshold: 1 minute
- Max files per cycle: 5

## 📈 Monitoring & Analytics

```bash
# Current status
python processor_dashboard.py

# Live monitoring (auto-refresh)
python processor_dashboard.py --live

# Detailed statistics
python processor_dashboard.py --stats

# Processing history
python auto_processor.py --list
```

## 🐳 Docker Deployment

```bash
# Build
docker build -t mcp-dataset-server .

# Run (mount your service account key securely)
docker run -p 8000:8000 \
  -v /secure/path/to/key.json:/app/keys/key.json \
  -e GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/app/keys/key.json \
  -e MCP_SERVER_FOLDER_ID=your_folder_id \
  mcp-dataset-server
```

## 🔍 Troubleshooting

### Common Issues
- **No files detected**: Check Google Drive permissions
- **Processing errors**: Verify service account access
- **MCP not working**: Check Claude Desktop configuration

### Debug Commands
```bash
# Test Google Drive connection
python -c "from utils import get_drive_service; print('✅ Connected')"

# Check auto-processor status
python auto_processor.py --once

# Verify MCP server
python test_mcp_server.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. **Never commit sensitive data**
4. Test your changes
5. Submit a pull request

## 📚 Documentation

- [SECURITY_SETUP.md](SECURITY_SETUP.md) - Security configuration
- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - Automation features
- [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) - LLM integration

## 📄 License

MIT License

## 🎉 What Makes This Special

- **🔒 Security First**: Proper credential management
- **🤖 True Automation**: Zero manual intervention
- **🧠 LLM Integration**: Natural language data processing
- **📊 Professional Output**: Enterprise-ready documentation
- **🔧 Multiple Interfaces**: API, CLI, MCP, Dashboard
- **📈 Real-time Monitoring**: Live processing status
- **🗂️ Perfect Organization**: Structured output folders

Transform your messy data files into professional, documented, quality-checked datasets automatically! 🚀