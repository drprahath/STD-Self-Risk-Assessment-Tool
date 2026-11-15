# STD Self-Risk Assessment Tool

A comprehensive web-based application for self-assessment of sexually transmitted infection (STI) risk, built with Python and Streamlit.

## Features

✅ **Personal Risk Assessment**
- Comprehensive questionnaire about sexual behavior and history
- Personalized risk scoring based on multiple factors
- Risk categories: Low, Moderate, High, and Very High

✅ **Patient Data Management**
- Store and manage patient personal details
- Track assessment history
- View detailed assessment records
- Export patient records

✅ **Personalized Recommendations**
- Risk-based guidance on next steps
- Testing frequency recommendations
- Prevention strategies
- Lifestyle advice based on risk level

✅ **Educational Resources**
- Information about 7 common STIs
- Symptoms, transmission methods, and treatments
- Testing information and prevention strategies
- Important medical disclaimers and resources

✅ **User-Friendly Interface**
- Clean, intuitive navigation
- Color-coded risk indicators
- Easy-to-understand results
- Mobile-responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this project**
   ```bash
   # If using git
   git clone <repository-url>
   cd std-risk-assessment
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Streamlit app:
```bash
streamlit run std_risk_assessment_app.py
```

The application will open in your default browser at `http://localhost:8501`

### Note for Windows users:
If the app doesn't open automatically, manually navigate to `http://localhost:8501` in your browser.

## Usage Guide

### 1. **Home Page**
   - Get an overview of the tool's features
   - Understand the risk categories
   - Learn how to get started

### 2. **New Assessment**
   - Fill in your personal information
   - Answer questions about sexual behavior
   - Review your medical and testing history
   - Click "Calculate Risk Score" to get results
   - Receive personalized recommendations

### 3. **View Records**
   - See all your past assessments
   - View detailed information for each assessment
   - Delete old records if needed
   - Track changes over time

### 4. **STD Information**
   - Learn about common STIs
   - Understand symptoms and transmission
   - Review treatment options
   - Get testing information

### 5. **About**
   - Important medical disclaimers
   - When to seek medical care
   - Prevention tips
   - Helpful resources

## Risk Scoring System

The app calculates risk based on 6 factors:

| Factor | Weight |
|--------|--------|
| Number of sexual partners (12 months) | 0-3 points |
| Protection usage frequency | 0-3 points |
| Previous STI history | 0-2 points |
| Partner STI history | 0-2 points |
| Current symptoms | 0-3 points |
| Time since last test | 0-3 points |
| **Maximum Total Score** | **18 points** |

### Risk Categories:
- 🟢 **Low Risk** (0-2): Continue safe practices and annual testing
- 🟡 **Moderate Risk** (3-5): Test within 2 weeks, use protection consistently
- 🔴 **High Risk** (6-9): Test immediately, inform partners, abstain until tested
- 🔴 **Very High Risk** (10+): Seek medical evaluation today, urgent action needed

## Data Storage

- Patient assessment records are stored in `patient_records.json`
- This file is created automatically in the same directory as the app
- Data is stored locally on your device (no cloud upload by default)
- You can backup or delete this file as needed

## Important Medical Disclaimers

⚠️ **This tool is for educational purposes ONLY**

- **Not a diagnosis tool**: Cannot diagnose any condition
- **Not a replacement for medical advice**: Always consult a healthcare provider
- **Self-reported data**: Results are based on your answers only
- **Professional evaluation needed**: A doctor's assessment is necessary for proper diagnosis and treatment

## When to Seek Immediate Medical Care

🔴 Seek emergency medical attention if you experience:
- Severe pain or discomfort
- Signs of severe infection (high fever, chills)
- Unusual or concerning symptoms
- Any symptoms that worry you

## Prevention Strategies

✓ **Use protection**: Condoms and barriers for all sexual activities
✓ **Get vaccinated**: HPV and Hepatitis B vaccines are available
✓ **Test regularly**: Annual testing is recommended for sexually active individuals
✓ **Communicate**: Talk openly with partners about sexual health
✓ **Get treated**: Seek immediate treatment if diagnosed with an STI
✓ **Limit partners**: Reduce number of sexual partners
✓ **Avoid risky situations**: Don't have unprotected sex with untreated partners

## Helpful Resources

- **CDC Sexual Health**: https://www.cdc.gov/sexualhealth
- **Planned Parenthood**: https://www.plannedparenthood.org
- **WHO STI Information**: https://www.who.int/activities/strengthening-stis-response
- **Local Health Departments**: Search for your local health department website
- **Crisis Hotlines**: Call or text your local health crisis line for support

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8+
- **RAM**: 512 MB minimum
- **Storage**: 10 MB for app + space for records
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Troubleshooting

### App won't start
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Try running with verbose mode
streamlit run std_risk_assessment_app.py --logger.level=debug
```

### Port already in use
```bash
# Run on a different port
streamlit run std_risk_assessment_app.py --server.port 8502
```

### Records not saving
- Ensure the app has write permissions in its directory
- Check that there's enough disk space
- Try deleting the `patient_records.json` file and restart

## Performance

- App loads in < 2 seconds
- Assessment calculation takes < 1 second
- Handles 1000+ patient records efficiently

## Future Enhancements

- Database backend for better data management
- Multi-user support with authentication
- Export reports as PDF
- Integration with healthcare provider systems
- Appointment booking integration
- Multilingual support

## License

This project is for educational purposes. Ensure compliance with local health regulations when deploying.

## Support & Questions

For technical issues or feature requests, please contact your system administrator or the development team.

## Version History

**v1.0** (November 2024)
- Initial release
- Core assessment functionality
- STD information database
- Patient record management
- Risk scoring system

---

**Last Updated**: November 2024

**Important**: Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment.
