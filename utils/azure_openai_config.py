import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from openai import AzureOpenAI

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
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.0,  # Use 0 temperature for more consistent/factual responses
    )
    
    return client

def get_native_azure_client():
    """
    Create a native Azure OpenAI client using environment variables.
    
    Returns:
        AzureOpenAI client (native OpenAI SDK)
    """
    # Check for required environment variables
    required_env_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    
    # Set up native Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    return client 