#!/bin/bash

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip

# First try: Install with requirements.txt
pip install -r requirements.txt

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Trying alternative approach..."
    
    # Try with a more flexible requirements file
    echo "Creating temporary flexible requirements file..."
    cat > requirements_flexible.txt << EOF
streamlit>=1.25.0
crewai>=0.20.0
python-dotenv>=0.19.0
openai>=1.10.0
langchain>=0.0.267
langchain-openai>=0.0.2
langchain-community>=0.0.10
pydantic>=2.0.0
pypdf>=3.15.0
docx2txt>=0.8
pandas>=1.5.0
azure-identity>=1.10.0
EOF
    
    echo "Installing with flexible requirements..."
    pip install -r requirements_flexible.txt
    
    # Install Azure OpenAI SDK directly with pip
    echo "Attempting to install Azure OpenAI SDK directly..."
    pip install azure-openai
    
    # If that fails, try the OpenAI SDK without Azure specifics
    if [ $? -ne 0 ]; then
        echo "Azure OpenAI SDK installation failed. Using standard OpenAI SDK instead."
        echo "You may need to modify the code to use the standard OpenAI client."
        
        # Create a file to indicate we're using alternative setup
        touch .using_alternative_setup
    fi
    
    # Check if the overall installation worked
    if [ $? -ne 0 ]; then
        echo "Error installing dependencies. Please check your Python environment and try again."
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating a template .env file..."
    cat > .env << EOF
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your_resource_name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Standard OpenAI (used as fallback)
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo "Please edit the .env file with your Azure OpenAI or standard OpenAI credentials before running the application."
    echo "For Azure OpenAI, make sure to set:"
    echo "1. AZURE_OPENAI_API_KEY - Your Azure OpenAI API key"
    echo "2. AZURE_OPENAI_ENDPOINT - Your Azure OpenAI endpoint URL"
    echo "3. AZURE_OPENAI_DEPLOYMENT_NAME - The deployment name of your model"
    echo "4. AZURE_OPENAI_API_VERSION - The API version (recommended: 2024-02-15-preview)"
    exit 1
fi

# Run the Streamlit app
echo "Starting the IT Contract Analysis application..."
streamlit run app.py

# Deactivate the virtual environment when the app is closed
deactivate 