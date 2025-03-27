from crewai import Agent, LLM, Tool
from typing import List, Optional
from langchain.tools import BaseTool
import os
from dotenv import load_dotenv

# Import tools
from tools import ContractParsingTool, ComplianceDatabaseTool, RiskEvaluationTool

# Load environment variables
load_dotenv()

# Create LLM configuration
if os.getenv("AZURE_OPENAI_API_KEY"):
    # Using the direct configuration approach for Azure OpenAI
    try:
        azure_model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        llm = LLM(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            model=f"azure/{azure_model_name}",
            temperature=0.1
        )
        print(f"Using Azure OpenAI deployment '{azure_model_name}' for agents")
    except Exception as e:
        print(f"Error configuring Azure OpenAI: {str(e)}")
        if os.getenv("OPENAI_API_KEY"):
            # Fallback to standard OpenAI
            llm = LLM(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o-mini",
                temperature=0.1
            )
            print("Falling back to standard OpenAI for agents")
        else:
            raise ValueError("No valid LLM configuration found. Please set up Azure OpenAI or standard OpenAI API keys.")
# Fallback to standard OpenAI
elif os.getenv("OPENAI_API_KEY"):
    llm = LLM(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.1
    )
    print("Using standard OpenAI for agents")
else:
    raise ValueError("No valid LLM configuration found. Please set up Azure OpenAI or standard OpenAI API keys.")

# Convert LangChain tools to CrewAI tools
def convert_to_crewai_tool(tool_instance):
    """
    Convert a LangChain BaseTool instance to a CrewAI Tool
    """
    return Tool(
        name=tool_instance.name,
        description=tool_instance.description,
        func=tool_instance._run
    )

def create_document_parsing_agent(tools: Optional[List[BaseTool]] = None) -> Agent:
    """
    Create an agent specialized in document parsing and information extraction.
    
    Args:
        tools: Optional list of tools for the agent to use
        
    Returns:
        Agent: CrewAI agent for document parsing
    """
    # Initialize default tools if none provided
    if tools is None:
        # Create the default tool and convert it to a CrewAI tool
        parsing_tool = ContractParsingTool()
        crewai_tools = [convert_to_crewai_tool(parsing_tool)]
    else:
        # Convert the provided tools to CrewAI tools
        crewai_tools = [convert_to_crewai_tool(tool) for tool in tools]
    
    return Agent(
        role="Document Parsing Specialist",
        goal="Extract and structure key information from IT contract documents with high accuracy",
        backstory="""
        You are an expert in document analysis with a specialization in IT contracts. 
        You have years of experience extracting and organizing information from complex legal documents.
        Your ability to identify key sections, clauses, and terms in contracts is unmatched.
        You can quickly scan through lengthy documents and extract the most relevant details.
        """,
        tools=crewai_tools,
        verbose=True,
        llm=llm
    )

def create_legal_compliance_agent(tools: Optional[List[BaseTool]] = None) -> Agent:
    """
    Create an agent specialized in legal compliance analysis.
    
    Args:
        tools: Optional list of tools for the agent to use
        
    Returns:
        Agent: CrewAI agent for legal compliance analysis
    """
    # Initialize default tools if none provided
    if tools is None:
        # Create the default tool and convert it to a CrewAI tool
        compliance_tool = ComplianceDatabaseTool()
        crewai_tools = [convert_to_crewai_tool(compliance_tool)]
    else:
        # Convert the provided tools to CrewAI tools
        crewai_tools = [convert_to_crewai_tool(tool) for tool in tools]
    
    return Agent(
        role="Legal Compliance Expert",
        goal="Identify legal compliance issues and risks in IT contracts with comprehensive recommendations",
        backstory="""
        You are a highly experienced legal expert specializing in IT and technology contracts.
        With a background in technology law, you've advised numerous companies on compliance 
        issues related to software licensing, data protection, and service agreements.
        You have a keen eye for identifying problematic clauses and compliance risks in contracts.
        Your expertise ensures organizations avoid legal pitfalls in their technology agreements.
        """,
        tools=crewai_tools,
        verbose=True,
        llm=llm
    )

def create_risk_analysis_agent(tools: Optional[List[BaseTool]] = None) -> Agent:
    """
    Create an agent specialized in risk analysis and assessment.
    
    Args:
        tools: Optional list of tools for the agent to use
        
    Returns:
        Agent: CrewAI agent for risk analysis
    """
    # Initialize default tools if none provided
    if tools is None:
        # Create the default tool and convert it to a CrewAI tool
        risk_tool = RiskEvaluationTool()
        crewai_tools = [convert_to_crewai_tool(risk_tool)]
    else:
        # Convert the provided tools to CrewAI tools
        crewai_tools = [convert_to_crewai_tool(tool) for tool in tools]
    
    return Agent(
        role="Risk Assessment Specialist",
        goal="Evaluate business and operational risks in IT contracts with actionable mitigation strategies",
        backstory="""
        You are a senior risk analyst with expertise in IT contract risk management.
        You have helped numerous organizations identify and mitigate risks in their
        technology agreements. Your experience spans various industries, giving you 
        a broad perspective on risk patterns and effective mitigation strategies.
        You systematically identify, analyze, and prioritize risks based on their 
        potential impact and likelihood.
        """,
        tools=crewai_tools,
        verbose=True,
        llm=llm
    ) 