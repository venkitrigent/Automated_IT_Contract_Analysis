# Automated IT Contract Analysis

A powerful agentic framework built with CrewAI and Streamlit to analyze IT contracts, extract insights, and assess compliance and risk factors.

## Features

- **Document Parsing**: Extracts key information from IT contracts (parties, dates, terms, etc.)
- **Legal Compliance Analysis**: Identifies potential compliance issues and legal risks
- **Risk Assessment**: Evaluates business and operational risks with mitigation recommendations
- **Flexible LLM Support**: Works with both Azure OpenAI and standard OpenAI
- **User-Friendly Interface**: Simple Streamlit UI for document upload and analysis

## Getting Started

### Prerequisites

- Python 3.8+ (Python 3.12 recommended)
- OpenAI API key (or Azure OpenAI credentials)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Automated_IT_Contract_Analysis.git
   cd Automated_IT_Contract_Analysis
   ```

2. Run the installation script:
   ```
   bash run.sh
   ```

   This script will:
   - Create a virtual environment
   - Install dependencies
   - Set up a template .env file for your API keys
   - Start the application

### Configuration

Create a `.env` file in the project root with your API credentials:

```
# For Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# For standard OpenAI (fallback)
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the application:
   ```
   bash run.sh
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload an IT contract document (PDF or text)

4. Review the analysis results:
   - Contract details extraction
   - Compliance analysis
   - Risk assessment

## Example Contracts

The `data` directory contains example IT contracts for testing:

- Software Development Agreement
- IT Service Level Agreement (SLA)
- Software Licensing Agreement

## Project Structure

```
Automated_IT_Contract_Analysis/
├── agents/                 # Agent definitions
│   ├── document_parsing_agent.py
│   ├── legal_compliance_agent.py
│   ├── risk_analysis_agent.py
│   └── __init__.py
├── data/                   # Example contract documents
├── utils/                  # Utility modules
│   ├── azure_openai_config.py
│   ├── openai_fallback.py
│   ├── contract_analysis_crew.py
│   └── __init__.py
├── app.py                  # Streamlit application
├── requirements.txt        # Project dependencies
├── run.sh                  # Installation and startup script
└── .env                    # Configuration (add your API keys)
```

## Troubleshooting

### Package Installation Issues

If you encounter issues with package installation:

1. The `run.sh` script will automatically attempt to install compatible versions
2. If Azure OpenAI installation fails, the application will fall back to standard OpenAI
3. Check the terminal output for specific error messages and recommendations

### API Connection Issues

1. Verify your API keys in the `.env` file
2. Check internet connectivity
3. Ensure your Azure OpenAI resource is properly configured with appropriate deployments

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework for building agentic workflows
- [Streamlit](https://streamlit.io/) - Framework for building data applications
- [Azure OpenAI](https://azure.microsoft.com/services/cognitive-services/openai-service/) - Microsoft's OpenAI service 