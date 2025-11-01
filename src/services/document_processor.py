"""
Document processing and chunking service.
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config


class DocumentProcessor:
    """Handles document loading and chunking."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
    
    def load_document(self, file_path: str) -> str:
        """Load document from file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_sections(self, text: str) -> List[tuple]:
        """
        Extract sections from document based on numbered headers.
        Returns list of (section_title, section_content) tuples.
        """
        sections = []
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check if line starts with a number (section header)
            if line.strip() and line.strip()[0].isdigit() and '.' in line[:3]:
                # Save previous section
                if current_section:
                    sections.append((
                        current_section,
                        '\n'.join(current_content).strip()
                    ))
                
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                if line.strip():  # Skip empty lines
                    current_content.append(line)
        
        # Add last section
        if current_section:
            sections.append((
                current_section,
                '\n'.join(current_content).strip()
            ))
        
        return sections
    
    def process_document(self, text: str, source: str = "market_report") -> List[Document]:
        """
        Process document into chunks with metadata.
        
        Args:
            text: Document text
            source: Source identifier
            
        Returns:
            List of Document objects with metadata
        """
        sections = self.extract_sections(text)
        documents = []
        
        for section_title, section_content in sections:
            # Skip empty sections
            if not section_content:
                continue
            
            # Create chunks for this section
            chunks = self.text_splitter.create_documents(
                texts=[section_content],
                metadatas=[{
                    "section": section_title,
                    "source": source,
                    "doc_type": "market_research"
                }]
            )
            documents.extend(chunks)
        
        return documents
    
    def get_full_document(self, file_path: str) -> str:
        """Get full document text for summarization and extraction."""
        return self.load_document(file_path)