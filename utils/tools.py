from typing import List, Dict
import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from utils.config import SUPPORTED_LANGUAGES, SEARCH_ENGINE_URL, NEWS_SOURCES, DEFAULT_NEWS_COUNT
import urllib.parse
import re
from functools import lru_cache

class TranslationTool:
    def __init__(self):
        # Initialize GoogleTranslator instance directly
        self.translator = GoogleTranslator(source='auto')
        # Cache for translations
        self._translation_cache = {}

    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text to target language with caching"""
        if not text or not text.strip():
            return text

        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language. Supported languages: {list(SUPPORTED_LANGUAGES.keys())}")
        
        # Check if text is already in target language
        if target_lang == 'en' and all(ord(c) < 128 for c in text):
            return text
        
        # Use cached translation if available
        cache_key = f"{text}_{target_lang}"
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        
        try:
            # Set target language
            self.translator.target = target_lang
            
            # Split long text into smaller chunks for better performance
            max_chunk_size = 5000  # Google Translate's limit
            chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            
            # Translate chunks and combine results
            translated_chunks = []
            for chunk in chunks:
                try:
                    translated = self.translator.translate(chunk)
                    translated_chunks.append(translated)
                except Exception as e:
                    print(f"Error translating chunk: {e}")
                    translated_chunks.append(chunk)  # Keep original text if translation fails
            
            result = ' '.join(translated_chunks)
            
            # Cache the result
            self._translation_cache[cache_key] = result
            return result
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def clear_cache(self):
        """Clear the translation cache"""
        self._translation_cache.clear()

class WebSearchTool:
    def __init__(self):
        self.search_url = SEARCH_ENGINE_URL
        self.news_sources = NEWS_SOURCES
        self.default_count = DEFAULT_NEWS_COUNT
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _construct_search_query(self, topic: str, location: str = None) -> str:
        """Construct a search query for news articles"""
        # Add site restrictions for reliable news sources
        site_restrictions = " OR ".join([f"site:{site}" for site in self.news_sources])
        
        # Build the query with proper formatting
        query_parts = [topic]
        if location:
            query_parts.append(location)
        
        # Add news-specific terms
        query_parts.extend(["news", "latest", "recent"])
        
        # Combine all parts
        query = " ".join(query_parts)
        
        # Add site restrictions
        query = f"{query} ({site_restrictions})"
        
        return urllib.parse.quote(query)

    def _extract_news_links(self, html_content: str) -> List[Dict[str, str]]:
        """Extract news article links and titles from search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        news_items = []
        
        # Find all search result containers
        for result in soup.find_all(['div', 'article'], class_=['g', 'SoaBEf']):
            # Try to find the main link
            link = result.find('a')
            if not link or not link.get('href'):
                continue
                
            url = link.get('href')
            # Skip if not a valid URL
            if not url.startswith('http'):
                continue
                
            # Get title
            title = result.find(['h3', 'h4'])
            if not title:
                continue
                
            # Get snippet/description
            snippet = result.find(['div', 'span'], class_=['VwiC3b', 'yXK7lf'])
            description = snippet.text if snippet else ""
            
            # Get source and date if available
            source_div = result.find(['div', 'span'], class_=['UPmit', 'yXK7lf'])
            source = source_div.text if source_div else ""
            
            # Only include if it's from a trusted source
            if any(source_name in url.lower() for source_name in self.news_sources):
                news_items.append({
                    'title': title.text.strip(),
                    'url': url,
                    'description': description.strip(),
                    'source': source.strip()
                })
        
        return news_items

    def search_news(self, topic: str, location: str = None, count: int = None) -> List[Dict[str, str]]:
        """Search for news articles based on topic and location"""
        try:
            query = self._construct_search_query(topic, location)
            
            # Add news-specific parameters to the URL
            params = {
                'q': query,
                'tbm': 'nws',  # News search
                'tbs': 'qdr:d',  # Last day
                'hl': 'en',  # Language
                'num': count or self.default_count  # Number of results
            }
            
            # Construct the full URL with parameters
            url = f"{self.search_url}?{urllib.parse.urlencode(params)}"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            news_items = self._extract_news_links(response.text)
            
            # Sort by source reliability (prioritize major news sources)
            priority_sources = ['reuters.com', 'apnews.com', 'bbc.com']
            news_items.sort(key=lambda x: any(source in x['url'].lower() for source in priority_sources), reverse=True)
            
            return news_items[:count or self.default_count]
            
        except Exception as e:
            print(f"Error searching news: {e}")
            return []

class WebScrapingTool:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_text_from_url(self, url: str) -> str:
        """Extract text content from a webpage"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error scraping webpage: {e}")
            return ""

    def scrape_webpage(self, url: str) -> str:
        """
        Scrape content from a webpage.
        Args:
            url: The URL to scrape
        Returns:
            The scraped content as a string
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract the main content
            # Try to find the main article content
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=['content', 'article', 'post'])
            
            if article:
                # Get all paragraphs from the article
                paragraphs = article.find_all('p')
                content = '\n\n'.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            else:
                # Fallback to getting all paragraphs
                paragraphs = soup.find_all('p')
                content = '\n\n'.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            
            # Get the title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Get the publication date if available
            date = None
            date_elements = soup.find_all(['time', 'span', 'div'], class_=['date', 'published', 'timestamp'])
            for element in date_elements:
                if element.get('datetime'):
                    date = element['datetime']
                    break
                elif element.get_text().strip():
                    date = element.get_text().strip()
                    break
            
            # Format the result
            result = f"Title: {title_text}\n"
            if date:
                result += f"Date: {date}\n"
            result += f"\nContent:\n{content}"
            
            return result
            
        except requests.RequestException as e:
            return f"Error scraping webpage: {str(e)}"
        except Exception as e:
            return f"Error processing webpage content: {str(e)}" 