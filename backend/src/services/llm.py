"""
OpenAI LLM service.

Generates grounded responses using GPT-4o-mini with RAG context.
"""

import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from src.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for generating responses using OpenAI chat models."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_chat_model

    def _build_system_prompt(self, retrieved_chunks: List[Dict]) -> str:
        """
        Build system prompt with retrieved context.

        Args:
            retrieved_chunks: List of retrieved document chunks

        Returns:
            System prompt with context
        """
        context_text = "\n\n".join(
            [
                f"[Source: {chunk['title']} - {chunk['file_path']}]\n{chunk['chunk_text']}"
                for chunk in retrieved_chunks
            ]
        )

        system_prompt = f"""You are a helpful AI assistant for the "Physical AI & Humanoid Robotics" textbook.

Your role is to answer questions based ONLY on the provided book content. Follow these guidelines:

1. GROUNDING: Base all answers strictly on the provided context below. Do not use external knowledge.
2. CITATIONS: Reference specific sources when making claims (e.g., "According to the ROS2 chapter...").
3. SCOPE: If the question is outside the book's scope, politely state: "I don't have information about that in the documentation. I can only answer questions about Physical AI, robotics, ROS2, and related topics covered in this book."
4. CLARITY: Explain technical concepts clearly, suitable for students learning robotics.
5. HONESTY: If the context doesn't contain enough information to answer fully, admit it.

CONTEXT FROM BOOK:
{context_text}

Answer the user's question based on the above context."""

        return system_prompt

    def _build_conversation_history(
        self, conversation_messages: List[Dict], current_query: str, selected_text: Optional[str]
    ) -> List[Dict[str, str]]:
        """
        Build conversation history for LLM context.

        Args:
            conversation_messages: Previous messages in conversation
            current_query: Current user query
            selected_text: Optional selected text from page

        Returns:
            List of message dictionaries for OpenAI API
        """
        messages = []

        # Add previous conversation context (last N messages)
        for msg in conversation_messages[-settings.max_conversation_context :]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current query with selected text if present
        if selected_text:
            query_with_context = f"""Selected text from page: "{selected_text}"

Question: {current_query}"""
            messages.append({"role": "user", "content": query_with_context})
        else:
            messages.append({"role": "user", "content": current_query})

        return messages

    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[Dict],
        conversation_history: List[Dict] = None,
        selected_text: Optional[str] = None,
    ) -> str:
        """
        Generate AI response based on query and retrieved context.

        Args:
            query: User query
            retrieved_chunks: Retrieved document chunks
            conversation_history: Previous messages in conversation
            selected_text: Optional selected text from page

        Returns:
            AI-generated response

        Raises:
            Exception: If API call fails
        """
        try:
            # Build system prompt with context
            system_prompt = self._build_system_prompt(retrieved_chunks)

            # Build conversation history
            conversation_history = conversation_history or []
            messages = self._build_conversation_history(
                conversation_history, query, selected_text
            )

            # Generate response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages,
                ],
                temperature=0.7,
                max_tokens=500,
            )

            answer = response.choices[0].message.content
            logger.info(f"Generated response (length: {len(answer)} chars)")
            return answer

        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise

    async def check_health(self) -> bool:
        """
        Check if OpenAI API is accessible.

        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple test request
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {str(e)}")
            return False
