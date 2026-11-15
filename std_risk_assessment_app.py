import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="STD Self-Risk Assessment Tool",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing patient records
if "patients" not in st.session_state:
    st.session_state.patients = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# Risk assessment database
RISK_FACTORS = {
    "sexual_partners": {
        "1": 0,
        "2-3": 1,
        "4-5": 2,
        "6+": 3
    },
    "protection_usage": {
        "Always": 0,
        "Most of the time": 1,
        "Sometimes": 2,
        "Never": 3,
        "Not applicable": 0
    },
    "previous_sti": {
        "No": 0,
        "Yes": 2
    },
    "partner_history": {
        "Unknown": 2,
        "No history": 0,
        "Has history": 2,
        "Uncertain": 1
    },
    "recent_symptoms": {
        "No symptoms": 0,
        "Mild symptoms": 1,
        "Moderate symptoms": 2,
        "Severe symptoms": 3
    },
    "last_test": {
        "Within 3 months": 0,
        "3-6 months ago": 1,
        "6-12 months ago": 2,
        "Over 1 year ago": 3,
        "Never tested": 3
    }
}

# STD Information Database
STD_INFO = {
    "Chlamydia": {
        "symptoms": "Unusual discharge, burning during urination, abdominal pain, abnormal menstrual bleeding",
        "transmission": "Unprotected sexual contact",
        "treatment": "Antibiotics (Azithromycin or Doxycycline)",
        "complications": "Pelvic inflammatory disease, infertility, ectopic pregnancy",
        "testing": "Urine or swab test"
    },
    "Gonorrhea": {
        "symptoms": "Painful urination, pus discharge, pelvic pain, abnormal menstrual bleeding",
        "transmission": "Unprotected sexual contact",
        "treatment": "Antibiotics (Ceftriaxone + Azithromycin)",
        "complications": "Infertility, pelvic inflammatory disease, disseminated infection",
        "testing": "Urine or swab test"
    },
    "Syphilis": {
        "symptoms": "Painless sores (chancre), rash, fever, swollen lymph nodes",
        "transmission": "Unprotected sexual contact, blood transfusion, mother to child",
        "treatment": "Antibiotics (Penicillin)",
        "complications": "Neurosyphilis, cardiovascular damage, congenital syphilis",
        "testing": "Blood test (RPR/VDRL and FTA-ABS)"
    },
    "Herpes (HSV)": {
        "symptoms": "Painful blisters, itching, tingling, flu-like symptoms",
        "transmission": "Unprotected sexual contact, skin-to-skin contact",
        "treatment": "Antivirals (Acyclovir, Valacyclovir)",
        "complications": "Recurrent outbreaks, nerve pain, increased HIV risk",
        "testing": "Blood test or viral culture"
    },
    "HPV": {
        "symptoms": "Genital warts, often asymptomatic",
        "transmission": "Unprotected sexual contact",
        "treatment": "Observation, topical treatments, or removal of warts",
        "complications": "Cervical cancer, anal cancer, genital cancer",
        "testing": "HPV test, Pap smear for women"
    },
    "HIV": {
        "symptoms": "Early: flu-like; Later: fatigue, fever, lymphadenopathy",
        "transmission": "Unprotected sexual contact, blood exposure, mother to child",
        "treatment": "Antiretroviral therapy (ART)",
        "complications": "AIDS, opportunistic infections",
        "testing": "Blood test (4th generation), Rapid test"
    },
    "Hepatitis B": {
        "symptoms": "Jaundice, fatigue, abdominal pain, dark urine",
        "transmission": "Unprotected sexual contact, blood exposure",
        "treatment": "Supportive care, Antivirals for chronic infection",
        "complications": "Cirrhosis, hepatic cancer, liver failure",
        "testing": "Blood test (HBsAg, Anti-HBc)"
    }
}

