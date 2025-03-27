from crewai import Task
from typing import Optional
from agents import create_document_parsing_agent, create_legal_compliance_agent, create_risk_analysis_agent

def create_contract_extraction_task(contract_text: str) -> Task:
    """
    Create a task for extracting information from a contract.
    
    Args:
        contract_text: The text content of the contract document
        
    Returns:
        Task: CrewAI task for contract extraction
    """
    return Task(
        description=f"""
        Analyze the following IT contract and extract key information in a structured format:
        
        {contract_text}
        
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
        """,
        expected_output="""
        A structured JSON object containing key information extracted from the contract,
        including parties, dates, terms, and clauses.
        """,
        agent=create_document_parsing_agent()
    )

def create_compliance_analysis_task() -> Task:
    """
    Create a task for analyzing legal compliance in a contract.
    
    Returns:
        Task: CrewAI task for compliance analysis
    """
    return Task(
        description="""
        Analyze the parsed contract information for legal compliance issues and risks.
        
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
        """,
        expected_output="""
        A comprehensive compliance analysis in JSON format that identifies legal issues,
        potential risks, and provides actionable recommendations.
        """,
        agent=create_legal_compliance_agent(),
        context=[create_contract_extraction_task]  # This will be dynamically replaced with actual task
    )

def create_risk_assessment_task() -> Task:
    """
    Create a task for assessing business and operational risks in a contract.
    
    Returns:
        Task: CrewAI task for risk assessment
    """
    return Task(
        description="""
        Conduct a comprehensive risk assessment of the IT contract based on the parsed contract
        information and compliance analysis.
        
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
        """,
        expected_output="""
        A detailed risk assessment in JSON format that quantifies risks, provides
        mitigation strategies, and highlights critical areas requiring attention.
        """,
        agent=create_risk_analysis_agent(),
        context=[create_contract_extraction_task, create_compliance_analysis_task]  # Will be replaced with actual tasks
    ) 