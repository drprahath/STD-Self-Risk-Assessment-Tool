# 🚀 Streamlit Cloud Deployment Guide

## Complete Step-by-Step Deployment Instructions

### 📋 Prerequisites
- GitHub account (free at github.com)
- Streamlit account (free at share.streamlit.io - sign up with GitHub)
- Your app files ready

### ✅ Step 1: Create a GitHub Repository

1. **Go to GitHub.com** and sign in with your account
2. **Click "+"** in the top right corner → **"New repository"**
3. **Enter repository details:**
   - Repository name: `std-risk-assessment-app`
   - Description: "STD Self-Risk Assessment Tool"
   - Make it **Public** (required for free Streamlit Cloud deployment)
   - ✅ Check "Add a README file"
   - Add .gitignore: **Python**
4. **Click "Create repository"**

---

### ✅ Step 2: Upload Your Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. **Go to your new repository** on GitHub
2. **Click "Add file"** → **"Upload files"**
3. **Upload these files:**
   - `std_risk_assessment_app.py` (main app)
   - `requirements.txt` (dependencies)
   - `config.json` (configuration)
   - `README.md` (documentation)
   - `.gitignore` (ignore unnecessary files)

4. **Add commit message:** "Initial commit: STD Risk Assessment App"
5. **Click "Commit changes"**

**Option B: Using Git Command Line**

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/std-risk-assessment-app.git
cd std-risk-assessment-app

# Copy your app files to this directory
# Then run these commands:

git add std_risk_assessment_app.py requirements.txt config.json README.md
git commit -m "Initial commit: STD Risk Assessment App"
git push origin main
```

---

### ✅ Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:** https://share.streamlit.io/
2. **Sign up/Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the deployment form:**
   - **Repository:** YOUR_USERNAME/std-risk-assessment-app
   - **Branch:** main
   - **Main file path:** `std_risk_assessment_app.py`
5. **Click "Deploy!"**

**The deployment will take 2-3 minutes**

---

### 🎉 Step 4: Your App is Live!

Streamlit will generate a URL like:
```
https://std-risk-assessment-app.streamlit.app
```

Your app is now **publicly accessible** from anywhere in the world!

---

## 📊 File Structure Required

Your GitHub repository should have:

```
std-risk-assessment-app/
├── std_risk_assessment_app.py    (main application)
├── requirements.txt               (Python dependencies)
├── config.json                   (configuration file)
├── README.md                     (documentation)
└── .gitignore                    (files to ignore)
```

---

## 🔧 Additional Configuration

### Setting up Secrets (if needed)

For sensitive data, use Streamlit secrets:

1. **In your Streamlit Cloud app:**
   - Click "⋮" (menu) → **Settings**
   - Go to **Secrets**
   - Add your secrets in TOML format:
   ```toml
   api_key = "your-secret-key"
   database_url = "your-database-url"
   ```

2. **In your app code:**
   ```python
   import streamlit as st
   secret = st.secrets["api_key"]
   ```

---

## 📝 requirements.txt Format

Ensure your `requirements.txt` is properly formatted:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.25.0
```

---

## 🔍 Troubleshooting Deployment

### App won't start
- Check `requirements.txt` for correct package names
- Ensure `std_risk_assessment_app.py` is in root directory
- Check Streamlit Cloud logs for error messages

### Missing dependencies
- Update `requirements.txt` with all required packages
- Commit and push changes to GitHub
- Redeploy (Streamlit auto-updates on push)

### File not found errors
- Verify all files are in the root directory
- Check file names match exactly (case-sensitive on Linux)
- Ensure relative paths work correctly

---

## 📱 Sharing Your App

Once deployed, you can:

1. **Share the direct URL:**
   ```
   https://std-risk-assessment-app.streamlit.app
   ```

2. **Embed in a website:**
   ```html
   <iframe src="https://std-risk-assessment-app.streamlit.app" 
           width="100%" height="600"></iframe>
   ```

3. **Create a QR code** pointing to your deployed URL

---

## 🔄 Updates and Redeployment

Any changes are **automatic**:
1. Update your code locally
2. Commit to GitHub: `git push origin main`
3. Streamlit automatically redeploys your app
4. Changes live within 2-3 minutes

---

## 📊 Monitoring Your App

On Streamlit Cloud:
- View analytics and usage statistics
- Monitor app health
- Check logs for errors
- Manage app settings

---

## 💡 Pro Tips

- **Faster deployment:** Push only necessary files using `.gitignore`
- **Better performance:** Optimize data loading with caching
- **Custom domain:** Upgrade for custom domain support
- **Private repos:** Upgrade to Streamlit Cloud Pro for private repositories

---

## 🆘 Need Help?

- **Streamlit Docs:** https://docs.streamlit.io
- **Deployment Docs:** https://docs.streamlit.io/deploy/streamlit-cloud
- **GitHub Issues:** Check repository issues
- **Streamlit Community:** https://discuss.streamlit.io

---

## ✨ What's Deployed

Your deployed app includes:
- ✅ STD Risk Assessment questionnaire
- ✅ Patient data management
- ✅ Risk scoring (0-18 points)
- ✅ Personalized recommendations
- ✅ STI information database (7 diseases)
- ✅ Medical disclaimer
- ✅ Complete user interface

**Your app is ready to help patients assess their STI risk!** 🎉