def calculate_risk_score(assessment):
    """Calculate total risk score from assessment"""
    score = 0
    score += RISK_FACTORS["sexual_partners"].get(assessment.get("partners", "1"), 0)
    score += RISK_FACTORS["protection_usage"].get(assessment.get("protection", "Always"), 0)
    score += RISK_FACTORS["previous_sti"].get(assessment.get("previous_sti", "No"), 0)
    score += RISK_FACTORS["partner_history"].get(assessment.get("partner_history", "Unknown"), 0)
    score += RISK_FACTORS["recent_symptoms"].get(assessment.get("symptoms", "No symptoms"), 0)
    score += RISK_FACTORS["last_test"].get(assessment.get("last_test", "Never tested"), 0)
    return score

def get_risk_category(score):
    """Determine risk category based on score"""
    if score <= 2:
        return "LOW RISK", "🟢"
    elif score <= 5:
        return "MODERATE RISK", "🟡"
    elif score <= 9:
        return "HIGH RISK", "🔴"
    else:
        return "VERY HIGH RISK", "🔴"

def get_recommendations(score):
    """Get recommendations based on risk score"""
    recommendations = []
    
    if score <= 2:
        recommendations.append("✓ Continue practicing safe sex habits")
        recommendations.append("✓ Maintain regular STI testing (annually or as recommended)")
        recommendations.append("✓ Use protection consistently")
        recommendations.append("✓ Get vaccinated for HPV and Hepatitis B if eligible")
    elif score <= 5:
        recommendations.append("⚠ Schedule STI testing within 2 weeks")
        recommendations.append("⚠ Discuss sexual history with partner(s)")
        recommendations.append("⚠ Use protection consistently for all sexual activities")
        recommendations.append("⚠ Consider PrEP (Pre-exposure prophylaxis) if at risk for HIV")
        recommendations.append("⚠ Get HPV and Hepatitis B vaccination if not already done")
    elif score <= 9:
        recommendations.append("⚠⚠ Schedule STI testing IMMEDIATELY (within 1 week)")
        recommendations.append("⚠⚠ Inform recent sexual partners to get tested")
        recommendations.append("⚠⚠ Abstain from sexual contact until tested and cleared")
        recommendations.append("⚠⚠ Use protection strictly for all future sexual activities")
        recommendations.append("⚠⚠ Consult a healthcare provider about PrEP")
        recommendations.append("⚠⚠ Inform your healthcare provider about symptoms")
    else:
        recommendations.append("🔴 URGENT: Schedule testing TODAY or visit urgent care")
        recommendations.append("🔴 Seek immediate medical evaluation if experiencing symptoms")
        recommendations.append("🔴 Notify all recent sexual partners for testing")
        recommendations.append("🔴 Abstain from sexual contact until cleared by healthcare provider")
        recommendations.append("🔴 Do not delay - seek professional medical advice immediately")
    
    return recommendations

def save_patient_data():
    """Save patient data to JSON file"""
    if st.session_state.patients:
        filepath = "patient_records.json"
        with open(filepath, "w") as f:
            json.dump(st.session_state.patients, f, indent=4, default=str)

def load_patient_data():
    """Load patient data from JSON file"""
    if os.path.exists("patient_records.json"):
        with open("patient_records.json", "r") as f:
            st.session_state.patients = json.load(f)

# Main app
def main():
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🏥 STD Self-Risk Assessment Tool")
    
    st.markdown("---")
    st.write("This tool helps you understand your personal STD risk status and provides guidance on what steps to take next.")
    st.write("**Disclaimer:** This tool is for educational purposes only and does not replace professional medical advice.")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "New Assessment", "View Records", "STD Information", "About"]
    )
    
    if page == "Home":
        show_home()
    elif page == "New Assessment":
        show_assessment()
    elif page == "View Records":
        show_records()
    elif page == "STD Information":
        show_std_info()
    elif page == "About":
        show_about()

