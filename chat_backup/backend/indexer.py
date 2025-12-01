"""
Document indexer for the AI Native Book
Indexes all markdown/mdx files from the book into Qdrant
"""

import os
import re
from pathlib import Path
from typing import List, Dict
import markdown
from bs4 import BeautifulSoup
from rag_service import RAGService
from dotenv import load_dotenv

load_dotenv()

class DocumentIndexer:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.rag_service = RAGService()
        self.md = markdown.Markdown(extensions=['meta', 'fenced_code'])

    def extract_frontmatter(self, content: str) -> tuple[Dict, str]:
        """Extract YAML frontmatter from markdown"""
        frontmatter = {}
        body = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Parse frontmatter
                fm_lines = parts[1].strip().split('\n')
                for line in fm_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
                body = parts[2].strip()

        return frontmatter, body

    def clean_markdown(self, content: str) -> str:
        """Convert markdown to clean text"""
        # Remove code blocks but keep their content
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Convert markdown to HTML then to text
        html = self.md.convert(content)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def chunk_document(self, content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split document into overlapping chunks"""
        words = content.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def index_file(self, file_path: Path):
        """Index a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter and body
            frontmatter, body = self.extract_frontmatter(content)

            # Get title
            title = frontmatter.get('title', '')
            if not title:
                # Try to extract from first heading
                match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
                if match:
                    title = match.group(1)
                else:
                    title = file_path.stem

            # Clean and chunk the content
            clean_content = self.clean_markdown(body)
            chunks = self.chunk_document(clean_content)

            # Get relative path from docs directory
            rel_path = file_path.relative_to(self.docs_dir.parent)

            # Index each chunk
            for i, chunk in enumerate(chunks):
                doc_id = f"{rel_path}#chunk{i}"

                metadata = {
                    "title": title,
                    "file_path": str(rel_path),
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "sidebar_position": frontmatter.get('sidebar_position', ''),
                }

                print(f"Indexing: {doc_id}")
                self.rag_service.index_document(doc_id, chunk, metadata)

            print(f"✓ Indexed {file_path.name} ({len(chunks)} chunks)")

        except Exception as e:
            print(f"✗ Error indexing {file_path}: {e}")

    def index_all(self):
        """Index all markdown files in the docs directory"""
        print(f"Indexing documents from: {self.docs_dir}")

        # Find all .md and .mdx files
        md_files = list(self.docs_dir.glob('**/*.md'))
        mdx_files = list(self.docs_dir.glob('**/*.mdx'))
        all_files = md_files + mdx_files

        print(f"Found {len(all_files)} files to index")

        for file_path in all_files:
            self.index_file(file_path)

        print(f"\n✓ Indexing complete! Indexed {len(all_files)} files")

def main():
    """Main indexer function"""
    # Path to the book docs directory
    docs_dir = Path(__file__).parent.parent / "book" / "docs"

    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        return

    indexer = DocumentIndexer(str(docs_dir))
    indexer.index_all()

if __name__ == "__main__":
    main()
