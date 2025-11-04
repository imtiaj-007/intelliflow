import threading
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

from app.core import settings
from app.utils.logger import log


class ChromaDBManager:
    """
    Thread-safe singleton manager for ChromaDB operations.
    Provides centralized management of client, embedding function, and collection.
    """

    def __init__(self):
        """Initialize ChromaDB client, embedding function, and collection."""
        try:
            self.client = chromadb.PersistentClient(path=settings.CHROMA_STORAGE_PATH)
            self.embedding_function = GoogleGenerativeAiEmbeddingFunction(
                api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_EMBEDDING_MODEL
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="intelliflow",
                embedding_function=self.embedding_function,
                metadata={
                    "description": "Intelliflow Chroma collection for knowledgebase context",
                    "created_at": str(datetime.now(timezone.utc)),
                },
            )
            log.info("ChromaDB manager initialized successfully")

        except Exception as e:
            log.error(f"Failed to initialize ChromaDB manager: {e}")
            raise

    def heartbeat(self) -> int:
        """Returns a nanosecond heartbeat. Useful for making sure the client remains connected."""
        return self.client.heartbeat()

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add documents to the collection.

        Args:
            documents: List of document texts to add
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of document IDs

        Returns:
            List of document IDs that were added
        """
        try:
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]

            if metadatas is None:
                metadatas = [{} for _ in documents]

            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

            log.info(f"Added {len(documents)} documents to ChromaDB collection")
            return ids

        except Exception as e:
            log.error(f"Failed to add documents to ChromaDB: {e}")
            raise

    def query(
        self,
        query_texts: List[str],
        n_results: int = settings.TOP_K_RESULTS,
        where: Optional[Dict] = None,
        where_document: Optional[Dict] = None,
    ) -> Dict:
        """
        Query the collection for similar documents.

        Args:
            query_texts: List of query texts
            n_results: Number of results to return
            where: Optional metadata filter
            where_document: Optional document content filter

        Returns:
            Dictionary containing query results
        """
        try:
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                where_document=where_document,
            )
            log.debug(f"Query returned {len(results.get('documents', []))} results")
            return results

        except Exception as e:
            log.error(f"Failed to query ChromaDB: {e}")
            raise

    def get_collection_info(self) -> Dict:
        """Get information about the current collection."""
        try:
            return self.collection.get()
        except Exception as e:
            log.error(f"Failed to get collection info: {e}")
            raise

    def count_documents(self) -> int:
        """Get the number of documents in the collection."""
        try:
            return self.collection.count()
        except Exception as e:
            log.error(f"Failed to count documents: {e}")
            raise


class ChromaDBInstance:
    """
    Thread-safe singleton factory class for ChromaDBManager instances.

    This class implements the double-checked locking pattern to ensure only one
    ChromaDBManager instance is created and shared across the application, providing
    thread safety and efficient resource management for ChromaDB operations.

    Attributes:
        _chroma_manager_instance (Optional[ChromaDBManager]): The singleton ChromaDBManager instance
        _chroma_manager_lock (threading.Lock): Lock for thread-safe singleton creation
    """

    _chroma_manager_instance: Optional[ChromaDBManager] = None
    _chroma_manager_lock: threading.Lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> ChromaDBManager:
        """
        Get or create the singleton ChromaDBManager instance using thread-safe pattern.

        This method uses double-checked locking to ensure thread safety while
        maintaining performance by avoiding unnecessary lock acquisition.

        Returns:
            ChromaDBManager: The singleton ChromaDBManager instance for ChromaDB operations

        Note:
            The singleton pattern ensures consistent ChromaDB client configuration
            and connection reuse throughout the application lifecycle.
        """

        if cls._chroma_manager_instance is None:
            with cls._chroma_manager_lock:
                if cls._chroma_manager_instance is None:
                    cls._chroma_manager_instance = ChromaDBManager()

        return cls._chroma_manager_instance
