from typing import Optional
from uuid import UUID

from app.ai.ai_client import LLMManager
from app.ai.chroma_db import ChromaDBInstance
from app.ai.prompt_manager import PromptManager
from app.core.settings import settings
from app.repository.file import FileRepository
from app.utils.logger import log


class ChatService:
    """Service class for handling chat operations.

    This class provides a high-level interface for chat-related operations, coordinating
    with file repository for document management and integrating AI components for
    semantic search and response generation.

    Attributes:
        file_repo (FileRepository): Repository instance for file-related database operations
        chroma_manager: ChromaDB manager instance for vector search operations
        llm_manager: LLM manager instance for AI model interactions
        prompt_manager: Prompt manager for generating structured prompts
    """

    def __init__(self, file_repository: FileRepository):
        """Initialize the ChatService with required dependencies.

        Args:
            file_repository (FileRepository): Repository instance for file database operations
        """
        self.file_repo = file_repository
        self.chroma_manager = ChromaDBInstance.get_instance()
        self.chat_client = LLMManager().get_chat_instance()
        self.prompt_manager = PromptManager()

    async def chat_with_workflow(self, query: str, workflow_id: str | UUID) -> Optional[str]:
        """Generate a chat response using semantic search from workflow documents.

        This method performs semantic search on documents associated with the workflow,
        retrieves relevant context, and generates an AI-powered response.

        Args:
            query (str): The user's query/question
            workflow_id (UUID): The workflow ID to search within

        Returns:
            Optional[str]: The generated response, or None if an error occurs

        Raises:
            Exception: If any step in the chat generation process fails
        """
        try:
            # Get files associated with the workflow
            workflow_id = UUID(workflow_id) if isinstance(workflow_id, str) else workflow_id
            file = await self.file_repo.get_file_by_workflow_id(workflow_id)
            if not file:
                return "No documents found in this workflow. Please upload files first."

            # Perform semantic search to find relevant context
            search_results = self.chroma_manager.query(
                query_texts=[query],
                n_results=settings.TOP_K_RESULTS,
                where={"file_id": str(file.id)},
            )

            if not search_results or not search_results.get("documents"):
                return "I couldn't find relevant information in your documents to answer this question."

            # Combine retrieved context and generate prompt
            context = "\n\n".join(
                [f"Document {i+1}:\n{doc}" for i, doc in enumerate(search_results["documents"][0])]
            )
            prompt = self.prompt_manager.get_rag_prompt(context=context, question=query)

            response = await self.chat_client.ainvoke(prompt)
            return response.content if hasattr(response, "content") else str(response)

        except Exception as e:
            log.error(f"Failed to generate chat response: {e}")
            raise
