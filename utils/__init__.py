# Utility modules for IT Contract Analysis
from utils.document_parser import parse_document, chunk_text
from utils.contract_analysis_crew import ContractAnalysisCrew

# Dynamic imports for OpenAI configuration
try:
    from utils.azure_openai_config import get_azure_openai_client, get_native_azure_client
except ImportError:
    from utils.openai_fallback import get_openai_client, get_native_openai_client

__all__ = [
    'parse_document',
    'chunk_text',
    'get_azure_openai_client'
] 