def show_home():
    st.header("Welcome to STD Self-Risk Assessment Tool")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Features")
        st.write("""
        - **Personal Risk Assessment**: Answer a few questions about your sexual health
        - **Risk Scoring**: Get a comprehensive risk score based on multiple factors
        - **Personalized Recommendations**: Receive tailored guidance based on your risk level
        - **STD Information**: Learn about common STDs, symptoms, and treatments
        - **Patient Records**: Store and track your assessment history
        """)
    
    with col2:
        st.subheader("🎯 Risk Categories")
        st.markdown("""
        - 🟢 **Low Risk**: Score 0-2
        - 🟡 **Moderate Risk**: Score 3-5
        - 🔴 **High Risk**: Score 6-9
        - 🔴 **Very High Risk**: Score 10+
        """)
    
    st.markdown("---")
    st.subheader("Getting Started")
    st.write("1. Click on **'New Assessment'** to start your self-risk assessment")
    st.write("2. Answer all questions honestly for accurate results")
    st.write("3. Review your risk score and personalized recommendations")
    st.write("4. Follow the recommended next steps")

def show_assessment():
    st.header("STD Self-Risk Assessment")
    
    with st.form("risk_assessment_form"):
        st.subheader("Personal Information")
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        age = st.number_input("Age *", min_value=13, max_value=120, step=1)
        gender = st.selectbox("Gender *", ["Select...", "Male", "Female", "Non-binary", "Prefer not to say"])
        email = st.text_input("Email (optional)", placeholder="your.email@example.com")
        
        st.markdown("---")
        st.subheader("Sexual History & Behavior")
        
        partners = st.selectbox(
            "Number of sexual partners in the last 12 months *",
            ["1", "2-3", "4-5", "6+"],
            help="This includes all types of sexual contact"
        )
        
        protection = st.selectbox(
            "How often do you use protection (condoms/barriers)? *",
            ["Always", "Most of the time", "Sometimes", "Never", "Not applicable"],
            help="Protection is important for preventing STI transmission"
        )
        
        st.markdown("---")
        st.subheader("Medical & Testing History")
        
        previous_sti = st.selectbox(
            "Have you had any STI (Sexually Transmitted Infection) before? *",
            ["No", "Yes"],
            help="Includes any previously diagnosed STI"
        )
        
        partner_history = st.selectbox(
            "Do you know if any of your recent partners have had STIs? *",
            ["Unknown", "No history", "Has history", "Uncertain"],
            help="This information helps assess transmission risk"
        )
        
        last_test = st.selectbox(
            "When was your last STI test? *",
            ["Within 3 months", "3-6 months ago", "6-12 months ago", "Over 1 year ago", "Never tested"],
            help="Regular testing is recommended for sexually active individuals"
        )
        
        st.markdown("---")
        st.subheader("Current Health Status")
        
        symptoms = st.selectbox(
            "Are you currently experiencing any of these symptoms? *",
            ["No symptoms", "Mild symptoms", "Moderate symptoms", "Severe symptoms"],
            help="Unusual discharge, pain during urination, genital sores, rash, or pelvic pain"
        )
        
        if symptoms != "No symptoms":
            symptom_details = st.text_area(
                "Please describe your symptoms in detail",
                placeholder="Describe the symptoms you're experiencing..."
            )
        
        st.markdown("---")
        
        # Form submission
        submitted = st.form_submit_button("📊 Calculate Risk Score", use_container_width=True)
        
        if submitted:
            if not name or gender == "Select...":
                st.error("Please fill in all required fields marked with *")
            else:
                assessment = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "email": email,
                    "partners": partners,
                    "protection": protection,
                    "previous_sti": previous_sti,
                    "partner_history": partner_history,
                    "last_test": last_test,
                    "symptoms": symptoms,
                    "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if symptoms != "No symptoms":
                    assessment["symptom_details"] = symptom_details
                
                # Calculate risk score
                risk_score = calculate_risk_score(assessment)
                risk_category, risk_emoji = get_risk_category(risk_score)
                
                # Store assessment
                assessment["risk_score"] = risk_score
                assessment["risk_category"] = risk_category
                st.session_state.patients.append(assessment)
                save_patient_data()
                
                # Display results
                st.success("Assessment completed! Here are your results:")
                
                st.markdown("---")
                st.subheader("📊 Your Risk Assessment Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Risk Score", f"{risk_score}/18")
                with col2:
                    st.metric("Risk Category", f"{risk_emoji} {risk_category}")
                with col3:
                    st.metric("Assessment Date", assessment["assessment_date"])
                
                st.markdown("---")
                st.subheader("💡 Personalized Recommendations")
                
                recommendations = get_recommendations(risk_score)
                for rec in recommendations:
                    st.write(rec)
                
                st.markdown("---")
                st.subheader("⚕️ Next Steps")
                
                if risk_score <= 2:
                    st.info("""
                    ✓ Your risk level is low. Continue to:
                    - Practice safe sex consistently
                    - Get tested annually
                    - Maintain open communication with partners
                    - Stay vaccinated against preventable STIs
                    """)
                elif risk_score <= 5:
                    st.warning("""
                    ⚠️ Your risk level is moderate. Please:
                    - Schedule an STI test within 2 weeks
                    - Use protection for all sexual activities
                    - Inform your partners to get tested
                    - Consider speaking with a healthcare provider
                    """)
                elif risk_score <= 9:
                    st.error("""
                    ⚠️⚠️ Your risk level is high. Please:
                    - Schedule an STI test IMMEDIATELY
                    - Visit a clinic or healthcare provider within 1 week
                    - Inform all recent sexual partners
                    - Abstain from sexual contact until tested
                    """)
                else:
                    st.error("""
                    🔴 Your risk level is VERY HIGH. URGENT ACTION NEEDED:
                    - Seek medical evaluation TODAY
                    - Visit an urgent care or emergency department if necessary
                    - Notify all recent sexual partners immediately
                    - Do not engage in sexual activity until cleared by a healthcare provider
                    """)
                
                st.markdown("---")
                st.info("Your assessment has been saved. You can view your records in the 'View Records' section.")

