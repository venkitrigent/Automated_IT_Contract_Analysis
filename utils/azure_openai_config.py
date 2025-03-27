import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load environment variables
load_dotenv()

def get_azure_openai_model():
    """
    Returns a configured Azure OpenAI model for use with LangChain/CrewAI.
    
    Returns:
        AzureChatOpenAI: Configured Azure OpenAI language model
    """
    # Check for required environment variables
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    
    # Setup Azure OpenAI model
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0.0,  # Lower temperature for more consistent responses
    )

def get_azure_openai_client():
    """
    Provides guidance on how to directly configure the CrewAI LLM for Azure OpenAI.
    
    Example usage:
    ```python
    from crewai import LLM
    
    llm = LLM(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        model="azure/your-deployment-name",
        temperature=0.1
    )
    ```
    
    Returns:
        None: This function provides documentation only
    """
    # Check for required environment variables
    required_env_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")
    
    # This function doesn't return a client, just provides guidance
    return None

def get_native_azure_client():
    """
    This function is a placeholder that explains how to use Azure OpenAI with CrewAI.
    The recommended way to use Azure OpenAI with CrewAI is to use the LLM class with direct configuration:
    
    from crewai import LLM
    
    # Create LLM with direct parameters instead of environment variables
    llm = LLM(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        model="azure/your-deployment-name",
        temperature=0.1
    )
    
    Returns:
        None: This function is a placeholder for documentation
    """
    return None 