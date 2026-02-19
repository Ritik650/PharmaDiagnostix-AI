import streamlit as st
import requests
import json
from datetime import datetime

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="PharmaDiagnostix AI Clinical Portal", page_icon="🧬", layout="wide")

# 2. Advanced CSS for Enterprise Styling
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 8px; font-weight: bold; height: 50px;}
    .safe-card {background-color: #d4edda; border-left: 8px solid #28a745; padding: 20px; border-radius: 8px; color: #155724; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .warning-card {background-color: #fff3cd; border-left: 8px solid #ffc107; padding: 20px; border-radius: 8px; color: #856404; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .danger-card {background-color: #f8d7da; border-left: 8px solid #dc3545; padding: 20px; border-radius: 8px; color: #721c24; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .unknown-card {background-color: #e2e3e5; border-left: 8px solid #6c757d; padding: 20px; border-radius: 8px; color: #383d41; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .metric-box {background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Area
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80) # Placeholder Medical Icon
with col_title:
    st.title("PharmaDiagnostix AI")
    st.markdown("**Precision Pharmacogenomics & AI Clinical Decision Support**")
st.markdown("---")

# 4. EHR Sidebar (Makes it look like a real hospital system)
with st.sidebar:
    st.header("📋 Patient EHR Entry")
    patient_id = st.text_input("Patient ID", value="PAT-88392")
    
    st.subheader("Demographics (Mock)")
    col_age, col_sex = st.columns(2)
    with col_age: st.number_input("Age", value=45, min_value=1)
    with col_sex: st.selectbox("Sex", ["M", "F", "Other"])
    
    st.subheader("🧬 Genomic Analysis Setup")
    drug = st.selectbox(
        "Target Medication", 
        ["CODEINE", "CLOPIDOGREL", "WARFARIN", "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"],
        help="Select the drug you intend to prescribe."
    )
    uploaded_file = st.file_uploader("Upload Sequenced VCF", type=['vcf'])
    
    st.markdown("---")
    st.caption("Secured via PharmaDiagnostix End-to-End Encryption")

# 5. Main Action
if not uploaded_file:
    st.info("👈 **Awaiting Data:** Please enter patient details and upload a VCF file in the sidebar to begin the AI analysis.")
    # Optional: Display a diagram to make the empty state look professional
    # 

if uploaded_file and st.button("🚀 Execute AI Risk Assessment", type="primary"):
    with st.spinner('🧬 Sequencing VCF, matching CPIC guidelines, and generating Med-Gemma insights...'):
        try:
            # API Call
            files = {'vcf_file': (uploaded_file.name, uploaded_file.getvalue(), 'text/vcard')}
            data = {'patient_id': patient_id, 'drug': drug}
            response = requests.post("http://localhost:8000/analyze", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                risk = result['risk_assessment']['risk_label']
                severity = result['risk_assessment']['severity']
                confidence = result['risk_assessment']['confidence_score']
                
                # --- DASHBOARD METRICS ROW ---
                st.markdown("### 📊 Rapid Analysis Overview")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric(label="Target Gene", value=result['gene'])
                m2.metric(label="Risk Level", value=risk)
                m3.metric(label="Severity", value=severity.upper())
                m4.metric(label="AI Confidence", value=f"{confidence * 100}%")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- INTERACTIVE TABS ---
                tab1, tab2, tab3 = st.tabs(["🚦 AI Clinical Narrative", "🧬 Genomic Breakdown", "📄 Export & Raw Data"])
                
                with tab1:
                    st.subheader("Clinical Decision Support")
                    
                    # Enhanced Traffic Light Cards
                    if severity in ["high", "critical"]:
                        st.markdown(f"<div class='danger-card'><h3>🚨 RED ALERT: {risk}</h3><p>High risk of adverse drug reaction or severe inefficacy detected.</p></div>", unsafe_allow_html=True)
                    elif severity == "moderate" and risk != "Unknown":
                        st.markdown(f"<div class='warning-card'><h3>⚠️ CAUTION: {risk}</h3><p>Dosage adjustment highly recommended based on CPIC guidelines.</p></div>", unsafe_allow_html=True)
                    elif risk == "Safe":
                        st.markdown(f"<div class='safe-card'><h3>✅ CLEAR: {risk}</h3><p>Patient metabolizer status indicates standard dosing is safe.</p></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='unknown-card'><h3>🔍 INCONCLUSIVE: {risk}</h3><p>Missing or sparse genetic markers. Proceed with standard clinical caution.</p></div>", unsafe_allow_html=True)
                    
                    st.markdown("#### 🤖 Med-Gemma Explanation")
                    st.info(result['explanation'])

                with tab2:
                    st.subheader("Pharmacogenomic Details")
                    col_gen1, col_gen2 = st.columns(2)
                    with col_gen1:
                        st.markdown("**Predicted Phenotype & Diplotype**")
                        st.code(result['phenotype'], language="text")
                    with col_gen2:
                        st.markdown("**Analyzed Medication**")
                        st.code(result['drug'], language="text")
                    
                    st.write("This analysis is derived by scanning the patient's VCF file against known pharmacogene star alleles and processing the result through our custom risk engine.")

                with tab3:
                    st.subheader("Raw API Telemetry")
                    st.json(result)
                    
                    # Generate a downloadable text report
                    report_content = f"""PharmaDiagnostix CLINICAL REPORT
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Patient ID: {patient_id}
Drug: {drug}
Gene: {result['gene']}
Phenotype: {result['phenotype']}
Risk Label: {risk}
Severity: {severity.upper()}

CLINICAL NARRATIVE:
{result['explanation']}
"""
                    st.download_button(
                        label="📥 Download Clinical Report (TXT)",
                        data=report_content,
                        file_name=f"PGx_Report_{patient_id}_{drug}.txt",
                        mime="text/plain"
                    )
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Backend Connection Failed. Ensure FastAPI is running on port 8000. Error: {e}")