import os
import tempfile
import threading
from typing import Any, Dict, List, Optional, Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ai.chroma_db import ChromaDBInstance
from app.utils.logger import log


class EmbeddingManager:
    """
    Manager for document processing, text splitting, and embedding operations.

    Handles PDF file processing, text chunking, and integration with ChromaDB
    for vector storage and similarity search operations. Uses the existing
    ChromaDB singleton instance for database operations.

    Attributes:
        chroma_manager (ChromaDBManager): Singleton instance for ChromaDB operations
        text_splitter (RecursiveCharacterTextSplitter): Text splitter for document chunking
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the EmbeddingManager with text splitting configuration.

        Args:
            chunk_size (int): The maximum size of text chunks for splitting documents
            chunk_overlap (int): The overlap between consecutive text chunks
        """
        self.chroma_manager = ChromaDBInstance.get_instance()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
        )

    def process_file_content(
        self, file_content: bytes, file_extension: str = ".pdf"
    ) -> List[Document]:
        """
        Process file content by writing to temporary file and loading as documents.

        Args:
            file_content (bytes): The binary content of the file to process
            file_extension (str): The file extension to use for temporary file creation

        Returns:
            List[Document]: List of processed and chunked document objects

        Raises:
            FileNotFoundError: If the temporary file cannot be created or accessed
            Exception: For any other processing errors during document loading
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp:
                tmp.write(file_content)
                temp_path = tmp.name

            documents = self._load_pdf(temp_path)
            os.unlink(temp_path)

            return documents

        except Exception:
            if "temp_path" in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _load_pdf(self, file_path: str) -> List[Document]:
        """
        Internal method to load and split PDF documents.

        Args:
            file_path (str): Path to the PDF file to load

        Returns:
            List[Document]: List of chunked document objects

        Raises:
            FileNotFoundError: If the specified file path does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        log.info(f"Loaded {len(docs)} pages from PDF")

        # Split into chunks
        chunks = self.text_splitter.split_documents(docs)
        log.info(f"Split into {len(chunks)} chunks")
        return chunks

    def add_documents_to_store(
        self, documents: List[Document], file_id: str
    ) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
        """
        Add processed documents to the ChromaDB vector store.

        Extracts text content and metadata from documents, then stores them
        in ChromaDB with appropriate file-specific metadata.

        Args:
            documents (List[Document]): List of document objects to add to store
            file_id (str): Unique identifier for the source file

        Returns:
            List[str]: List of document IDs that were successfully stored

        Raises:
            Exception: If there's an error during the document addition process
        """
        try:
            if not documents:
                log.warning("No documents to add to vector store")
                return []

            # Extract texts and metadata for ChromaDB
            texts = [doc.page_content for doc in documents]
            metadatas = [
                {
                    "file_id": file_id,
                    "page": doc.metadata.get("page", 0),
                    "source": doc.metadata.get("source", "unknown"),
                    "chunk_index": i,
                }
                for i, doc in enumerate(documents)
            ]

            # Add documents in chromaDB
            ids = [f"{file_id}_{i}" for i in range(len(documents))]
            stored_ids = self.chroma_manager.add_documents(
                documents=texts, metadatas=metadatas, ids=ids
            )

            log.info(f"Added {len(stored_ids)} documents to ChromaDB")
            return texts, metadatas, stored_ids

        except Exception as e:
            log.error(f"Error adding documents to ChromaDB: {e}")
            raise

    def similarity_search(self, query: str, k: int = 5, file_id: str = None) -> List[Dict]:
        """
        Perform similarity search against the vector store.

        Queries ChromaDB for documents similar to the provided query text,
        optionally filtered by a specific file ID.

        Args:
            query (str): The search query text
            k (int): Number of top results to return
            file_id (str, optional): Optional file ID to filter results by

        Returns:
            List[Dict]: Dictionary containing search results with documents,
                        metadata, and distances. Returns empty results on error.
        """
        try:
            where_filter = {"file_id": file_id} if file_id else None

            results = self.chroma_manager.query(
                query_texts=[query],
                n_results=k,
                where=where_filter,
            )

            log.info(f"Found {len(results.get('documents', []))} results for query")
            return results

        except Exception as e:
            log.error(f"Error during similarity search: {e}")
            return {"documents": [], "metadatas": [], "distances": []}

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the ChromaDB collection.

        Returns information about document count and collection metadata.

        Returns:
            Dict[str, Any]: Dictionary containing document count and collection info,
                            or error information if stats retrieval fails
        """
        try:
            collection_info = self.chroma_manager.get_collection_info()
            count = self.chroma_manager.count_documents()
            return {"document_count": count, "collection": collection_info}
        except Exception as e:
            log.error(f"Error getting stats: {e}")
            return {"document_count": "unknown"}


class EmbeddingInstance:
    """
    Thread-safe singleton factory class for EmbeddingManager instances.

    Implements the double-checked locking pattern to ensure only one
    EmbeddingManager instance is created and shared across the application,
    providing thread safety and efficient resource management for embedding operations.

    Attributes:
        _embedding_manager_instance (Optional[EmbeddingManager]): The singleton EmbeddingManager instance
        _embedding_manager_lock (threading.Lock): Lock for thread-safe singleton creation
    """

    _embedding_manager_instance: Optional[EmbeddingManager] = None
    _embedding_manager_lock: threading.Lock = threading.Lock()

    @classmethod
    def get_instance(cls, chunk_size: int = 1000, chunk_overlap: int = 200) -> EmbeddingManager:
        """
        Get or create the singleton EmbeddingManager instance using thread-safe pattern.

        This method uses double-checked locking to ensure thread safety while
        maintaining performance by avoiding unnecessary lock acquisition.

        Args:
            chunk_size (int): The size of text chunks for splitting documents
            chunk_overlap (int): The overlap between text chunks

        Returns:
            EmbeddingManager: The singleton EmbeddingManager instance for embedding operations

        Note:
            The singleton pattern ensures consistent embedding configuration
            and resource reuse throughout the application lifecycle.
        """

        if cls._embedding_manager_instance is None:
            with cls._embedding_manager_lock:
                if cls._embedding_manager_instance is None:
                    cls._embedding_manager_instance = EmbeddingManager(chunk_size, chunk_overlap)

        return cls._embedding_manager_instance
