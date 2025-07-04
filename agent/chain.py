from langchain.agents import create_tool_calling_agent, AgentExecutor

def create_agent_chain(llm, tools, prompt):
    """
    Creates the agent chain (AgentExecutor).
    """
    # Agent Initialization
    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )
    return agent_executor
