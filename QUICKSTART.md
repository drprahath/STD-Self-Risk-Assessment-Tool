# Quick Start Guide - STD Self-Risk Assessment App

## Step 1: Install Requirements

Open your command prompt/terminal in the app directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

```bash
streamlit run std_risk_assessment_app.py
```

## Step 3: Access the Web App

The app will automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually paste this URL into your browser.

---

## App Navigation

### 🏠 Home
- Overview of the tool
- Risk category information
- Getting started instructions

### 📋 New Assessment
Complete a comprehensive questionnaire covering:
1. **Personal Information**
   - Full name, age, gender, email

2. **Sexual History & Behavior**
   - Number of sexual partners in last 12 months
   - Frequency of protection usage

3. **Medical & Testing History**
   - Previous STI diagnoses
   - Sexual partner STI history
   - Date of last STI test

4. **Current Health Status**
   - Current symptoms (if any)
   - Detailed symptom description

**Result**: Get your risk score (0-18) and personalized recommendations!

### 💾 View Records
- See all your past assessments
- View detailed information for each assessment
- Compare results over time
- Delete old records

### 📚 STD Information
Learn about 7 common STIs:
- Chlamydia
- Gonorrhea
- Syphilis
- Herpes (HSV)
- HPV
- HIV
- Hepatitis B

For each STI, you'll find:
- Common symptoms
- How it's transmitted
- Available treatments
- Possible complications
- How it's tested

### ℹ️ About
- Important medical disclaimers
- When to seek immediate medical care
- Prevention strategies
- Helpful resources and hotlines

---

## Understanding Your Results

### Risk Score (0-18 points)

**🟢 Low Risk (0-2 points)**
- Continue current safe practices
- Get tested annually
- Use protection consistently
- Stay up-to-date with vaccinations

**🟡 Moderate Risk (3-5 points)**
- Schedule STI test within 2 weeks
- Inform recent partners to get tested
- Use protection for all sexual activities
- Consider PrEP if at HIV risk

**🔴 High Risk (6-9 points)**
- Schedule test IMMEDIATELY (within 1 week)
- Inform all recent sexual partners
- Abstain from sexual contact until tested
- Consult healthcare provider URGENTLY

**🔴 Very High Risk (10+ points)**
- Seek medical evaluation TODAY
- Visit urgent care if necessary
- Notify all recent partners immediately
- Do not engage in sexual activity until cleared

---

## Example Scenarios

### Scenario 1: Low Risk Individual
**Profile:**
- 1 sexual partner in last 12 months
- Always uses protection
- No previous STI
- Partner has no history of STI
- Last tested 2 months ago
- No symptoms

**Expected Score:** 0-2 (Low Risk)
**Recommendations:** Continue safe practices, test annually

### Scenario 2: Moderate Risk Individual
**Profile:**
- 3-4 sexual partners in last 12 months
- Uses protection most of the time
- No previous STI
- Uncertain about partner history
- Last tested 6 months ago
- No symptoms

**Expected Score:** 3-5 (Moderate Risk)
**Recommendations:** Test within 2 weeks, use protection consistently

### Scenario 3: High Risk Individual
**Profile:**
- 5+ sexual partners in last 12 months
- Inconsistent protection usage
- Previous STI in past
- Partner has STI history
- Last tested over 1 year ago
- Experiencing symptoms

**Expected Score:** 6-9+ (High Risk)
**Recommendations:** Test immediately, notify partners, seek medical care

---

## Tips for Accurate Assessment

✅ **Be Honest**
- Accurate answers lead to accurate risk assessment
- Your data is private and local to your device

✅ **Remember Sexual History**
- Include all types of sexual contact (vaginal, anal, oral)
- Look back 12 months for partner count

✅ **Know Your Testing History**
- Keep track of your last STI test
- Different tests are needed for different STIs

✅ **Understand Symptoms**
- Unusual discharge, pain, sores, rashes in genital areas
- Pelvic pain, abnormal bleeding
- Other flu-like symptoms with sexual exposure

---

## After Your Assessment

### If Low Risk (0-2)
1. ✓ Continue safe sexual practices
2. ✓ Get tested annually
3. ✓ Stay vaccinated
4. ✓ Maintain open communication with partners

### If Moderate Risk (3-5)
1. ⚠️ Schedule STI test within 2 weeks
2. ⚠️ Use protection consistently
3. ⚠️ Inform recent partners
4. ⚠️ Talk to healthcare provider

### If High Risk (6-9)
1. 🔴 Schedule test IMMEDIATELY
2. 🔴 Visit clinic/doctor within 1 week
3. 🔴 Notify all recent sexual partners
4. 🔴 Abstain from sexual activity until cleared

### If Very High Risk (10+)
1. 🔴 Seek medical help TODAY
2. 🔴 Go to urgent care if needed
3. 🔴 Contact all recent partners immediately
4. 🔴 Do NOT have sex until cleared by doctor

---

## Finding Healthcare Services

### Where to Get Tested
- **Local Health Department** - Often free or low-cost
- **Planned Parenthood** - Confidential services
- **Community Health Centers** - Affordable care
- **Your Doctor** - Primary care physician
- **Urgent Care Centers** - For immediate needs
- **Hospitals** - Emergency rooms

### How to Find Services
1. Search "STI testing near me"
2. Call your local health department
3. Visit Planned Parenthood's clinic locator
4. Ask your doctor for referrals
5. Check your insurance network

---

## Important Reminders

⚠️ **This tool is for educational purposes only**
- It does NOT diagnose any condition
- It does NOT replace professional medical advice
- Always consult a healthcare provider
- Seek immediate medical care for severe symptoms

✓ **Privacy**
- Your data stays on your device
- No information is sent to external servers
- Keep your assessment records secure
- Share results only with healthcare providers

---

## Common Questions

**Q: Is my data private?**
A: Yes, all data is stored locally on your device in `patient_records.json`

**Q: Can this diagnose an STI?**
A: No, this is for risk assessment only. Only a healthcare provider can diagnose.

**Q: How often should I test?**
A: Sexually active individuals should test at least annually, or more frequently based on risk.

**Q: What if I test positive?**
A: Contact your healthcare provider immediately. Most STIs are treatable with antibiotics or antivirals.

**Q: Should I tell my partners?**
A: Yes, recent sexual partners should be notified so they can get tested and treated if needed.

**Q: Is there a vaccine?**
A: Yes, vaccines exist for HPV and Hepatitis B. Ask your doctor if you're eligible.

---

## Keyboard Shortcuts

- **Refresh App**: F5 or Ctrl+R
- **Clear Browser Cache**: Ctrl+Shift+Delete
- **Open Developer Tools**: F12

---

## Troubleshooting

### App won't start
```bash
pip install --upgrade streamlit
streamlit run std_risk_assessment_app.py
```

### Port is already in use
```bash
streamlit run std_risk_assessment_app.py --server.port 8502
```

### Records disappeared
- Check if `patient_records.json` exists in the app directory
- Restore from backup if available

---

## Support Resources

🏥 **Medical Resources**
- CDC Sexual Health: www.cdc.gov/sexualhealth
- Planned Parenthood: www.plannedparenthood.org
- WHO STI Info: www.who.int

📞 **Hotlines**
- STI Hotline: 1-800-232-4636 (US)
- Chat support at various health websites

📱 **Apps & Tools**
- Partner notification services
- Appointment booking apps
- Health record management apps

---

## Version: 1.0
**Last Updated**: November 2024

**Remember**: This tool is here to help you understand your risk and take appropriate action. When in doubt, always consult a qualified healthcare professional.
