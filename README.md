# Multi-Agent AI Chatbot

A sophisticated multi-agent AI system built with CrewAI, featuring specialized agents for content summarization, headline generation, news analysis, translation, and semantic search. This project leverages the power of Groq LLM and provides a user-friendly Streamlit interface.

## 🚀 Features

### Core Functionalities
- **Content Summarization**: Generate concise summaries while preserving original meaning
- **Headline Creation**: Create engaging, attention-grabbing headlines
- **News Analysis**: Search and analyze recent news articles from reliable sources
- **Text Translation**: Professional translation with cultural context awareness
- **Semantic Search**: Find similar content using vector embeddings

### Key Capabilities
- **Multi-language Support**: Native support for English and Bengali
- **Real-time Web Search**: Access to current news and information
- **Vector Storage**: ChromaDB integration for efficient content retrieval
- **Cultural Sensitivity**: Context-aware translations and content processing
- **Modular Architecture**: Extensible agent-based system

## 🏗️ Architecture

The project follows a modular, agent-based architecture:

```
├── agents/           # Specialized AI agents
│   ├── domain_agents.py    # Agent definitions and configurations
│   └── base_agent.py       # Base agent class
├── utils/            # Utility modules and tools
│   ├── tools.py           # Web search, scraping, and translation tools
│   ├── vector_store.py    # ChromaDB integration
│   ├── text_processor.py  # Text processing utilities
│   └── config.py          # Configuration management
├── main.py           # Streamlit application entry point
├── groq_llm.py       # Groq LLM configuration
└── requirements.txt  # Python dependencies
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Majidul17068/Multi_Agent_AI.git
   cd Multi_Agent_AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 🎯 Usage

### Web Interface
Access the application through your web browser at `http://localhost:8501`

### Available Functions

#### 1. Content Summarization
- Input: Any text content
- Output: Concise summary in the original language
- Features: Maintains context and key information

#### 2. Headline Generation
- Input: Article or content text
- Output: Engaging headline (5-10 words)
- Features: Language-aware, culturally appropriate

#### 3. News Analysis
- Input: Topic and optional location
- Output: Curated list of recent news articles
- Features: Real-time search, reliable sources, detailed summaries

#### 4. Text Translation
- Input: Text and target language
- Output: Natural, culturally-aware translation
- Features: Chunk-based processing, refinement for Bengali

#### 5. Semantic Search
- Input: Query text
- Output: Similar content from stored documents
- Features: Vector-based similarity search

## 🤖 Agents Overview

### Specialized Agents

| Agent | Role | Capabilities |
|-------|------|--------------|
| **Summarizer Agent** | Content Summarizer | Distills complex information into clear summaries |
| **Headline Agent** | Headline Creator | Creates engaging, accurate headlines |
| **News Analyst Agent** | News Analyst | Finds and analyzes news from reliable sources |
| **Translator Agent** | Professional Translator | Provides culturally-aware translations |

### Agent Tools
- **Translation Tool**: Multi-language translation capabilities
- **Web Search Tool**: Real-time news and information search
- **Web Scraping Tool**: Content extraction from web pages
- **Vector Store**: Semantic search and content storage

## 🔧 Configuration

### Environment Variables
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Customization
- Modify agent behaviors in `agents/domain_agents.py`
- Add new tools in `utils/tools.py`
- Configure vector store settings in `utils/vector_store.py`

## 📊 Dependencies

### Core Dependencies
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and tool management
- **Streamlit**: Web application interface
- **ChromaDB**: Vector database for semantic search
- **Groq**: High-performance LLM provider

### Key Libraries
- `deep-translator`: Translation capabilities
- `beautifulsoup4`: Web scraping
- `sentence-transformers`: Text embeddings
- `python-dotenv`: Environment management

## 🚀 Performance Features

- **Chunk-based Processing**: Handles large texts efficiently
- **Vector Embeddings**: Fast semantic search capabilities
- **Caching**: Optimized response times
- **Error Handling**: Robust error management and recovery

## 🔒 Security & Privacy

- API keys stored in environment variables
- No sensitive data logged or stored
- Secure web scraping practices
- Privacy-conscious content processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI Team**: For the excellent multi-agent framework
- **Groq**: For high-performance LLM services
- **LangChain**: For LLM integration tools
- **Streamlit**: For the web application framework

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the code comments
- Review the configuration files for customization options

## 🔄 Version History

- **v1.0.0**: Initial release with core multi-agent functionality
- Features: Summarization, headlines, news analysis, translation, semantic search

---

**Built with ❤️ using CrewAI, Groq, and Streamlit** 