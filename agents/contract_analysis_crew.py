from crewai import Crew, Task, Process
from agents.document_parsing_agent import DocumentParsingAgent
from agents.legal_compliance_agent import LegalComplianceAgent
from agents.risk_analysis_agent import RiskAnalysisAgent
from utils.document_parser import chunk_text

class ContractAnalysisCrew:
    """
    Crew that orchestrates the contract analysis workflow using multiple specialized agents.
    """
    
    def __init__(self, tools=None):
        """
        Initialize the contract analysis crew
        
        Args:
            tools: Optional dictionary of tools by agent type
                   {'document_parsing': [...], 'legal_compliance': [...], 'risk_analysis': [...]}
        """
        # Setup tools for each agent type
        tools = tools or {}
        document_parsing_tools = tools.get('document_parsing', [])
        legal_compliance_tools = tools.get('legal_compliance', [])
        risk_analysis_tools = tools.get('risk_analysis', [])
        
        # Create the agents
        self.document_parsing_agent = DocumentParsingAgent.create(tools=document_parsing_tools)
        self.legal_compliance_agent = LegalComplianceAgent.create(tools=legal_compliance_tools)
        self.risk_analysis_agent = RiskAnalysisAgent.create(tools=risk_analysis_tools)
        
    def analyze_contract(self, document_text):
        """
        Analyze a contract document using a sequence of specialized agents.
        
        Args:
            document_text: The text content of the contract document
            
        Returns:
            The combined analysis results from all agents
        """
        # Handle large documents by chunking if necessary
        if len(document_text) > 25000:  # If document is very large
            chunks = chunk_text(document_text)
            document_text = chunks[0]  # Use first chunk for initial analysis
            # Could implement more sophisticated chunking handling here
        
        # Create the tasks
        document_extraction_task = Task(
            description=DocumentParsingAgent.contract_extraction_task(document_text),
            agent=self.document_parsing_agent,
            expected_output="A structured JSON object containing key contract information"
        )
        
        # Create a lambda function to generate the description with the context
        compliance_task_description = lambda context: LegalComplianceAgent.compliance_analysis_task(context[0].output)
        
        compliance_analysis_task = Task(
            description=compliance_task_description,
            agent=self.legal_compliance_agent,
            context=[document_extraction_task],
            expected_output="A detailed compliance analysis of the contract"
        )
        
        # Create a lambda function to generate the description with the context
        risk_task_description = lambda context: RiskAnalysisAgent.risk_assessment_task(
            context[0].output, context[1].output
        )
        
        risk_assessment_task = Task(
            description=risk_task_description,
            agent=self.risk_analysis_agent,
            context=[document_extraction_task, compliance_analysis_task],
            expected_output="A comprehensive risk assessment of the contract with mitigation strategies"
        )
        
        # Create the crew
        crew = Crew(
            agents=[
                self.document_parsing_agent,
                self.legal_compliance_agent,
                self.risk_analysis_agent
            ],
            tasks=[
                document_extraction_task,
                compliance_analysis_task,
                risk_assessment_task
            ],
            verbose=2,
            process=Process.sequential  # Execute tasks in sequence
        )
        
        # Run the analysis
        result = crew.kickoff()
        
        return {
            "contract_data": document_extraction_task.output if hasattr(document_extraction_task, 'output') else None,
            "compliance_analysis": compliance_analysis_task.output if hasattr(compliance_analysis_task, 'output') else None,
            "risk_assessment": risk_assessment_task.output if hasattr(risk_assessment_task, 'output') else None,
            "final_result": result
        }