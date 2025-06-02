import streamlit as st
from crewai import Crew, Task
from agents.domain_agents import (
    summarizer_agent,
    headline_agent,
    news_analyst_agent,
    translator_agent
)
from utils.tools import TranslationTool, WebSearchTool, WebScrapingTool
from groq_llm import llm
from utils.vector_store import vector_store
from datetime import datetime
from utils.text_processor import split_into_chunks, combine_chunks, get_text_stats, format_stats
import json

# Initialize tools
translation_tool = TranslationTool()
web_search_tool = WebSearchTool()
web_tool = WebScrapingTool()

def create_summarization_task(content: str) -> Task:
    # Store the content in ChromaDB for future reference
    vector_store.add_documents(
        documents=[content],
        metadatas=[{"type": "content", "timestamp": str(datetime.now())}]
    )
    
    return Task(
        description=f"""Summarize the following content in its original language.
        If the content is in Bengali, create a Bengali summary.
        If the content is in English, create an English summary.
        Keep the summary clear, concise, and in the same language as the input.
        
        Content:
        {content}""",
        expected_output="A well-structured summary in the same language as the input content",
        agent=summarizer_agent
    )

def create_headline_task(content: str) -> Task:
    # Detect if the content is in Bengali
    is_bengali = any(ord(c) > 127 for c in content)
    
    task_description = f"""Create a short, impactful headline (5-10 words) for the following content.
    The headline should be in the same language as the input content.
    Focus on the main topic and key message.
    Make it engaging and attention-grabbing.
    
    Content:
    {content}"""

    if is_bengali:
        task_description += """
        
        Since the content is in Bengali:
        1. Create the headline in Bengali
        2. Ensure proper Bengali grammar and sentence structure
        3. Use natural Bengali expressions
        4. Maintain cultural appropriateness
        5. Use proper Bengali punctuation"""

    return Task(
        description=task_description,
        expected_output="A concise, engaging headline of 5-10 words in the same language as the input content",
        agent=headline_agent
    )

def create_news_analysis_task(query: str, location: str = None) -> Task:
    return Task(
        description=f"""Search for recent news articles about '{query}' {f'in {location}' if location else ''}.
        Use the web search tool to find relevant news articles from reliable sources.
        For each article found, use the web scraping tool to extract detailed content.
        
        Requirements:
        1. Find at least 5 relevant news articles
        2. Focus on recent news (last 24 hours)
        3. Prioritize major news sources (Reuters, AP, BBC, etc.)
        4. Ensure content directly relates to the topic and location
        
        For each article, provide:
        1. Article title
        2. Source name
        3. Publication date
        4. Article URL (as a clickable link)
        5. A brief summary (2-3 sentences)
        
        Format your response as a markdown list with clear sections for each article.
        Example format:
        ### Article 1
        **Title:** [Article Title]
        **Source:** [Source Name]
        **Date:** [Publication Date]
        **URL:** [Clickable Link]
        **Summary:** [Brief summary]
        
        If you cannot find enough recent articles, explain why and provide what you found.""",
        expected_output="""A well-formatted list of news articles, each containing:
        - Title
        - Source
        - Publication date
        - URL
        - Brief summary
        All formatted in markdown with proper sections and clickable links.""",
        agent=news_analyst_agent
    )

def create_translation_task(text: str, target_lang: str) -> Task:
    # Split text into chunks
    chunks = split_into_chunks(text)
    stats = get_text_stats(text)
    
    # Create chunk text with proper formatting
    chunk_text = ""
    for i, chunk in enumerate(chunks):
        chunk_text += f"Chunk {i+1}:\n{chunk}\n\n"
    
    task_description = f"""Translate the following text to {target_lang}.
    Text Statistics: {format_stats(stats)}
    The text has been split into {len(chunks)} chunks for better processing.
    First, use the translation tool to perform the initial translation of each chunk.
    Then, analyze and refine the translations to ensure they are natural and culturally appropriate.
    
    Text chunks to translate:
    {chunk_text}"""

    # Add special instructions for Bengali translations
    if target_lang == "bn":
        task_description += """
        
        For Bengali translations:
        1. First, use the translation tool to get the initial translation of each chunk
        2. Then, analyze each Bengali chunk and improve it to:
           - Make it more natural and well-mannered
           - Use proper Bengali grammar and sentence structure
           - Ensure cultural appropriateness
           - Maintain formal tone where appropriate
           - Use proper Bengali punctuation and formatting
        3. Finally, combine all chunks into a coherent text
        
        Format your response exactly as follows:
        Initial Translations:
        [paste the initial translations from the translation tool here, chunk by chunk]
        
        Refined Translation:
        [paste your refined and combined version here]"""

    return Task(
        description=task_description,
        expected_output="A natural and accurate translation in the target language, with additional refinement for Bengali translations",
        agent=translator_agent
    )

