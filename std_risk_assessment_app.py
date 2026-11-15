import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import hashlib
import json
from io import BytesIO
import os

# Page configuration
st.set_page_config(
    page_title="STD Risk Assessment Tool v4",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .admin-badge { background-color: #ff6b6b; color: white; padding: 5px 10px; border-radius: 5px; }
    .user-badge { background-color: #4ecdc4; color: white; padding: 5px 10px; border-radius: 5px; }
    .success-box { background-color: #d4edda; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745; }
    .info-box { background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #17a2b8; }
    .warning-box { background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; }
</style>
""", unsafe_allow_html=True)

# ===== DATABASE SETUP =====
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('std_assessment.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        user_type TEXT,
        name TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Assessments table
    c.execute('''CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY,
        user_id TEXT NOT NULL,
        name TEXT,
        age INTEGER,
        email TEXT,
        phone TEXT,
        responses TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    
    conn.commit()
    conn.close()

init_database()

# ===== AUTHENTICATION FUNCTIONS =====
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin(admin_id, password):
    """Verify admin credentials"""
    conn = sqlite3.connect('std_assessment.db')
    c = conn.cursor()
    c.execute('SELECT password_hash, user_type FROM users WHERE user_id = ?', (admin_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[1] == 'admin':
        return hash_password(password) == result[0]
    return False

def verify_user(user_id):
    """Verify user exists (no password needed)"""
    conn = sqlite3.connect('std_assessment.db')
    c = conn.cursor()
    c.execute('SELECT user_type FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    return result and result[0] == 'user'

def create_admin_account(admin_id, password, name, email):
    """Create admin account"""
    try:
        conn = sqlite3.connect('std_assessment.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, password_hash, user_type, name, email) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (admin_id, hash_password(password), 'admin', name, email))
        conn.commit()
        conn.close()
        return True, "Admin account created successfully"
    except sqlite3.IntegrityError:
        return False, "Admin ID already exists"

def create_user_account(user_id, name, email, phone):
    """Create user account (no password)"""
    try:
        conn = sqlite3.connect('std_assessment.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, user_type, name, email) 
                     VALUES (?, ?, ?, ?)''',
                  (user_id, 'user', name, email))
        conn.commit()
        conn.close()
        return True, "User account created successfully"
    except sqlite3.IntegrityError:
        return False, "User ID already exists"

# ===== LOGIN PAGE =====
def login_page():
    """Render login page"""
    st.title("🏥 STD Self-Risk Assessment Tool v4.0")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("👨‍⚕️ Admin Login")
        admin_id = st.text_input("Admin ID", key="admin_id")
        admin_password = st.text_input("Password", type="password", key="admin_password")
        
        if st.button("🔓 Admin Login", key="admin_login_btn"):
            if verify_admin(admin_id, admin_password):
                st.session_state.logged_in = True
                st.session_state.user_type = 'admin'
                st.session_state.user_id = admin_id
                st.success("✅ Admin login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid admin ID or password")
        
        st.markdown("---")
        st.subheader("Create Admin Account (First Time)")
        with st.expander("Create New Admin Account"):
            new_admin_id = st.text_input("New Admin ID", key="new_admin_id")
            new_admin_password = st.text_input("Password", type="password", key="new_admin_password")
            new_admin_name = st.text_input("Full Name", key="new_admin_name")
            new_admin_email = st.text_input("Email", key="new_admin_email")
            
            if st.button("Create Admin Account", key="create_admin_btn"):
                if new_admin_id and new_admin_password and new_admin_name:
                    success, message = create_admin_account(new_admin_id, new_admin_password, new_admin_name, new_admin_email)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill all required fields")
    
    with col2:
        st.header("👤 User Login")
        user_id = st.text_input("User ID (No Password Required)", key="user_id")
        user_name = st.text_input("Your Full Name", key="user_name")
        user_email = st.text_input("Your Email", key="user_email")
        
        if st.button("✅ User Login", key="user_login_btn"):
            if verify_user(user_id):
                st.session_state.logged_in = True
                st.session_state.user_type = 'user'
                st.session_state.user_id = user_id
                st.success("✅ User login successful!")
                st.rerun()
            else:
                st.warning("User ID not found. Creating new account...")
                success, message = create_user_account(user_id, user_name, user_email, "")
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'user'
                    st.session_state.user_id = user_id
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("---")
        st.info("💡 **User Login Info:** No password needed! Just enter your User ID and name to get started.")

# ===== ASSESSMENT QUESTIONS =====
ASSESSMENT_QUESTIONS = {
    1: {
        "question": "What is your age group?",
        "options": {
            "13-19": 2,
            "20-29": 2,
            "30-39": 1,
            "40+": 0
        }
    },
    2: {
        "question": "Number of sexual partners in the past year?",
        "options": {
            "None": 0,
            "1 partner": 1,
            "2-5 partners": 2,
            "More than 5": 3
        }
    },
    3: {
        "question": "How often do you use condoms?",
        "options": {
            "Always": 0,
            "Usually": 1,
            "Sometimes": 2,
            "Never": 3
        }
    },
    4: {
        "question": "Have you been diagnosed with an STI before?",
        "options": {
            "No": 0,
            "Yes, but treated": 2,
            "Yes, current": 3
        }
    },
    5: {
        "question": "Do you know your partner's STI status?",
        "options": {
            "Yes, negative": 0,
            "Uncertain": 2,
            "Not discussed": 3
        }
    },
    6: {
        "question": "Are you experiencing any symptoms?",
        "options": {
            "No symptoms": 0,
            "Mild symptoms": 2,
            "Significant symptoms": 3
        }
    },
    7: {
        "question": "Have you had unprotected sex in past 3 months?",
        "options": {
            "No": 0,
            "Yes, once": 2,
            "Yes, multiple times": 3
        }
    },
    8: {
        "question": "Any other health conditions affecting immunity?",
        "options": {
            "No": 0,
            "Diabetes": 1,
            "HIV/AIDS": 3
        }
    },
    9: {
        "question": "When was your last STI test?",
        "options": {
            "Less than 3 months ago": 0,
            "3-12 months ago": 1,
            "More than 1 year ago": 2,
            "Never tested": 3
        }
    },
    10: {
        "question": "Are you taking PrEP (Pre-exposure prophylaxis)?",
        "options": {
            "Yes, regularly": 0,
            "No": 2
        }
    },
    11: {
        "question": "Have you received HPV vaccination?",
        "options": {
            "Yes, complete": 0,
            "Partial": 1,
            "No": 2
        }
    },
    12: {
        "question": "Do you have access to regular sexual health education?",
        "options": {
            "Yes": 0,
            "Limited": 1,
            "No": 2
        }
    }
}

RISK_CATEGORIES = {
    (0, 6): ("🟢 Lower Risk", "Your risk level is relatively low. Continue preventive practices."),
    (7, 15): ("🟡 Moderate Risk", "You have moderate risk. Get tested and consider preventive measures."),
    (16, 25): ("🔴 Higher Risk", "You have higher risk. Urgent testing and consultation recommended."),
    (26, 36): ("🔴 Very High Risk", "You have very high risk. Immediate medical consultation required."),
}

def get_risk_level(score):
    """Get risk level based on score"""
    for (min_score, max_score), (level, recommendation) in RISK_CATEGORIES.items():
        if min_score <= score <= max_score:
            return level, recommendation
    return "Unknown", "Unable to determine risk level"

# ===== USER ASSESSMENT FLOW =====
def user_assessment_page():
    """User assessment form"""
    st.header("📋 New Assessment")
    st.info("Please answer all questions honestly for accurate results. Your responses are kept private.")
    
    # Personal details
    st.subheader("👤 Personal Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", key="assess_name")
        age = st.number_input("Age", min_value=13, max_value=100, key="assess_age")
    with col2:
        email = st.text_input("Email", key="assess_email")
        phone = st.text_input("Phone Number", key="assess_phone")
    
    # Assessment questions
    st.subheader("🔍 Assessment Questions")
    responses = {}
    total_score = 0
    
    for q_num, q_data in ASSESSMENT_QUESTIONS.items():
        st.markdown(f"**Question {q_num}/12:** {q_data['question']}")
        response = st.radio(
            label=f"Select option for Q{q_num}",
            options=list(q_data['options'].keys()),
            key=f"q{q_num}",
            label_visibility="collapsed"
        )
        responses[q_num] = response
        total_score += q_data['options'][response]
        st.markdown("---")
    
    # Preview and submit
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👁️ Preview Results", key="preview_btn"):
            risk_level, recommendation = get_risk_level(total_score)
            st.markdown(f"<div class='info-box'><h3>Preview: Your Risk Score</h3><h2>{total_score}/36</h2><p>{risk_level}</p><p>{recommendation}</p></div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("✅ Final Submit", key="submit_btn"):
            if name and email:
                conn = sqlite3.connect('std_assessment.db')
                c = conn.cursor()
                c.execute('''INSERT INTO assessments (user_id, name, age, email, phone, responses, risk_score, risk_level)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (st.session_state.user_id, name, age, email, phone, 
                           json.dumps(responses), total_score, risk_level))
                conn.commit()
                conn.close()
                
                st.success("✅ Assessment submitted successfully!")
                st.balloons()
                
                # Show results
                st.markdown(f"<div class='success-box'><h3>Your Assessment Results</h3><h2>{total_score}/36</h2><p><strong>{risk_level}</strong></p><p>{recommendation}</p></div>", unsafe_allow_html=True)
            else:
                st.error("Please fill in name and email before submitting")

# ===== ADMIN DASHBOARD =====
def admin_dashboard():
    """Admin control panel"""
    st.header("👨‍⚕️ Admin Dashboard")
    
    # Admin menu
    admin_menu = st.sidebar.radio(
        "Admin Menu",
        ["📊 Dashboard", "👥 View All Records", "✏️ Edit Records", "📥 Export Data", "⚙️ Settings"]
    )
    
    if admin_menu == "📊 Dashboard":
        st.subheader("Dashboard Overview")
        
        conn = sqlite3.connect('std_assessment.db')
        c = conn.cursor()
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        c.execute('SELECT COUNT(*) FROM assessments')
        total_assessments = c.fetchone()[0]
        with col1:
            st.metric("Total Assessments", total_assessments)
        
        c.execute('SELECT COUNT(DISTINCT user_id) FROM assessments')
        total_users = c.fetchone()[0]
        with col2:
            st.metric("Total Users", total_users)
        
        c.execute('SELECT AVG(risk_score) FROM assessments')
        avg_risk = c.fetchone()[0] or 0
        with col3:
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        
        c.execute('SELECT COUNT(*) FROM assessments WHERE risk_score >= 26')
        high_risk = c.fetchone()[0]
        with col4:
            st.metric("High Risk Cases", high_risk)
        
        # Risk distribution chart
        st.subheader("Risk Level Distribution")
        c.execute('''SELECT risk_level, COUNT(*) FROM assessments GROUP BY risk_level''')
        data = c.fetchall()
        
        if data:
            df_risk = pd.DataFrame(data, columns=['Risk Level', 'Count'])
            st.bar_chart(df_risk.set_index('Risk Level'))
        
        conn.close()
    
    elif admin_menu == "👥 View All Records":
        st.subheader("All Patient Records")
        
        conn = sqlite3.connect('std_assessment.db')
        df = pd.read_sql_query('''SELECT id, user_id, name, age, email, risk_score, risk_level, created_at FROM assessments
                                   ORDER BY created_at DESC''', conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No assessments found")
    
    elif admin_menu == "✏️ Edit Records":
        st.subheader("Edit Patient Records")
        
        conn = sqlite3.connect('std_assessment.db')
        c = conn.cursor()
        c.execute('SELECT id, name, age, email FROM assessments ORDER BY created_at DESC')
        records = c.fetchall()
        conn.close()
        
        if records:
            record_options = [f"{r[1]} (ID: {r[0]})" for r in records]
            selected_record = st.selectbox("Select Record to Edit", record_options)
            
            if selected_record:
                record_id = int(selected_record.split("ID: ")[1].rstrip(")"))
                
                conn = sqlite3.connect('std_assessment.db')
                c = conn.cursor()
                c.execute('SELECT name, age, email, phone FROM assessments WHERE id = ?', (record_id,))
                record = c.fetchone()
                
                if record:
                    st.markdown("**Edit Details:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name", value=record[0])
                        new_age = st.number_input("Age", value=record[1], min_value=13, max_value=100)
                    with col2:
                        new_email = st.text_input("Email", value=record[2])
                        new_phone = st.text_input("Phone", value=record[3] or "")
                    
                    if st.button("💾 Save Changes"):
                        c.execute('''UPDATE assessments SET name=?, age=?, email=?, phone=? WHERE id=?''',
                                  (new_name, new_age, new_email, new_phone, record_id))
                        conn.commit()
                        st.success("✅ Record updated successfully!")
                
                conn.close()
        else:
            st.info("No records to edit")
    
    elif admin_menu == "📥 Export Data":
        st.subheader("Export Patient Data")
        
        conn = sqlite3.connect('std_assessment.db')
        df = pd.read_sql_query('''SELECT user_id, name, age, email, phone, risk_score, risk_level, created_at FROM assessments
                                   ORDER BY created_at DESC''', conn)
        conn.close()
        
        if not df.empty:
            # Excel export
            st.markdown("**📊 Export Formats:**")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Export as Excel"):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Assessments')
                    output.seek(0)
                    st.download_button(
                        label="Download Excel File",
                        data=output.getvalue(),
                        file_name=f"assessments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col2:
                if st.button("📥 Export as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV File",
                        data=csv,
                        file_name=f"assessments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        else:
            st.info("No data to export")

# ===== MAIN APP LOGIC =====
def main():
    """Main application"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.user_id = None
    
    # Logout button in sidebar
    if st.session_state.logged_in:
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_id = None
            st.rerun()
        
        # Show current user
        if st.session_state.user_type == 'admin':
            st.sidebar.markdown(f"<div class='admin-badge'>👨‍⚕️ Admin: {st.session_state.user_id}</div>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"<div class='user-badge'>👤 User: {st.session_state.user_id}</div>", unsafe_allow_html=True)
    
    # Render appropriate page
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == 'admin':
        admin_dashboard()
    else:  # Regular user
        st.header("🏥 STD Self-Risk Assessment Tool")
        user_menu = st.sidebar.radio("Menu", ["📋 New Assessment", "📊 My Records", "📚 Information", "❓ About"])
        
        if user_menu == "📋 New Assessment":
            user_assessment_page()
        elif user_menu == "📊 My Records":
            st.subheader("My Assessment Records")
            conn = sqlite3.connect('std_assessment.db')
            df = pd.read_sql_query('''SELECT created_at, risk_score, risk_level FROM assessments 
                                       WHERE user_id = ? ORDER BY created_at DESC''',
                                   conn, params=(st.session_state.user_id,))
            conn.close()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No assessments yet")
        elif user_menu == "📚 Information":
            st.subheader("STD Information & Resources")
            st.info("📖 Coming soon - Comprehensive STD information and resources")
        elif user_menu == "❓ About":
            st.subheader("About This Tool")
            st.markdown("""
            This tool helps you assess your STD risk based on various factors.
            **Standards:** NACO, TANSACS, CDC, WHO
            """)

if __name__ == "__main__":
    main()
