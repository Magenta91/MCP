# 🔒 Security Setup Guide

## ⚠️ **IMPORTANT: Before Using This System**

This repository contains template files with placeholder values. You **MUST** configure your own credentials and IDs before the system will work.

## 🔐 **Required Security Setup**

### **Step 1: Google Service Account Key**

1. **Download your service account key** from Google Cloud Console
2. **Save it securely** outside this repository (e.g., `~/keys/` or `C:\keys\`)
3. **Never commit the key file** to version control

### **Step 2: Update Environment Variables**

Create your own `.env` file with real values:

```bash
# Copy the template
cp .env.template .env

# Edit with your actual values
nano .env
```

**Required values:**
```env
# Path to your service account JSON key file
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/path/to/your/service-account-key.json

# Your actual Google Drive folder IDs
MCP_SERVER_FOLDER_ID=your_actual_server_folder_id
MCP_CLIENT_FOLDER_ID=your_actual_client_folder_id
```

### **Step 3: Update MCP Configuration**

Edit `mcp_config.json` with your actual paths and IDs:

```json
{
  "mcpServers": {
    "dataset-onboarding": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/full/path/to/this/directory",
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/path/to/your/service-account-key.json",
        "MCP_SERVER_FOLDER_ID": "your_actual_server_folder_id",
        "MCP_CLIENT_FOLDER_ID": "your_actual_client_folder_id"
      }
    }
  }
}
```

## 🛡️ **Security Best Practices**

### **✅ DO:**
- Store service account keys outside the repository
- Use environment variables for sensitive data
- Regularly rotate service account keys
- Use minimal required permissions
- Keep `.env` files in `.gitignore`

### **❌ DON'T:**
- Commit service account keys to version control
- Share credentials in plain text
- Use overly permissive service account roles
- Store sensitive data in code files

## 🔍 **Verify Security**

Before committing to GitHub, check:

```bash
# Ensure no sensitive files will be committed
git status

# Check what would be committed
git add . --dry-run

# Verify .gitignore is working
git check-ignore *.json
git check-ignore .env
```

## 🚨 **If You Accidentally Commit Secrets**

If you accidentally commit sensitive information:

1. **Immediately revoke** the compromised credentials
2. **Remove from Git history**:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch sensitive-file.json' \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push** to overwrite history:
   ```bash
   git push origin --force --all
   ```
4. **Generate new credentials**

## 📋 **Security Checklist**

Before going public:

- [ ] Service account key file removed from repository
- [ ] `.env` file contains only template values
- [ ] `mcp_config.json` contains only template values
- [ ] `.gitignore` includes all sensitive file patterns
- [ ] No hardcoded credentials in any `.py` files
- [ ] All folder IDs replaced with placeholders
- [ ] Security documentation is complete

## 🔧 **Local Development**

For local development, create a `local.env` file (also gitignored):

```bash
# Copy your real environment
cp .env local.env

# Use in development
export $(cat local.env | xargs)
python main.py
```

## 🌐 **Production Deployment**

For production:

1. Use environment variables or secret management systems
2. Never store credentials in container images
3. Use IAM roles instead of service account keys when possible
4. Implement proper access logging and monitoring

## 📞 **Support**

If you need help with security setup:
1. Check the main README.md for setup instructions
2. Review Google Cloud documentation for service accounts
3. Ensure your Google Drive folders have proper sharing permissions

Remember: **Security is not optional!** 🔒