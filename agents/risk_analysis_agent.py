from crewai import Agent
from langchain_community.tools import BaseTool
from typing import Optional, Type
import os

# Try to import Azure OpenAI first, fallback to standard OpenAI
try:
    from utils.azure_openai_config import get_azure_openai_client
    get_llm = get_azure_openai_client
except ImportError:
    from utils.openai_fallback import get_openai_client
    get_llm = get_openai_client

class RiskAnalysisAgent:
    """
    Agent responsible for assessing business risks in IT contracts.
    """
    
    @staticmethod
    def create(tools: Optional[list[BaseTool]] = None):
        """
        Create a risk analysis agent with optional tools
        
        Args:
            tools: Optional list of tools to provide to the agent
            
        Returns:
            Risk analysis agent
        """
        return Agent(
            role="Risk Assessment Specialist",
            goal="Evaluate business and operational risks in IT contracts",
            backstory="""
            You are a senior risk analyst with expertise in IT contract risk management.
            You have helped numerous organizations identify and mitigate risks in their
            technology agreements. Your experience spans various industries, giving you 
            a broad perspective on risk patterns and effective mitigation strategies.
            You systematically identify, analyze, and prioritize risks based on their 
            potential impact and likelihood.
            """,
            tools=tools or [],  # Use provided tools or empty list if None
            verbose=True,
            allow_delegation=False,
            llm=get_llm(),
        )
    
    @staticmethod
    def risk_assessment_task(parsed_contract, compliance_analysis):
        """
        Create a task for assessing contract risks.
        
        Args:
            parsed_contract: The structured contract information from the parsing agent
            compliance_analysis: The compliance analysis from the legal agent
            
        Returns:
            A risk assessment task
        """
        return f"""
        Conduct a comprehensive risk assessment of the IT contract based on the following information:
        
        PARSED CONTRACT INFORMATION:
        {parsed_contract}
        
        LEGAL COMPLIANCE ANALYSIS:
        {compliance_analysis}
        
        Your risk assessment should cover:
        1. Financial risks (e.g., cost overruns, hidden fees, payment terms)
        2. Operational risks (e.g., service disruptions, poor performance)
        3. Strategic risks (e.g., vendor lock-in, misalignment with business objectives)
        4. Reputational risks (e.g., security breaches, performance failures)
        5. Security and data risks (e.g., data breaches, unauthorized access)
        6. Vendor risks (e.g., vendor stability, resource capabilities)
        7. Exit and transition risks (e.g., contract termination obstacles)
        
        For each identified risk:
        - Assign a risk level (High, Medium, Low)
        - Calculate potential business impact (Financial, Operational, Strategic, Reputational)
        - Suggest practical risk mitigation strategies
        - Provide actionable recommendations for contract negotiation
        
        Finally, provide an overall risk score (1-10) for the contract and summarize the top 3-5 critical
        risk areas that need immediate attention.
        
        Format the output as a structured JSON object with categories for different risk areas and a
        summary section with the overall risk assessment.
        """ 