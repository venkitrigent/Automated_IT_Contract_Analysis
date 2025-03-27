import streamlit as st
import json
import time
import os
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.document_parser import parse_document
from crew import ContractAnalysisCrew

# Check if Azure OpenAI or OpenAI is configured
USING_AZURE = os.getenv("AZURE_OPENAI_API_KEY") is not None and \
              os.getenv("AZURE_OPENAI_ENDPOINT") is not None and \
              os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") is not None

# Set page configuration
st.set_page_config(
    page_title="IT Contract Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
    }
    .upload-section {
        border: 2px dashed #ccc;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .results-section {
        margin-top: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .warning {
        color: #ff4b4b;
        font-weight: bold;
    }
    .success {
        color: #4CAF50;
        font-weight: bold;
    }
    .env-info {
        background-color: #e0f7fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

def validate_config():
    """Validate the LLM configuration and return status"""
    if USING_AZURE:
        # Azure OpenAI validation
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION"
        ]
        
        print(f"Checking Azure OpenAI environment variables...")
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                print(f"✓ {var} is set")
        
        if missing_vars:
            for var in missing_vars:
                print(f"✗ {var} is missing")
            return False, f"Missing environment variables: {', '.join(missing_vars)}"
            
        return True, "Azure OpenAI configuration is valid."
    else:
        # Standard OpenAI validation
        if not os.getenv("OPENAI_API_KEY"):
            print("✗ OPENAI_API_KEY is missing")
            return False, "Missing OPENAI_API_KEY environment variable"
        else:
            print("✓ OPENAI_API_KEY is set")
            return True, "OpenAI configuration is valid."

def main():
    # Title and description
    st.title("📄 Automated IT Contract Analysis")
    
    # Show banner for OpenAI vs Azure OpenAI
    if USING_AZURE:
        st.success("Using Azure OpenAI for analysis")
    else:
        st.warning("Using standard OpenAI API for analysis")
    
    # Check LLM Configuration
    config_valid, config_message = validate_config()
    
    if not config_valid:
        st.error(f"LLM Configuration Error: {config_message}")
        
        # Show debug information if in development
        with st.expander("Environment Debug Information"):
            st.markdown("<div class='env-info'>", unsafe_allow_html=True)
            if USING_AZURE:
                st.write("### Azure OpenAI Settings")
                azure_vars = {
                    "AZURE_OPENAI_API_KEY": "***" + (os.getenv("AZURE_OPENAI_API_KEY", "")[-4:] if os.getenv("AZURE_OPENAI_API_KEY") else "Not Set"),
                    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", "Not Set"),
                    "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "Not Set"),
                    "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", "Not Set")
                }
                for key, value in azure_vars.items():
                    st.write(f"{key}: {value}")
            else:
                st.write("### OpenAI Settings")
                openai_key = os.getenv("OPENAI_API_KEY", "Not Set")
                masked_key = "***" + openai_key[-4:] if openai_key != "Not Set" else "Not Set"
                st.write(f"OPENAI_API_KEY: {masked_key}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        if USING_AZURE:
            st.info("""
            Please check your .env file and ensure all required Azure OpenAI variables are set correctly:
            
            ```
            AZURE_OPENAI_API_KEY=your_api_key_here
            AZURE_OPENAI_ENDPOINT=https://your_resource_name.openai.azure.com/
            AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
            AZURE_OPENAI_API_VERSION=2024-02-15-preview
            ```
            
            Make sure your deployment is active in Azure OpenAI Studio and the deployment name is correct.
            """)
        else:
            st.info("""
            Please set the OPENAI_API_KEY environment variable in your .env file:
            
            ```
            OPENAI_API_KEY=your_openai_api_key_here
            ```
            """)
        return
    
    st.markdown("""
    <div class="info-box">
        <p>Upload your IT contract document to get instant insights on key terms, compliance issues, and potential risks.</p>
        <p>Supported file formats: <strong>PDF</strong>, <strong>DOCX</strong>, <strong>TXT</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drag and drop your IT contract document here", 
                                     type=["pdf", "docx", "txt"],
                                     accept_multiple_files=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with st.expander("Document Preview", expanded=True):
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type
            }
            
            st.json(file_details)
        
        # Process document button
        if st.button("Analyze Contract"):
            # Parse the document
            with st.spinner("Parsing document..."):
                document_info = parse_document(uploaded_file, uploaded_file.name)
                
                if not document_info["success"]:
                    st.error(f"Failed to parse document: {document_info['error']}")
                else:
                    st.success("Document parsed successfully!")
                    
                    # Display a short preview of the extracted text
                    with st.expander("Document Text Preview", expanded=False):
                        preview_text = document_info["text"][:500] + "..." if len(document_info["text"]) > 500 else document_info["text"]
                        st.text_area("Extracted Text", preview_text, height=150)
                    
                    # Run the analysis
                    with st.spinner("Analyzing contract... This may take a few minutes..."):
                        progress_bar = st.progress(0)
                        
                        # Create progress updates
                        progress_steps = [
                            "Extracting contract information...",
                            "Identifying parties and key terms...",
                            "Analyzing compliance requirements...",
                            "Assessing risks and obligations...",
                            "Generating final report..."
                        ]
                        
                        # Show progress text
                        progress_text = st.empty()
                        
                        # Create initial progress
                        progress_text.text(progress_steps[0])
                        progress_bar.progress(20)
                        
                        try:
                            # Run the analysis with our CrewAI crew
                            analysis_results = ContractAnalysisCrew.analyze_contract(document_info["text"])
                            
                            # Update progress to completion
                            progress_bar.progress(100)
                            progress_text.text("Analysis complete!")
                            
                            # Display results
                            st.markdown("## Analysis Results")
                            
                            # Contract Data
                            if "contract_details" in analysis_results:
                                with st.expander("📋 Contract Information", expanded=True):
                                    try:
                                        if isinstance(analysis_results["contract_details"], dict):
                                            st.json(analysis_results["contract_details"])
                                        else:
                                            st.text_area("Contract Data", str(analysis_results["contract_details"]), height=300)
                                    except Exception:
                                        st.text_area("Contract Data", str(analysis_results["contract_details"]), height=300)
                            
                            # Compliance Analysis
                            if "compliance_analysis" in analysis_results:
                                with st.expander("⚖️ Compliance Analysis", expanded=True):
                                    try:
                                        if isinstance(analysis_results["compliance_analysis"], dict):
                                            st.json(analysis_results["compliance_analysis"])
                                        else:
                                            st.markdown(str(analysis_results["compliance_analysis"]))
                                    except Exception:
                                        st.markdown(str(analysis_results["compliance_analysis"]))
                            
                            # Risk Assessment
                            if "risk_assessment" in analysis_results:
                                with st.expander("🚨 Risk Assessment", expanded=True):
                                    try:
                                        if isinstance(analysis_results["risk_assessment"], dict):
                                            st.json(analysis_results["risk_assessment"])
                                        else:
                                            st.markdown(str(analysis_results["risk_assessment"]))
                                    except Exception:
                                        st.markdown(str(analysis_results["risk_assessment"]))
                            
                            # Summary
                            st.markdown("## Summary")
                            st.info("Analysis completed successfully. Review the detailed findings in each section above.")
                            
                            # Add download option for the full analysis
                            combined_analysis = {
                                "document_name": uploaded_file.name,
                                "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "analysis_results": analysis_results
                            }
                            
                            # Convert to JSON for download
                            analysis_json = json.dumps(combined_analysis, indent=2)
                            st.download_button(
                                label="Download Full Analysis Report",
                                data=analysis_json,
                                file_name=f"analysis-{uploaded_file.name.split('.')[0]}.json",
                                mime="application/json"
                            )
                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
                            with st.expander("Detailed Error Information"):
                                st.write(traceback.format_exc())
    
    # Information about the analysis process
    with st.expander("How It Works", expanded=False):
        st.markdown("""
        ### Our Analysis Process

        1. **Document Parsing**
           - Extracts text from your uploaded contract
           - Identifies key sections and clauses
           
        2. **Legal Compliance Review**
           - Analyzes compliance with relevant regulations (GDPR, CCPA, etc.)
           - Identifies potential compliance issues
           
        3. **Risk Assessment**
           - Evaluates financial, operational, and security risks
           - Provides recommendations for risk mitigation
           
        ### The Team Behind the Analysis

        Our system uses a crew of AI agents specialized in different aspects of contract analysis:

        - **Document Parsing Specialist**: Extracts and structures key contract information
        - **Legal Compliance Expert**: Analyzes contracts for legal and regulatory compliance
        - **Risk Assessment Specialist**: Identifies and quantifies business risks
        
        This system is built with CrewAI, an orchestration framework for agentic workflows.
        """)

if __name__ == "__main__":
    main() 