def save_translation(text: str, translation: str, target_lang: str) -> None:
    """Save translation to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"translation_{target_lang}_{timestamp}.json"
    
    data = {
        "original_text": text,
        "translation": translation,
        "target_language": target_lang,
        "timestamp": timestamp
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename

def main():
    st.title("Multi-Agent AI Chatbot")
    st.write("Choose a functionality and provide the necessary input:")

    # Sidebar for functionality selection
    functionality = st.sidebar.selectbox(
        "Select Functionality",
        ["Summarize Content", "Create Headline", "Analyze News", "Translate Text", "Search Similar Content"]
    )

    if functionality == "Summarize Content":
        content = st.text_area("Enter content to summarize:", height=200)
        if st.button("Summarize"):
            if content:
                with st.spinner("Generating summary..."):
                    try:
                        task = create_summarization_task(content)
                        crew = Crew(agents=[summarizer_agent], tasks=[task], verbose=True)
                        result = crew.kickoff()
                        st.success("Summary:")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                        st.info("Please try again with different content.")
            else:
                st.warning("Please enter some content to summarize.")

    elif functionality == "Create Headline":
        content = st.text_area("Enter content for headline:", height=200)
        if st.button("Generate Headline"):
            if content:
                with st.spinner("Generating headline..."):
                    try:
                        task = create_headline_task(content)
                        crew = Crew(agents=[headline_agent], tasks=[task], verbose=True)
                        result = crew.kickoff()
                        st.success("Generated Headline:")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Error generating headline: {str(e)}")
                        st.info("Please try again with different content.")
            else:
                st.warning("Please enter some content for the headline.")

    elif functionality == "Analyze News":
        query = st.text_input("Enter news topic or keywords:")
        location = st.text_input("Enter location (optional, e.g., US, UK, India):")
        if st.button("Analyze News"):
            if query:
                with st.spinner("Searching for news articles..."):
                    task = create_news_analysis_task(query, location if location else None)
                    crew = Crew(agents=[news_analyst_agent], tasks=[task], verbose=True)
                    result = crew.kickoff()
                    
                    # Display results in a more organized way
                    st.success("News Analysis Results:")
                    st.markdown(result)
            else:
                st.warning("Please enter a news topic or keywords.")

    elif functionality == "Translate Text":
        text = st.text_area("Enter text to translate:", height=200)
        
        # Show text statistics
        if text:
            stats = get_text_stats(text)
            st.info(format_stats(stats))
            
            # Warning for very long texts
            if stats["characters"] > 10000:
                st.warning("This is a long text. Translation may take some time.")
        
        target_lang = st.selectbox(
            "Select target language",
            ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "bn"],
            format_func=lambda x: {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese",
                "ru": "Russian",
                "zh": "Chinese",
                "ja": "Japanese",
                "ko": "Korean",
                "bn": "Bengali"
            }[x]
        )
        
        if st.button("Translate"):
            if text:
                try:
                    # Clear translation cache if it gets too large
                    if len(translation_tool._translation_cache) > 1000:
                        translation_tool.clear_cache()
                    
                    # Split text into chunks
                    chunks = split_into_chunks(text)
                    
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Translate each chunk
                    translated_chunks = []
                    for i, chunk in enumerate(chunks):
                        status_text.text(f"Translating chunk {i+1} of {len(chunks)}...")
                        translated_chunk = translation_tool.translate_text(chunk, target_lang)
                        translated_chunks.append(translated_chunk)
                        progress_bar.progress((i + 1) / len(chunks))
                    
                    # Store translations in vector store for RAG
                    vector_store.add_documents(
                        documents=translated_chunks,
                        metadatas=[{
                            "type": "translation",
                            "chunk_index": i,
                            "target_lang": target_lang,
                            "timestamp": str(datetime.now())
                        } for i in range(len(translated_chunks))]
                    )
                    
                    # Create and run the task for refinement
                    task = create_translation_task(text, target_lang)
                    crew = Crew(agents=[translator_agent], tasks=[task], verbose=True)
                    result = crew.kickoff()
                    
                    # Display results differently for Bengali translations
                    if target_lang == "bn":
                        st.success("Translation Results:")
                        if "Initial Translations:" in result and "Refined Translation:" in result:
                            initial = result.split("Initial Translations:")[1].split("Refined Translation:")[0].strip()
                            refined = result.split("Refined Translation:")[1].strip()
                            
                            st.markdown("### Initial Translations")
                            st.write(initial)
                            st.markdown("### Refined Translation")
                            st.write(refined)
                            
                            # Save translation
                            filename = save_translation(text, refined, target_lang)
                            st.download_button(
                                label="Download Translation",
                                data=json.dumps({
                                    "original": text,
                                    "initial_translations": initial,
                                    "refined_translation": refined
                                }, ensure_ascii=False, indent=2),
                                file_name=filename,
                                mime="application/json"
                            )
                        else:
                            st.write(result)
                    else:
                        st.success("Translation:")
                        st.write(result)
                        
                        # Save translation
                        filename = save_translation(text, result, target_lang)
                        st.download_button(
                            label="Download Translation",
                            data=json.dumps({
                                "original": text,
                                "translation": result
                            }, ensure_ascii=False, indent=2),
                            file_name=filename,
                            mime="application/json"
                        )
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
                    st.info("Please try again with a shorter text or different language.")
            else:
                st.warning("Please enter some text to translate.")

    elif functionality == "Search Similar Content":
        query = st.text_input("Enter search query:")
        if st.button("Search"):
            if query:
                with st.spinner("Searching for similar content..."):
                    try:
                        results = vector_store.search(query)
                        st.success("Similar Content Found:")
                        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                            st.markdown(f"### Result {i+1}")
                            st.write("Content:")
                            st.write(doc)
                            st.write("Metadata:", metadata)
                    except Exception as e:
                        st.error(f"Error searching content: {str(e)}")
                        st.info("Please try again with a different query.")
            else:
                st.warning("Please enter a search query.")

if __name__ == "__main__":
    main()
