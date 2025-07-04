import os
from langchain_openai import ChatOpenAI
from .tools import get_tools
from .prompts import get_agent_prompt
from .chain import create_agent_chain

def get_openai_api_key():
    """Gets the OpenAI API key from environment variables."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai_api_key

def create_agent(model_name: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    Creates and returns the Novelix agent executor.

    Args:
        model_name (str): The name of the OpenAI model to use.
        temperature (float): The temperature for the LLM's output generation.

    Returns:
        The agent executor.
    """
    # Ensure API keys are set
    get_openai_api_key()
    # The Tavily API key is checked within the tool itself.

    # 1. LLM Configuration
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    # 2. Tools
    tools = get_tools()

    # 3. Agent Prompt
    prompt = get_agent_prompt()

    # 4. Create Agent Chain (Executor)
    agent_executor = create_agent_chain(llm, tools, prompt)

    return agent_executor
