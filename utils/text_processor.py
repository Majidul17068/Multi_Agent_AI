from typing import List, Dict, Tuple
import re
from datetime import datetime

def split_into_chunks(text: str, max_chunk_size: int = 5000) -> List[str]:
    """
    Split text into chunks while trying to maintain sentence boundaries.
    Args:
        text: The text to split
        max_chunk_size: Maximum size of each chunk
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    # Split into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # If a single sentence is longer than max_chunk_size, split it further
        if len(sentence) > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split long sentence into smaller parts
            words = sentence.split()
            temp_chunk = []
            temp_size = 0
            
            for word in words:
                if temp_size + len(word) + 1 <= max_chunk_size:
                    temp_chunk.append(word)
                    temp_size += len(word) + 1
                else:
                    if temp_chunk:
                        chunks.append(' '.join(temp_chunk))
                    temp_chunk = [word]
                    temp_size = len(word)
            
            if temp_chunk:
                chunks.append(' '.join(temp_chunk))
            continue
        
        # Normal case: add sentence to current chunk if it fits
        if current_size + len(sentence) + 1 <= max_chunk_size:
            current_chunk.append(sentence)
            current_size += len(sentence) + 1
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = len(sentence)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def combine_chunks(chunks: List[str]) -> str:
    """Combine chunks back into a single text."""
    return ' '.join(chunks)

def get_text_stats(text: str) -> Dict[str, int]:
    """
    Get statistics about the text.
    Returns:
        Dictionary containing character count, word count, and sentence count
    """
    if not text:
        return {"characters": 0, "words": 0, "sentences": 0}
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    words = text.split()
    
    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences)
    }

def process_batch(texts: List[str], max_chunk_size: int = 5000) -> List[Tuple[str, List[str], Dict[str, int]]]:
    """
    Process a batch of texts, returning chunks and statistics for each.
    Args:
        texts: List of texts to process
        max_chunk_size: Maximum size of each chunk
    Returns:
        List of tuples containing (original_text, chunks, stats)
    """
    results = []
    for text in texts:
        chunks = split_into_chunks(text, max_chunk_size)
        stats = get_text_stats(text)
        results.append((text, chunks, stats))
    return results

def format_stats(stats: Dict[str, int]) -> str:
    """Format statistics into a readable string."""
    return f"Characters: {stats['characters']:,} | Words: {stats['words']:,} | Sentences: {stats['sentences']:,}" 