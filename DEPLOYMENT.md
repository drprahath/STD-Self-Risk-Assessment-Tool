# STD Risk Assessment App - Deployment & Running Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Performance Tips](#performance-tips)

---

## Quick Start

### For Immediate Launch (Assuming Python & Dependencies Already Installed)

```bash
cd path/to/app/directory
streamlit run std_risk_assessment_app.py
```

App will open at: `http://localhost:8501`

---

## Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
```

Required: Python 3.8 or higher

If Python is not installed:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas numpy
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
```

---

## Running the Application

### Basic Launch

```bash
streamlit run std_risk_assessment_app.py
```

### Advanced Options

**Run on Custom Port:**
```bash
streamlit run std_risk_assessment_app.py --server.port 8502
```

**Run in Development Mode:**
```bash
streamlit run std_risk_assessment_app.py --logger.level=debug
```

**Run Headless (No Browser Launch):**
```bash
streamlit run std_risk_assessment_app.py --server.headless true
```

**Full Custom Configuration:**
```bash
streamlit run std_risk_assessment_app.py \
  --server.port 8502 \
  --server.address 0.0.0.0 \
  --logger.level debug \
  --client.showErrorDetails true
```

---

## Configuration

### Default Settings (In Application)

Located in `std_risk_assessment_app.py`:
- Theme: Light mode
- Storage: Local JSON file
- Port: 8501
- Browser: Auto-opens on launch

### Customize via Streamlit Config

Create `.streamlit/config.toml` in the app directory:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
runOnSave = true
enableXsrfProtection = true

[client]
showErrorDetails = false
toolbarMode = "viewer"
```

---

## Troubleshooting

### Issue 1: "Command 'streamlit' not found"

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install streamlit
pip install streamlit
```

### Issue 2: "Port 8501 already in use"

**Solution:**
```bash
# Option 1: Use different port
streamlit run std_risk_assessment_app.py --server.port 8502

# Option 2: Kill process on port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8501
kill -9 <PID>
```

### Issue 3: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue 4: App crashes on startup

**Solution:**
```bash
# Check Python version
python --version

# Verify file integrity
python -m py_compile std_risk_assessment_app.py

# Run in debug mode
streamlit run std_risk_assessment_app.py --logger.level=debug
```

### Issue 5: Records not saving

**Solution:**
1. Check directory permissions: `ls -la` (macOS/Linux) or check Properties (Windows)
2. Ensure disk space available
3. Delete `patient_records.json` and restart
4. Check if .gitignore is blocking the file

### Issue 6: Browser won't open automatically

**Solution:**
1. Manually navigate to `http://localhost:8501`
2. Check firewall settings
3. Run with: `streamlit run std_risk_assessment_app.py --server.headless false`

---

## Performance Tips

### Optimize Startup Speed

1. **Use Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Reduce Initial Load**
   - Comment out debug features if not needed
   - Close unnecessary browser tabs
   - Ensure sufficient RAM (512 MB minimum)

### Optimize Runtime Performance

1. **Enable Session State Caching**
   Already implemented in the app via `@st.cache_data`

2. **Monitor Memory Usage**
   ```bash
   # Windows: Check Task Manager
   # macOS/Linux:
   top -p <PID>
   ```

3. **Clear Cache if Slow**
   ```bash
   rm -rf .streamlit/cache  # macOS/Linux
   rmdir .streamlit\cache   # Windows
   ```

### Optimize Data Storage

1. **Archive Old Records**
   - Export and backup `patient_records.json` regularly
   - Keep active records under 1000 entries
   - Delete old records from View Records tab

2. **Backup Strategy**
   ```bash
   # Create backup
   cp patient_records.json patient_records_backup_$(date +%Y%m%d).json
   ```

---

## Deployment Options

### Option 1: Local Machine (Recommended for Testing)

```bash
streamlit run std_risk_assessment_app.py
```

- Simplest setup
- Full control
- Local data storage
- Single user

### Option 2: Private Network

```bash
streamlit run std_risk_assessment_app.py --server.address 192.168.1.100
```

- Multiple users on network
- Access via `http://192.168.1.100:8501`
- Share with team/colleagues

### Option 3: Docker Container

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY std_risk_assessment_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "std_risk_assessment_app.py"]
```

Build and run:
```bash
docker build -t std-risk-app .
docker run -p 8501:8501 std-risk-app
```

### Option 4: Cloud Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy from repository
4. App runs at: `https://yourname-std-risk-app.streamlit.app`

---

## Security Considerations

⚠️ **Important for Production Deployment**

1. **Data Encryption**
   - Patient data stored in local JSON (plain text by default)
   - Encrypt `patient_records.json` for sensitive deployments
   - Consider database with encryption

2. **Access Control**
   - Currently no authentication
   - Add login/password for production
   - Use HTTPS for remote access

3. **HIPAA Compliance** (if handling real patient data)
   - Implement proper authentication
   - Use encrypted database
   - Audit logging
   - Consider certified healthcare platforms

### Simple Authentication Addition

Add to top of `std_risk_assessment_app.py`:

```python
import streamlit as st

# Simple password protection
def check_password():
    if "password_ok" not in st.session_state:
        st.session_state.password_ok = False
    
    if not st.session_state.password_ok:
        password = st.text_input("Enter password:", type="password")
        if password == "your_password_here":  # Change this!
            st.session_state.password_ok = True
            st.rerun()
        else:
            st.error("Incorrect password")
            return False
    return True

if not check_password():
    st.stop()

# Rest of app continues here...
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor app performance
- Check for error logs

**Weekly:**
- Backup `patient_records.json`
- Review assessment trends
- Check disk space

**Monthly:**
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review and archive old records
- Performance optimization

### Backup Strategy

```bash
# Automatic backup script (Linux/macOS)
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp patient_records.json backups/patient_records_$TIMESTAMP.json
```

---

## Getting Help

### Common Resources

1. **Streamlit Documentation**: https://docs.streamlit.io
2. **Streamlit Community**: https://discuss.streamlit.io
3. **Python Documentation**: https://docs.python.org
4. **GitHub Issues**: Check repository issues

### Enable Debug Logging

```bash
streamlit run std_risk_assessment_app.py --logger.level=debug 2>&1 | tee app.log
```

---

## Testing the Application

### Test Checklist

- [ ] App launches without errors
- [ ] All pages load correctly
- [ ] Assessment form submits successfully
- [ ] Risk score calculates correctly
- [ ] Recommendations display properly
- [ ] Records save to file
- [ ] STD info page displays all STIs
- [ ] Records can be viewed and deleted
- [ ] No browser console errors
- [ ] Responsive on different screen sizes

### Manual Testing Steps

1. Launch app
2. Go through each navigation item
3. Complete a full assessment
4. Verify results display
5. Check patient_records.json file created
6. Complete another assessment
7. Verify records appear in View Records
8. Test delete function
9. Verify recommendations match risk score

---

## Version & Support

**App Version:** 1.0
**Last Updated:** November 2024
**Python Versions Supported:** 3.8, 3.9, 3.10, 3.11, 3.12

**For Issues or Improvements:**
Contact your development team or create an issue in the repository.

---

**Ready to launch? Run: `streamlit run std_risk_assessment_app.py`**
