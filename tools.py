from langchain.tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Optional, Type, Annotated, ClassVar
import os
import json
from utils.document_parser import parse_document, chunk_text

class ContractParsingInput(BaseModel):
    """Input for contract parsing tool."""
    contract_text: str = Field(..., description="The text content of the contract to parse")

class ContractParsingTool(BaseTool):
    """Tool for parsing contracts and extracting structured information."""
    name: ClassVar[str] = "contract_parsing_tool"
    description: ClassVar[str] = "Parses contract text and extracts key information such as parties, dates, terms, etc."
    args_schema: Type[BaseModel] = ContractParsingInput
    
    def _run(self, contract_text: str) -> str:
        """Run the contract parsing tool."""
        # If the contract is too long, chunk it and process in parts
        if len(contract_text) > 12000:
            chunks = chunk_text(contract_text, chunk_size=8000)
            results = []
            for i, chunk in enumerate(chunks):
                results.append(f"Analyzing chunk {i+1} of {len(chunks)}...")
                # Process each chunk - in a real tool, you'd do more here
            return json.dumps({"status": "success", "message": f"Contract analyzed in {len(chunks)} chunks"})
        else:
            # Process the entire contract
            return json.dumps({
                "status": "success", 
                "message": "Contract analyzed successfully",
                "length": len(contract_text)
            })

class ComplianceDatabaseInput(BaseModel):
    """Input for compliance database search tool."""
    query: str = Field(..., description="The compliance requirement or term to search for")
    jurisdiction: Optional[str] = Field(None, description="Specific jurisdiction to search regulations for")

class ComplianceDatabaseTool(BaseTool):
    """Tool for searching compliance requirements in different jurisdictions."""
    name: ClassVar[str] = "compliance_database_tool"
    description: ClassVar[str] = "Search for legal compliance requirements for specific terms or jurisdictions."
    args_schema: Type[BaseModel] = ComplianceDatabaseInput
    
    def _run(self, query: str, jurisdiction: Optional[str] = None) -> str:
        """Run the compliance database search tool."""
        # In a real implementation, this would query a compliance database
        compliance_data = {
            "GDPR": {
                "data_processing": "Requires explicit consent and right to be forgotten",
                "data_breach": "Must be reported within 72 hours"
            },
            "CCPA": {
                "data_collection": "Must disclose what personal information is collected",
                "opt_out": "Must provide a way to opt-out of data sale"
            }
        }
        
        results = {}
        if jurisdiction and jurisdiction.upper() in compliance_data:
            results[jurisdiction.upper()] = compliance_data[jurisdiction.upper()]
        else:
            # Search all jurisdictions
            for jur, reqs in compliance_data.items():
                for term, desc in reqs.items():
                    if query.lower() in term.lower() or query.lower() in desc.lower():
                        if jur not in results:
                            results[jur] = {}
                        results[jur][term] = desc
        
        return json.dumps(results)

class RiskEvaluationInput(BaseModel):
    """Input for risk evaluation tool."""
    contract_clause: str = Field(..., description="The specific contract clause to evaluate for risks")
    risk_type: Optional[str] = Field(None, description="Specific type of risk to evaluate (e.g., financial, operational)")

class RiskEvaluationTool(BaseTool):
    """Tool for evaluating the risk level of specific contract clauses."""
    name: ClassVar[str] = "risk_evaluation_tool"
    description: ClassVar[str] = "Evaluates the risk level of specific contract clauses."
    args_schema: Type[BaseModel] = RiskEvaluationInput
    
    def _run(self, contract_clause: str, risk_type: Optional[str] = None) -> str:
        """Run the risk evaluation tool."""
        # In a real implementation, this would use more sophisticated analysis
        risk_levels = {
            "financial": "medium",
            "operational": "low",
            "security": "high",
            "legal": "medium"
        }
        
        analysis = {
            "clause_length": len(contract_clause),
            "identified_risks": {}
        }
        
        # Simple risk evaluation based on keywords
        risk_keywords = {
            "financial": ["payment", "fee", "cost", "penalty", "compensation"],
            "operational": ["service", "performance", "availability", "uptime"],
            "security": ["data", "breach", "confidential", "secure", "encrypt"],
            "legal": ["liability", "indemnify", "warrant", "comply", "jurisdict"]
        }
        
        # Evaluate risks
        for risk_category, keywords in risk_keywords.items():
            if risk_type and risk_category != risk_type.lower():
                continue
                
            risk_score = 0
            for keyword in keywords:
                if keyword.lower() in contract_clause.lower():
                    risk_score += 1
            
            if risk_score > 0:
                level = "low"
                if risk_score >= 3:
                    level = "high"
                elif risk_score >= 2:
                    level = "medium"
                    
                analysis["identified_risks"][risk_category] = {
                    "level": level,
                    "score": risk_score,
                    "keywords_found": [k for k in keywords if k.lower() in contract_clause.lower()]
                }
        
        return json.dumps(analysis) 