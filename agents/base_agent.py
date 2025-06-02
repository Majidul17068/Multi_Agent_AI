from crewai import Agent

def create_base_agent(name, role, goal, backstory, llm):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        llm=llm
    )
