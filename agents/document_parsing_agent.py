from crewai import Agent
from langchain_community.tools import BaseTool
from typing import Optional, Type
import os

# Try to import Azure OpenAI first, fallback to standard OpenAI
try:
    from utils.azure_openai_config import get_azure_openai_client
    get_llm = get_azure_openai_client
    print("Successfully loaded Azure OpenAI client for document parsing")
except ImportError as e:
    print(f"Failed to import Azure OpenAI: {str(e)}")
    from utils.openai_fallback import get_openai_client
    get_llm = get_openai_client
    print("Falling back to standard OpenAI client for document parsing")

class DocumentParsingAgent:
    """
    Agent responsible for parsing and extracting key information from IT contracts.
    """
    
    @staticmethod
    def create(tools: Optional[list[BaseTool]] = None):
        """
        Create a document parsing agent with optional tools
        
        Args:
            tools: Optional list of tools to provide to the agent
            
        Returns:
            Document parsing agent
        """
        # Initialize LLM with appropriate error handling
        try:
            llm = get_llm()
            print(f"Document Parsing Agent using LLM: {type(llm).__name__}")
        except Exception as e:
            print(f"Error initializing LLM for Document Parsing Agent: {str(e)}")
            raise
            
        return Agent(
            role="Document Parsing Specialist",
            goal="Extract and structure key information from IT contract documents",
            backstory="""
            You are an expert in document analysis with a specialization in IT contracts. 
            You have years of experience extracting and organizing information from complex legal documents.
            Your ability to identify key sections, clauses, and terms in contracts is unmatched.
            You can quickly scan through lengthy documents and extract the most relevant details.
            """,
            tools=tools or [],  # Use provided tools or empty list if None
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
    
    @staticmethod
    def contract_extraction_task(document_text):
        """
        Create a task for extracting key contract information.
        
        Args:
            document_text: The text content of the contract document
            
        Returns:
            A structured extraction task
        """
        return f"""
        Analyze the following IT contract document and extract the key information in a structured format:
        
        {document_text}
        
        Extract and organize the following elements:
        1. Contract parties (names of all organizations involved)
        2. Contract effective date and termination date
        3. Contract type (e.g., SaaS, software license, maintenance, consulting)
        4. Contract value and payment terms
        5. Key deliverables or services
        6. SLAs or performance metrics
        7. Termination conditions
        8. Intellectual property clauses
        9. Data handling and privacy clauses
        10. Any unique or unusual clauses
        
        Format the output as a structured JSON object with these categories as keys.
        """ 