def show_records():
    st.header("Patient Records")
    
    if not st.session_state.patients:
        st.info("No records found. Start a new assessment to create your first record.")
    else:
        st.subheader(f"Total Assessments: {len(st.session_state.patients)}")
        
        # Create dataframe for display
        records_data = []
        for i, patient in enumerate(st.session_state.patients):
            records_data.append({
                "ID": i + 1,
                "Name": patient["name"],
                "Date": patient["assessment_date"],
                "Age": patient["age"],
                "Risk Score": patient["risk_score"],
                "Risk Category": patient["risk_category"]
            })
        
        df = pd.DataFrame(records_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("View Detailed Record")
        
        if st.session_state.patients:
            record_index = st.selectbox(
                "Select a record to view details:",
                range(len(st.session_state.patients)),
                format_func=lambda i: f"{st.session_state.patients[i]['name']} - {st.session_state.patients[i]['assessment_date']}"
            )
            
            patient = st.session_state.patients[record_index]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {patient['name']}")
                st.write(f"**Age:** {patient['age']}")
                st.write(f"**Gender:** {patient['gender']}")
                st.write(f"**Email:** {patient.get('email', 'Not provided')}")
            with col2:
                st.write(f"**Assessment Date:** {patient['assessment_date']}")
                st.write(f"**Risk Score:** {patient['risk_score']}/18")
                st.write(f"**Risk Category:** {patient['risk_category']}")
            
            st.markdown("---")
            st.subheader("Assessment Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Sexual Partners (12 months):** {patient['partners']}")
                st.write(f"**Protection Usage:** {patient['protection']}")
                st.write(f"**Previous STI:** {patient['previous_sti']}")
            with col2:
                st.write(f"**Partner History:** {patient['partner_history']}")
                st.write(f"**Last Test:** {patient['last_test']}")
                st.write(f"**Current Symptoms:** {patient['symptoms']}")
            
            if "symptom_details" in patient:
                st.markdown("---")
                st.write(f"**Symptom Details:** {patient['symptom_details']}")
            
            st.markdown("---")
            st.subheader("Recommendations")
            recommendations = get_recommendations(patient['risk_score'])
            for rec in recommendations:
                st.write(rec)
            
            # Delete record option
            if st.button("🗑️ Delete This Record", key=f"delete_{record_index}"):
                del st.session_state.patients[record_index]
                save_patient_data()
                st.success("Record deleted successfully!")
                st.rerun()

def show_std_info():
    st.header("STD Information & Resources")
    
    st.write("Learn about common sexually transmitted infections, their symptoms, and treatments.")
    
    selected_std = st.selectbox("Select an STI to learn more:", list(STD_INFO.keys()))
    
    if selected_std:
        info = STD_INFO[selected_std]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader(selected_std)
        
        st.markdown("---")
        
        st.subheader("Symptoms")
        st.write(info["symptoms"])
        
        st.markdown("---")
        
        st.subheader("Transmission")
        st.write(info["transmission"])
        
        st.markdown("---")
        
        st.subheader("Treatment")
        st.write(info["treatment"])
        
        st.markdown("---")
        
        st.subheader("Possible Complications")
        st.write(info["complications"])
        
        st.markdown("---")
        
        st.subheader("Testing")
        st.write(info["testing"])
        
        st.markdown("---")
        st.info("For detailed medical information, please consult with a healthcare provider.")

def show_about():
    st.header("About This Tool")
    
    st.write("""
    ## Purpose
    This STD Self-Risk Assessment Tool is designed to:
    - Help individuals understand their personal risk factors for STIs
    - Provide educational information about common STDs
    - Recommend appropriate next steps based on risk assessment
    - Encourage regular testing and safe sexual practices
    
    ## Important Disclaimer
    ⚠️ **This tool is for educational purposes ONLY and does not constitute medical advice.**
    - Results are based on self-reported information
    - A healthcare provider's evaluation is necessary for diagnosis
    - Always consult a medical professional for any health concerns
    - This tool cannot diagnose or treat any condition
    
    ## When to Seek Medical Care
    🔴 Seek immediate medical attention if you experience:
    - Unusual genital discharge or bleeding
    - Pain during urination or sexual intercourse
    - Genital sores, blisters, or warts
    - Unexplained rashes in genital areas
    - Pelvic or abdominal pain
    - Fever with other symptoms
    - Any other concerning symptoms
    
    ## STI Testing
    Regular STI testing is recommended if you:
    - Are sexually active
    - Have multiple partners
    - Are starting a new relationship
    - Have had unprotected sex
    - Are pregnant
    - Have symptoms of an STI
    
    ## Prevention
    Best practices to reduce STI risk:
    ✓ Use condoms and barriers consistently
    ✓ Get regular STI testing
    ✓ Communicate with partners about sexual history
    ✓ Avoid sexual contact with untreated partners
    ✓ Get vaccinated (HPV, Hepatitis B)
    ✓ Limit number of sexual partners
    ✓ Seek treatment immediately if diagnosed
    
    ## Resources
    - CDC Sexual Health Information: www.cdc.gov/sexualhealth
    - Planned Parenthood: www.plannedparenthood.org
    - WHO STI Information: www.who.int
    - Local Health Department websites
    
    ## Data Privacy
    Your assessment data is stored locally on this device. Please ensure:
    - Keep your assessment records secure
    - Share results only with healthcare providers
    - Delete records when no longer needed
    """)
    
    st.markdown("---")
    st.subheader("Version & Support")
    st.write("**Version:** 1.0")
    st.write("**Last Updated:** November 2024")
    st.write("**Support:** Consult your healthcare provider or local health department for assistance")

# Load existing patient data on startup
load_patient_data()

# Run the app
if __name__ == "__main__":
    main()
