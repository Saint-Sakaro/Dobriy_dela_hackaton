import logging
from typing import Any, Dict, Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class RagServiceError(RuntimeError):
    pass


class RagClient:
    """
    Placeholder client for the ML/RAG service.

    TODO: replace with real HTTP/gRPC calls once the ML service is ready.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.base_url = base_url or settings.RAG_SERVICE_URL
        self.api_key = api_key or settings.GIGACHAT_API_KEY

    def query(
        self,
        *,
        question: str,
        user,
        context_type: Optional[str] = None,
        context_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info(
            "RAG query: user=%s type=%s ctx=%s",
            getattr(user, "id", None),
            context_type,
            context_id,
        )
        # Stubbed response – integrate with actual service later.
        sources = []
        if context_type and context_id:
            sources.append({"type": context_type, "id": context_id})

        return {
            "answer": "Ассистент пока в режиме заглушки. Ответ появится после подключения RAG.",
            "sources": sources,
            "latency_ms": 0,
        }

