import streamlit as st
import json
import time
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.document_parser import parse_document
from agents.contract_analysis_crew import ContractAnalysisCrew

# Try to import Azure OpenAI
try:
    from utils.azure_openai_config import get_azure_openai_client, get_native_azure_client
    USING_AZURE = True
except ImportError:
    # Fallback to standard OpenAI
    from utils.openai_fallback import get_openai_client, get_native_openai_client
    USING_AZURE = False
    print("Using standard OpenAI instead of Azure OpenAI due to import error")

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
</style>
""", unsafe_allow_html=True)

def validate_llm_config():
    """Validate the LLM configuration and return status"""
    if USING_AZURE:
        # Azure OpenAI validation
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return False, f"Missing environment variables: {', '.join(missing_vars)}"
        
        # Test connection to Azure OpenAI
        try:
            client = get_native_azure_client()
            # Simple test to see if the client is working
            models = client.models.list()
            return True, "Azure OpenAI configuration is valid."
        except Exception as e:
            return False, f"Error connecting to Azure OpenAI: {str(e)}"
    else:
        # Standard OpenAI validation
        if not os.getenv("OPENAI_API_KEY"):
            # Try to use Azure key as fallback
            if os.getenv("AZURE_OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
            else:
                return False, "Missing OPENAI_API_KEY environment variable"
                
        # Test connection to OpenAI
        try:
            client = get_native_openai_client()
            # Simple test to see if the client is working
            models = client.models.list()
            return True, "OpenAI configuration is valid."
        except Exception as e:
            return False, f"Error connecting to OpenAI: {str(e)}"

def main():
    # Title and description
    st.title("📄 Automated IT Contract Analysis")
    
    # Show banner for OpenAI vs Azure OpenAI
    if USING_AZURE:
        st.success("Using Azure OpenAI for analysis")
    else:
        st.warning("Using standard OpenAI API for analysis (Azure OpenAI not available)")
    
    # Check LLM Configuration
    config_valid, config_message = validate_llm_config()
    
    if not config_valid:
        st.error(f"LLM Configuration Error: {config_message}")
        if USING_AZURE:
            st.info("Please check your .env file and ensure all required Azure OpenAI variables are set correctly.")
        else:
            st.info("Please set the OPENAI_API_KEY environment variable in your .env file.")
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
                        
                        # Simulate incremental progress while analysis is happening
                        crew = ContractAnalysisCrew()
                        
                        # Start analysis in a way that allows us to update progress
                        for i, step in enumerate(progress_steps):
                            progress_text.text(step)
                            progress_bar.progress((i+1)/len(progress_steps))
                            
                            # Only do the actual analysis once
                            if i == 0:
                                try:
                                    analysis_results = crew.analyze_contract(document_info["text"])
                                except Exception as e:
                                    st.error(f"Error during analysis: {str(e)}")
                                    st.info("If you're seeing OpenAI API errors, please check your API key and quota limits.")
                                    return
                            else:
                                # Simulate processing time for other steps
                                time.sleep(1)
                        
                        # Analysis complete
                        progress_bar.progress(100)
                        progress_text.text("Analysis complete!")
                        
                        # Display results
                        st.markdown("## Analysis Results")
                        
                        # Contract Data
                        if analysis_results["contract_data"]:
                            with st.expander("📋 Contract Information", expanded=True):
                                try:
                                    contract_data = json.loads(analysis_results["contract_data"]) if isinstance(analysis_results["contract_data"], str) else analysis_results["contract_data"]
                                    st.json(contract_data)
                                except Exception as e:
                                    st.text_area("Contract Data", analysis_results["contract_data"], height=300)
                        
                        # Compliance Analysis
                        if analysis_results["compliance_analysis"]:
                            with st.expander("⚖️ Compliance Analysis", expanded=True):
                                st.markdown(analysis_results["compliance_analysis"])
                        
                        # Risk Assessment
                        if analysis_results["risk_assessment"]:
                            with st.expander("🚨 Risk Assessment", expanded=True):
                                st.markdown(analysis_results["risk_assessment"])
                        
                        # Summary
                        st.markdown("## Summary")
                        st.info("Analysis completed successfully. Review the detailed findings in each section above.")
                        
                        # Add download option for the full analysis
                        combined_analysis = {
                            "document_name": uploaded_file.name,
                            "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "contract_data": analysis_results["contract_data"],
                            "compliance_analysis": analysis_results["compliance_analysis"],
                            "risk_assessment": analysis_results["risk_assessment"]
                        }
                        
                        # Convert to JSON for download
                        analysis_json = json.dumps(combined_analysis, indent=2)
                        st.download_button(
                            label="Download Full Analysis Report",
                            data=analysis_json,
                            file_name=f"analysis-{uploaded_file.name.split('.')[0]}.json",
                            mime="application/json"
                        )
    
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

        Our system uses advanced AI agents specialized in different aspects of contract analysis:

        - **Document Parsing Agent**: Extracts and structures key contract information
        - **Legal Compliance Agent**: Ensures contracts meet regulatory requirements
        - **Risk Analysis Agent**: Identifies and quantifies business risks
        """)

if __name__ == "__main__":
    main() 