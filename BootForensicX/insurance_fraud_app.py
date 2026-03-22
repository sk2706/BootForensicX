import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
import plotly.express as px
import io

st.set_page_config(page_title="Insurance Fraud Detection", layout="wide")

st.title("🔍 Insurance Claim Fraud Detection")
st.markdown("Upload claim data to detect potential fraud using AI")

@st.cache_resource
def load_fraud_model():
    try:
        classifier = pipeline("text-classification", 
                            model="microsoft/DialoGPT-medium",
                            device=-1)
        return classifier
    except:
        return None

def preprocess_data(df):
    required_columns = ['claim_amount', 'policy_age', 'claimant_age', 'incident_type']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        return None
    
    return df[required_columns]

def analyze_claim_risk(features):
    risk_score = 0
    
    if features['claim_amount'] > 10000:
        risk_score += 0.3
    if features['policy_age'] < 30:
        risk_score += 0.2
    if features['claimant_age'] < 25 or features['claimant_age'] > 65:
        risk_score += 0.2
    if features['incident_type'] in ['theft', 'vandalism']:
        risk_score += 0.3
    
    return min(risk_score, 1.0)

def main():
    model = load_fraud_model()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 Upload Claim Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV file with claim data",
            type=['csv'],
            help="File should contain: claim_amount, policy_age, claimant_age, incident_type"
        )
    
    with col2:
        st.subheader("📊 Quick Stats")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.metric("Total Claims", len(df))
            st.metric("Avg Claim Amount", f"${df['claim_amount'].mean():.2f}")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("📋 Data Preview")
        st.dataframe(df.head())
        
        if st.button("🚀 Analyze for Fraud", type="primary"):
            processed_data = preprocess_data(df)
            
            if processed_data is not None:
                st.subheader("🔍 Fraud Analysis Results")
                
                results = []
                for idx, row in processed_data.iterrows():
                    risk_score = analyze_claim_risk(row.to_dict())
                    
                    if risk_score > 0.6:
                        prediction = "HIGH RISK"
                        confidence = risk_score
                        color = "red"
                    elif risk_score > 0.3:
                        prediction = "MEDIUM RISK"
                        confidence = risk_score
                        color = "orange"
                    else:
                        prediction = "LOW RISK"
                        confidence = 1 - risk_score
                        color = "green"
                    
                    results.append({
                        'Claim ID': idx + 1,
                        'Prediction': prediction,
                        'Confidence': f"{confidence:.2%}",
                        'Risk Score': f"{risk_score:.3f}",
                        'Amount': f"${row['claim_amount']:.2f}"
                    })
                
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.pie(
                        results_df, 
                        names='Prediction', 
                        title="Risk Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig2 = px.histogram(
                        results_df, 
                        x='Risk Score', 
                        title="Risk Score Distribution",
                        nbins=20
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                high_risk = results_df[results_df['Prediction'] == 'HIGH RISK']
                if len(high_risk) > 0:
                    st.warning(f"⚠️ Found {len(high_risk)} high-risk claims requiring investigation")
                    
                    st.subheader("🚨 High Risk Claims")
                    st.dataframe(high_risk, use_container_width=True)
                else:
                    st.success("✅ No high-risk claims detected")

if __name__ == "__main__":
    main()
