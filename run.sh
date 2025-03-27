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

# Copy .env.template to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "⚠️ Please edit the .env file with your API keys before running the application."
fi

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
langchain>=0.0.267
langchain-community>=0.0.10
langchain-openai>=0.0.2
python-dotenv>=0.19.0
openai>=1.10.0
pydantic>=1.10.8
pypdf>=3.15.0
docx2txt>=0.8
pandas>=1.5.0
EOF
    
    echo "Installing with flexible requirements..."
    pip install -r requirements_flexible.txt
    
    # Try to install Azure OpenAI SDK
    echo "Attempting to install Azure OpenAI SDK..."
    pip install azure-openai || true
    
    # Check if the overall installation worked
    if [ $? -ne 0 ]; then
        echo "Error installing dependencies. Please check your Python environment and try again."
        exit 1
    fi
fi

# Check for required configuration
if ! grep -q "AZURE_OPENAI_API_KEY=" .env | grep -v "^#"; then
    if ! grep -q "OPENAI_API_KEY=" .env | grep -v "^#"; then
        echo "⚠️ Warning: No API keys found in .env file."
        echo "You need to configure either:"
        echo "1. Azure OpenAI (AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME)"
        echo "2. OpenAI (OPENAI_API_KEY)"
        echo "Please edit the .env file before running the application."
        
        # Don't exit here, let the app handle the error with better UI
    fi
fi

# Run the Streamlit app
echo "Starting the IT Contract Analysis application..."
streamlit run app.py

# Deactivate the virtual environment when the app is closed
deactivate 