from crewai import Crew, Process
from tasks import create_contract_extraction_task, create_compliance_analysis_task, create_risk_assessment_task

class ContractAnalysisCrew:
    """
    Crew for analyzing IT contracts, extracting key insights, and assessing compliance and risks.
    """
    
    @staticmethod
    def create_crew(contract_text: str) -> Crew:
        """
        Create a crew to analyze a contract.
        
        Args:
            contract_text: The text content of the contract to analyze
            
        Returns:
            Crew: A configured CrewAI crew for contract analysis
        """
        # Create tasks with the contract text
        contract_extraction = create_contract_extraction_task(contract_text)
        compliance_analysis = create_compliance_analysis_task()
        risk_assessment = create_risk_assessment_task()
        
        # Update the context of downstream tasks
        compliance_analysis.context = [contract_extraction]
        risk_assessment.context = [contract_extraction, compliance_analysis]
        
        # Create and return the crew
        return Crew(
            tasks=[contract_extraction, compliance_analysis, risk_assessment],
            process=Process.sequential,  # Execute tasks in order
            verbose=True,
        )
    
    @staticmethod
    def analyze_contract(contract_text: str) -> dict:
        """
        Analyze a contract document and return structured insights.
        
        Args:
            contract_text: The text content of the contract to analyze
            
        Returns:
            dict: Analysis results with contract details, compliance issues, and risks
        """
        # Create the crew
        crew = ContractAnalysisCrew.create_crew(contract_text)
        
        # Execute the crew's tasks
        results = crew.kickoff()
        
        # Structure and return the results
        try:
            # Try to convert any string results to JSON if possible
            import json
            
            contract_details = results[0]
            compliance_analysis = results[1]
            risk_assessment = results[2]
            
            # Try to parse JSON responses
            try:
                if isinstance(contract_details, str):
                    contract_details = ContractAnalysisCrew._extract_json(contract_details)
            except:
                pass
                
            try:
                if isinstance(compliance_analysis, str):
                    compliance_analysis = ContractAnalysisCrew._extract_json(compliance_analysis)
            except:
                pass
                
            try:
                if isinstance(risk_assessment, str):
                    risk_assessment = ContractAnalysisCrew._extract_json(risk_assessment)
            except:
                pass
            
            return {
                "contract_details": contract_details,
                "compliance_analysis": compliance_analysis,
                "risk_assessment": risk_assessment
            }
        except Exception as e:
            # If there's an error processing the results, return raw results
            return {
                "contract_details": results[0],
                "compliance_analysis": results[1],
                "risk_assessment": results[2],
                "error": f"Failed to structure results: {str(e)}"
            }
    
    @staticmethod
    def _extract_json(text):
        """
        Extract JSON data from text that might contain additional content.
        
        Args:
            text: Text containing JSON data
            
        Returns:
            Parsed JSON data or original text if parsing fails
        """
        import json
        import re
        
        try:
            # Try to find JSON content within the text
            json_pattern = r'(\{.*\})'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            if matches:
                # Find the largest JSON object (likely the main result)
                largest_match = max(matches, key=len)
                return json.loads(largest_match)
            
            # If no JSON-like content found or parsing fails, try the whole text
            return json.loads(text)
        except:
            # If JSON parsing fails, return the original text
            return text 