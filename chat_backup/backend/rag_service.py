from typing import List, Dict, Optional
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class RAGService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai_native_book")
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"

        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure Qdrant collection exists"""
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
                )
                print(f"Created collection: {self.collection_name}")
        except Exception as e:
            print(f"Error ensuring collection: {e}")

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def index_document(self, doc_id: str, content: str, metadata: Dict):
        """Index a document into Qdrant"""
        embedding = self.get_embedding(content)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "doc_id": doc_id,
                "content": content,
                **metadata
            }
        )

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

    def search_similar(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.get_embedding(query)

        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        results = []
        for result in search_results:
            results.append({
                "content": result.payload.get("content", ""),
                "doc_id": result.payload.get("doc_id", ""),
                "title": result.payload.get("title", ""),
                "file_path": result.payload.get("file_path", ""),
                "score": result.score
            })

        return results

    def generate_response(
        self,
        query: str,
        context_docs: List[Dict],
        selected_text: Optional[str] = None,
        chat_history: List[Dict] = None
    ) -> str:
        """Generate response using OpenAI with RAG context"""

        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['title'] or doc['file_path']}]\n{doc['content']}"
            for doc in context_docs
        ])

        # Build system message
        system_message = """You are a helpful AI assistant for the "AI Native Development: Physical AI & Humanoid Robotics" book.
Your role is to answer questions based on the book's content.

Guidelines:
- Provide accurate, helpful answers based on the provided context
- If the context doesn't contain the answer, say so clearly
- Cite specific sections or chapters when relevant
- Be concise but comprehensive
- Use technical terms appropriately
"""

        if selected_text:
            system_message += f"\n\nThe user has selected this specific text for context:\n```\n{selected_text}\n```\n"

        # Build messages
        messages = [
            {"role": "system", "content": system_message}
        ]

        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history[-6:])  # Last 3 exchanges

        # Add context and user query
        user_message = f"""Context from the book:
{context}

User question: {query}"""

        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    def test_connection(self) -> bool:
        """Test connection to Qdrant"""
        try:
            self.qdrant_client.get_collections()
            return True
        except Exception as e:
            print(f"Qdrant connection failed: {e}")
            return False
