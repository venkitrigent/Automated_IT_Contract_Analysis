import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from langchain_openai import AzureChatOpenAI
import azure.ai.openai as azure_openai

# Load environment variables
load_dotenv()

def get_azure_openai_client():
    """
    Create an Azure OpenAI client using environment variables.
    
    Returns:
        AzureChatOpenAI configured client for LangChain
    """
    # Check for required environment variables
    required_env_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    
    # Set up Azure OpenAI client for LangChain
    client = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0.0,  # Use 0 temperature for more consistent/factual responses
    )
    
    return client

def get_native_azure_client():
    """
    Create a native Azure OpenAI client using environment variables.
    
    Returns:
        AzureOpenAI client (native Azure SDK)
    """
    # Check for required environment variables
    required_env_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    
    # Set up native Azure OpenAI client
    client = azure_openai.AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    return client 