"""
Test script for Azure OpenAI integration with CrewAI
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Tool
from crewai import Process

# Load environment variables
load_dotenv()

def test_azure_llm():
    """Test Azure OpenAI integration with CrewAI"""
    
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("No Azure OpenAI API key found. Please set up your .env file.")
        return
    
    try:
        print("Setting up Azure OpenAI LLM...")
        azure_model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        
        # Use the direct configuration approach
        llm = LLM(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            model=f"azure/{azure_model_name}",
            temperature=0.1
        )
        
        print(f"Using Azure OpenAI deployment '{azure_model_name}'")
        
        # Create a simple CrewAI Tool (not LangChain BaseTool)
        search_tool = Tool(
            name="search_tool",
            description="Search for information about a topic",
            func=lambda topic: f"Found information about {topic}"
        )
        
        # Create a simple agent
        agent = Agent(
            role="Test Agent",
            goal="Test Azure OpenAI integration with CrewAI",
            backstory="You are a test agent designed to verify Azure OpenAI integration with CrewAI.",
            verbose=True,
            llm=llm,
            tools=[search_tool]  # Using the CrewAI tool directly
        )
        
        # Create a simple task
        task = Task(
            description="Search for information about AI ethics and write a brief paragraph.",
            expected_output="A paragraph about AI ethics.",
            agent=agent
        )
        
        # Create a crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=2
        )
        
        # Run the crew
        print("Running the crew...")
        result = crew.kickoff()
        
        print("\nResult:")
        print(result)
        
        print("\nAzure OpenAI integration test completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error testing Azure OpenAI integration: {str(e)}")
        return False

if __name__ == "__main__":
    test_azure_llm() 