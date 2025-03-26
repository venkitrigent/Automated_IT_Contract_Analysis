from crewai import Crew, Process, Task
from agents.document_parsing_agent import DocumentParsingAgent
from agents.legal_compliance_agent import LegalComplianceAgent
from agents.risk_analysis_agent import RiskAnalysisAgent
import json

class ContractAnalysisCrew:
    """
    Crew responsible for analyzing IT contracts, extracting key insights,
    and assessing legal compliance and business risks.
    """
    
    @staticmethod
    def create():
        """
        Create a contract analysis crew with all necessary agents
        
        Returns:
            Contract analysis crew
        """
        # Create agents
        document_parser = DocumentParsingAgent.create()
        legal_compliance = LegalComplianceAgent.create()
        risk_analyst = RiskAnalysisAgent.create()
        
        # Create the crew
        return Crew(
            agents=[document_parser, legal_compliance, risk_analyst],
            tasks=[],  # Tasks will be added dynamically
            process=Process.sequential,
            verbose=True,
        )
    
    @staticmethod
    def analyze_contract(crew, contract_text):
        """
        Analyze an IT contract document
        
        Args:
            crew: The contract analysis crew
            contract_text: The text content of the contract
            
        Returns:
            Analysis results as a dictionary with parsing, compliance, and risk data
        """
        # Reset crew tasks
        crew.tasks = []
        
        # Create tasks for analysis
        parsing_task = Task(
            description=DocumentParsingAgent.contract_extraction_task(contract_text),
            agent=crew.agents[0]
        )
        
        compliance_task = Task(
            description=lambda parsing_output: LegalComplianceAgent.compliance_analysis_task(parsing_output),
            agent=crew.agents[1],
            context=[parsing_task]
        )
        
        risk_task = Task(
            description=lambda parsing_output, compliance_output: 
                RiskAnalysisAgent.risk_assessment_task(parsing_output, compliance_output),
            agent=crew.agents[2],
            context=[parsing_task, compliance_task]
        )
        
        # Add tasks to crew
        crew.tasks = [parsing_task, compliance_task, risk_task]
        
        # Execute the analysis
        results = crew.kickoff()
        
        # Process and structure results
        try:
            # Attempt to parse JSON from each result
            parsing_results = ContractAnalysisCrew._extract_json(results[0])
            compliance_results = ContractAnalysisCrew._extract_json(results[1])
            risk_results = ContractAnalysisCrew._extract_json(results[2])
            
            # Create structured output
            analysis_results = {
                "contract_details": parsing_results,
                "compliance_analysis": compliance_results,
                "risk_assessment": risk_results
            }
            
            return analysis_results
        
        except Exception as e:
            # Return raw results if JSON parsing fails
            return {
                "contract_details": results[0],
                "compliance_analysis": results[1],
                "risk_assessment": results[2],
                "error": f"Failed to structure results: {str(e)}"
            }
    
    @staticmethod
    def _extract_json(text):
        """
        Extract JSON data from text that might contain additional content
        
        Args:
            text: Text containing JSON data
            
        Returns:
            Parsed JSON data or original text if parsing fails
        """
        try:
            # Try to find JSON content within the text
            # Look for content between { and } with the most content
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx+1]
                return json.loads(json_str)
            
            # If no JSON-like content found, return the original text
            return text
        
        except json.JSONDecodeError:
            # If JSON parsing fails, return the original text
            return text 