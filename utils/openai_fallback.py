import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def get_openai_client():
    """
    Create a standard OpenAI client using environment variables.
    This is a fallback if Azure OpenAI is not available.
    
    Returns:
        ChatOpenAI configured client for LangChain
    """
    # Check for required environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            # Try to use Azure key if OpenAI key is not available
            if var == "OPENAI_API_KEY" and os.getenv("AZURE_OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
            else:
                raise ValueError(f"Missing required environment variable: {var}")
    
    # Set up OpenAI client for LangChain
    client = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
        temperature=0.0,  # Use 0 temperature for more consistent/factual responses
    )
    
    return client

def get_native_openai_client():
    """
    Create a native OpenAI client using environment variables.
    This is a fallback if Azure OpenAI is not available.
    
    Returns:
        OpenAI client (native OpenAI SDK)
    """
    # Check for required environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            # Try to use Azure key if OpenAI key is not available
            if var == "OPENAI_API_KEY" and os.getenv("AZURE_OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
            else:
                raise ValueError(f"Missing required environment variable: {var}")
    
    # Set up native OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    return client 