from typing import List, Dict, Any, Optional
from datetime import datetime
from dateutil import parser

from preprocess.chunker import TextPreprocessor
from embedding.embedder import TextEmbedder
from retrieval.retriever import VectorRetriever
from gigachat import GigaChat


class Seeker:
    """
    Seeker с поддержкой RAG и истории диалога.
    - Первый запрос: поиск релевантных событий + RAG-контекст.
    - Последующие уточнения: только использование истории сообщений.
    - История сбрасывается по вызову reset().
    """

    def __init__(
        self,
        retriever: Optional[VectorRetriever] = None,
        embedder: Optional[TextEmbedder] = None,
        preprocessor: Optional[TextPreprocessor] = None,
        gigachat_creds: Optional[str] = None
    ):
        self.retriever = retriever or VectorRetriever.load(
            "ml\\data\\actions.index", "ml\\data\\actions_info.pkl"
        )
        self.embedder = embedder or TextEmbedder()
        self.preprocessor = preprocessor or TextPreprocessor(use_lemmatization=True)

        self.llm = GigaChat(
            credentials=gigachat_creds,
            verify_ssl_certs=False,
            timeout=60
        )

        # История сообщений для текущего диалога
        self.chat_history: List[Dict[str, str]] = []
        self.rag_initialized = False  # Флаг, добавлен ли RAG-контекст

    def get_raw_answer(
        self,
        query_text: str,
        city: Optional[str] = None,
        NKO: Optional[str] = None,
        toa: Optional[str] = None,
        time: Optional[str] = None
    ) -> List[Dict[str, str]]:
        query_vector = self.embedder.encode(self.preprocessor.process(query_text))
        answers = self.retriever.search(query_vector, city, NKO, toa, time)

        results = []
        for answ in answers:
            results.append({
                "text": f"[START CHUNK] {answ['text']} [END CHUNK]",
                "link": answ["link"]
            })
        return results

    @staticmethod
    def build_prompt(events: List[Dict[str, str]]) -> str:
        """
        Формирует RAG-контекст из найденных событий
        """
        blocks = []
        for i, e in enumerate(events, start=1):
            block = (
                f"EVENT {i}:\n"
                f"{e['text']}\n"
                f"LINK: {e['link']}\n"
            )
            blocks.append(block)

        context = "\n\n".join(blocks)

        full_prompt = (
            "Ты — интеллектуальная система поиска.\n"
            "Кратко расскажи о сути каждого события, указывая сначала организацию, "
            "а затем ссылку с пояснением, что там полное описание события. "
            "После всех описаний спроси у пользователя, хочет ли он узнать больше, "
            "и предложи возможные уточняющие вопросы. Предлагай только те вопросы, ответы на которые есть в исходных описаниях событий,"
            "в случае, если пользователь задал вопрос, ответ на который не находится в описании события, говори, что не нашел информации, отвечающей на запрос пользователя"
            f"КОНТЕКСТ:\n{context}\n\n"
        )
        return full_prompt

    def ask_llm(
        self,
        query_text: str,
        city: Optional[str] = None,
        NKO: Optional[str] = None,
        toa: Optional[str] = None,
        time: Optional[str] = None
    ) -> str:
        """
        Если это первый запрос диалога — добавляем RAG-контекст.
        Далее только история диалога используется.
        """
        if not self.rag_initialized:
            events = self.get_raw_answer(query_text, city, NKO, toa, time)
            if len(events) == 0:
                return "Не нашёл подходящих событий."

            rag_context = Seeker.build_prompt(events)
            self.chat_history.append({"role": "system", "content": rag_context})
            self.rag_initialized = True

        self.chat_history.append({"role": "user", "content": query_text})

        # Вызов LLM с историей
        request_payload = {
            "messages": self.chat_history,
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = self.llm.chat(request_payload)

        answer_text = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": answer_text})

        return answer_text

    def reset(self):
        """Сбрасывает историю диалога"""
        self.chat_history = []
        self.rag_initialized = False
