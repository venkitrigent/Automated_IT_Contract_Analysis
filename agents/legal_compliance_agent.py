from crewai import Agent
from langchain_community.tools import BaseTool
from typing import Optional, Type
import os

# Try to import Azure OpenAI first, fallback to standard OpenAI
try:
    from utils.azure_openai_config import get_azure_openai_client
    get_llm = get_azure_openai_client
    print("Successfully loaded Azure OpenAI client for legal compliance")
except ImportError as e:
    print(f"Failed to import Azure OpenAI: {str(e)}")
    from utils.openai_fallback import get_openai_client
    get_llm = get_openai_client
    print("Falling back to standard OpenAI client for legal compliance")

class LegalComplianceAgent:
    """
    Agent responsible for analyzing contracts for legal compliance and potential issues.
    """
    
    @staticmethod
    def create(tools: Optional[list[BaseTool]] = None):
        """
        Create a legal compliance agent with optional tools
        
        Args:
            tools: Optional list of tools to provide to the agent
            
        Returns:
            Legal compliance agent
        """
        # Initialize LLM with appropriate error handling
        try:
            llm = get_llm()
            print(f"Legal Compliance Agent using LLM: {type(llm).__name__}")
        except Exception as e:
            print(f"Error initializing LLM for Legal Compliance Agent: {str(e)}")
            raise
            
        return Agent(
            role="Legal Compliance Expert",
            goal="Identify legal compliance issues and risks in IT contracts",
            backstory="""
            You are a highly experienced legal expert specializing in IT and technology contracts.
            With a background in technology law, you've advised numerous companies on compliance 
            issues related to software licensing, data protection, and service agreements.
            You have a keen eye for identifying problematic clauses and compliance risks in contracts.
            Your expertise ensures organizations avoid legal pitfalls in their technology agreements.
            """,
            tools=tools or [],  # Use provided tools or empty list if None
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    @staticmethod
    def compliance_analysis_task(parsed_contract):
        """
        Create a task for analyzing contract compliance.
        
        Args:
            parsed_contract: The structured contract information from the parsing agent
            
        Returns:
            A compliance analysis task
        """
        return f"""
        Analyze the following parsed IT contract information for legal compliance issues and risks:
        
        {parsed_contract}
        
        Specifically evaluate:
        1. GDPR and data privacy compliance
        2. Intellectual property protections
        3. Liability and indemnification clauses
        4. Service level agreement enforceability
        5. Termination and exit provisions
        6. Regulatory compliance specific to IT services
        7. Security and data breach provisions
        8. Force majeure clauses
        9. Jurisdictional issues
        10. Any vague or ambiguous language
        
        For each compliance issue identified, explain:
        - The specific problematic clause or gap
        - The potential legal risk
        - Recommendation for addressing the issue
        
        Format the output as a structured JSON object with categories for different compliance areas.
        """ 