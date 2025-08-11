# 🤖 MCP Auto Dataset Processor - Complete Guide

## 🎯 **What We Built**

You now have a **fully automated dataset onboarding system** that watches your Google Drive folder and processes new files automatically - no manual file IDs needed!

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Start the Auto-Processor**
```bash
python start_auto_processor.py
```

### **Step 2: Upload Files**
- Upload any CSV or Excel file to your `MCP_server` Google Drive folder
- That's it! No file IDs, no manual commands

### **Step 3: Watch the Magic**
- Files are automatically detected within 30 seconds
- Complete processing pipeline runs automatically
- All artifacts saved in organized folders

## 📊 **Monitoring & Management**

### **Real-Time Dashboard**
```bash
# View current status
python processor_dashboard.py

# Live monitoring (auto-refreshing)
python processor_dashboard.py --live

# Detailed analytics
python processor_dashboard.py --stats
```

### **Manual Controls**
```bash
# Run single check
python auto_processor.py --once

# List processed files
python auto_processor.py --list

# Custom check interval
python auto_processor.py --interval 60

# Reset processed files log
python auto_processor.py --reset
```

## 🔧 **How It Works**

### **Intelligent File Detection**
- ✅ Monitors Google Drive folder continuously
- ✅ Only processes supported formats (CSV, Excel)
- ✅ Ignores already processed files
- ✅ Waits for upload completion before processing
- ✅ Handles multiple files efficiently

### **Automatic Processing Pipeline**
1. **File Detection** → New file uploaded to Google Drive
2. **Download** → File retrieved automatically
3. **Analysis** → Metadata extraction and statistics
4. **Quality Rules** → Intelligent DQ rule generation
5. **Documentation** → Excel contracts and reports
6. **Organization** → Structured folder creation
7. **Tracking** → Processing log updated

### **Smart Features**
- **Duplicate Prevention**: Won't process the same file twice
- **Error Recovery**: Handles failures gracefully
- **Batch Processing**: Can handle multiple files at once
- **Progress Tracking**: Maintains detailed logs
- **Resource Efficient**: Minimal system impact

## 📁 **Output Structure**

Each processed dataset gets its own organized folder:
```
processed_datasets/
└── your_dataset_name/
    ├── original_file.csv          # Original dataset
    ├── dataset_metadata.json      # Column info & stats
    ├── dataset_contract.xlsx      # Professional contract
    ├── dataset_dq_report.json     # Quality assessment
    └── README.md                  # Human-readable summary
```

## 🎛️ **Configuration**

### **Default Settings**
- **Check Interval**: 30 seconds
- **File Age Threshold**: 1 minute (prevents processing during upload)
- **Supported Formats**: CSV, Excel (.xlsx, .xls)
- **Max Files Per Cycle**: 5

### **Customization**
Edit `auto_config.py` to adjust:
- Check frequency
- File age requirements
- Supported formats
- Logging levels
- Output folders

## 🔍 **Troubleshooting**

### **No Files Being Processed?**
1. Check Google Drive folder permissions
2. Verify service account has access
3. Ensure files are supported formats
4. Check `processed_files.json` for duplicates

### **Processing Errors?**
1. Check Google Drive connectivity
2. Verify file formats are valid
3. Check disk space for output folders
4. Review error logs in console

### **Dashboard Not Showing Data?**
1. Ensure `processed_files.json` exists
2. Check Google Drive API access
3. Verify folder IDs in `.env` file

## 🎉 **Benefits**

### **Before (Manual)**
- ❌ Find file ID manually
- ❌ Run commands for each file
- ❌ Track processed files yourself
- ❌ Organize outputs manually
- ❌ Monitor progress constantly

### **After (Automated)**
- ✅ Just upload files to Google Drive
- ✅ Everything happens automatically
- ✅ Smart duplicate detection
- ✅ Organized output structure
- ✅ Real-time monitoring dashboard

## 🚀 **Production Deployment**

### **Run as Service (Linux)**
```bash
# Create systemd service
sudo nano /etc/systemd/system/mcp-auto-processor.service

[Unit]
Description=MCP Auto Dataset Processor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/mcp
ExecStart=/usr/bin/python3 start_auto_processor.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable mcp-auto-processor
sudo systemctl start mcp-auto-processor
```

### **Run as Service (Windows)**
Use Task Scheduler or Windows Service Wrapper to run `start_auto_processor.py` automatically.

### **Docker Deployment**
```bash
# Build image
docker build -t mcp-auto-processor .

# Run with auto-processor
docker run -d \
  -v /path/to/service-account.json:/app/keys/service-account.json \
  -v /path/to/processed_datasets:/app/processed_datasets \
  -e GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/app/keys/service-account.json \
  -e MCP_SERVER_FOLDER_ID=your_server_folder_id \
  -e MCP_CLIENT_FOLDER_ID=your_client_folder_id \
  mcp-auto-processor python start_auto_processor.py
```

## 🎯 **Use Cases**

### **Data Teams**
- Automatic ingestion of daily reports
- Continuous data quality monitoring
- Self-service data onboarding

### **Business Users**
- Upload spreadsheets for instant analysis
- Automated documentation generation
- Quality-checked data delivery

### **Data Engineers**
- Hands-off data pipeline integration
- Automated metadata cataloging
- Quality rule enforcement

## 🏆 **You Now Have**

A **production-ready, fully automated dataset onboarding system** that:
- ✅ Requires zero manual intervention
- ✅ Processes files within 30 seconds of upload
- ✅ Generates professional documentation
- ✅ Maintains organized data catalogs
- ✅ Provides real-time monitoring
- ✅ Scales to handle multiple files
- ✅ Recovers from errors gracefully

**Just upload files to Google Drive and walk away!** 🚀