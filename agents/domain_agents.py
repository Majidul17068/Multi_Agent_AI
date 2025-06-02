from crewai import Agent
from groq_llm import llm
from utils.tools import TranslationTool, WebSearchTool, WebScrapingTool
from langchain.tools import Tool

# Initialize tools
translation_tool = TranslationTool()
web_search_tool = WebSearchTool()
web_scraping_tool = WebScrapingTool()

def create_base_agent(role: str, goal: str, backstory: str, tools: list = None) -> Agent:
    # Convert tools to langchain Tool format if provided
    langchain_tools = []
    if tools:
        for tool in tools:
            if isinstance(tool, TranslationTool):
                langchain_tools.append(
                    Tool(
                        name="translate_text",
                        func=tool.translate_text,
                        description="Translate text to a target language"
                    )
                )
            elif isinstance(tool, WebSearchTool):
                langchain_tools.append(
                    Tool(
                        name="search_news",
                        func=tool.search_news,
                        description="Search for news articles based on topic and location"
                    )
                )
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=langchain_tools,
        verbose=True,
        llm=llm  # Explicitly set the LLM to our Groq instance
    )

# Create Langchain tools
search_tool = Tool(
    name="search_news",
    func=web_search_tool.search_news,
    description="Search for news articles based on a topic and optional location"
)

scrape_tool = Tool(
    name="scrape_webpage",
    func=web_scraping_tool.scrape_webpage,
    description="Scrape content from a webpage URL"
)

# News Analyst Agent
news_analyst_agent = Agent(
    role="News Analyst",
    goal="Find and analyze relevant news articles from reliable sources",
    backstory="""You are an experienced news analyst with expertise in finding and analyzing news articles.
    You have a strong understanding of reliable news sources and can quickly identify high-quality content.
    You are skilled at summarizing news articles while maintaining accuracy and objectivity.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
    llm=llm
)

# Define specialized agents
tutor_agent = create_base_agent(
    role="Tutor",
    goal="Help students understand complex topics through clear explanations and examples",
    backstory="""You are an experienced tutor with a passion for teaching. 
    You excel at breaking down complex concepts into simple, understandable parts."""
)

analyst_agent = create_base_agent(
    role="Analyst",
    goal="Analyze data and provide insights",
    backstory="""You are a skilled data analyst with expertise in interpreting complex information 
    and drawing meaningful conclusions."""
)

summarizer_agent = create_base_agent(
    role="Content Summarizer",
    goal="Create clear and concise summaries while maintaining the original meaning",
    backstory="""You are an expert at distilling complex information into clear, concise summaries. 
    You have a keen eye for identifying key points and maintaining the essence of the original content."""
)

headline_agent = create_base_agent(
    role="Headline Creator",
    goal="Create engaging and accurate headlines that capture the essence of the content",
    backstory="""You are a skilled headline writer with experience in creating attention-grabbing, 
    accurate headlines that effectively communicate the main message."""
)

translator_agent = create_base_agent(
    role="Professional Translator",
    goal="Provide accurate and natural translations while maintaining cultural context",
    backstory="""You are a professional translator with expertise in multiple languages. 
    You excel at providing accurate translations that maintain the original meaning while being natural 
    and culturally appropriate in the target language. You pay special attention to grammar, tone, 
    and cultural nuances.""",
    tools=[translation_tool]
)
