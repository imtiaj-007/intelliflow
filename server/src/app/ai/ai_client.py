import threading
from typing import Optional, Tuple

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pydantic import SecretStr

from app.core import settings


class LLMManager:
    """
    Thread-safe singleton manager for LLM instances.
    Provides shared instances for embeddings and chat to avoid redundant initialization.
    """

    _embedding_instance: Optional[GoogleGenerativeAIEmbeddings] = None
    _chat_instance: Optional[ChatGoogleGenerativeAI] = None
    _lock = threading.Lock()
    _api_secret: SecretStr = SecretStr(settings.GOOGLE_API_KEY)

    @classmethod
    def get_embedding_instance(cls) -> GoogleGenerativeAIEmbeddings:
        """Get or create a shared instance of GoogleGenerativeAIEmbeddings.

        Returns:
            GoogleGenerativeAIEmbeddings: Thread-safe singleton embedding instance

        Note:
            Uses double-checked locking pattern for thread safety
        """
        if cls._embedding_instance is None:
            with cls._lock:
                if cls._embedding_instance is None:
                    model: str = settings.LLM_EMBEDDING_MODEL or "gemini-embedding-001"
                    cls._embedding_instance = GoogleGenerativeAIEmbeddings(
                        model=model,
                        google_api_key=cls._api_secret,
                    )
        return cls._embedding_instance

    @classmethod
    def get_chat_instance(cls) -> ChatGoogleGenerativeAI:
        """Get or create a shared instance of ChatGoogleGenerativeAI.

        Returns:
            ChatGoogleGenerativeAI: Thread-safe singleton chat instance

        Note:
            Uses double-checked locking pattern for thread safety
        """
        if cls._chat_instance is None:
            with cls._lock:
                if cls._chat_instance is None:
                    model: str = settings.LLM_CHAT_MODEL or "gemini-2.5-pro"
                    cls._chat_instance = ChatGoogleGenerativeAI(
                        model=model, google_api_key=cls._api_secret
                    )
        return cls._chat_instance

    @classmethod
    def get_instances(cls) -> Tuple[GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI]:
        """Get both embedding and chat instances in a single call.

        Returns:
            Tuple[GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI]:
                Tuple containing embedding instance and chat instance
        """
        return cls.get_embedding_instance(), cls.get_chat_instance()
