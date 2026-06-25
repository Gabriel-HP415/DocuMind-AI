from __future__ import annotations

from typing import Generator, List, Tuple

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.core.config import settings
from app.services.vector_store.faiss_store import FaissStore

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Bạn là DocuMind AI, trợ lý AI thông minh. "
            "Hãy trả lời CÂU HỎI của người dùng bằng TIẾNG VIỆT. "
            "Sử dụng CHỈ DUY NHẤT các thông tin trong CONTEXT bên dưới để trả lời. "
            "Nếu không tìm thấy câu trả lời trong context, hãy trả lời: "
            "'Tôi không tìm thấy thông tin này trong tài liệu được cung cấp.' "
            "KHÔNG được bịa đặt thông tin.\n\n"
            "Context:\n{context}",
        ),
        ("user", "Câu hỏi: {question}"),
    ]
)

# Cache LLM instance
_cached_llm = None


def _get_llm():
    """Get cached LLM instance."""
    global _cached_llm
    if _cached_llm is None:
        _cached_llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE,
            num_ctx=1024,  # Reduced for faster inference
            timeout=120,
            options={
                "num_predict": 512,  # Limit output tokens
            }
        )
    return _cached_llm


class RagService:
    def __init__(self, faiss_store: FaissStore) -> None:
        self.faiss_store = faiss_store
        self._chain = None

    def _format_docs(self, docs: List[Tuple[str, float]]) -> str:
        return "\n\n".join(doc for doc, _ in docs)

    def _get_chain(self):
        """Get cached chain."""
        if self._chain is None:
            llm = _get_llm()
            retriever = self.faiss_store
            self._chain = (
                {
                    "context": lambda x: self._format_docs(retriever.search(x["question"], top_k=settings.TOP_K)),
                    "question": RunnablePassthrough(),
                }
                | PROMPT
                | llm
                | StrOutputParser()
            )
        return self._chain

    def ask(self, question: str) -> Tuple[str, List[dict]]:
        docs = self.faiss_store.search(question, top_k=settings.TOP_K)
        chain = self._get_chain()
        answer = chain.invoke({"question": question})
        sources = [{"text": text, "score": score} for text, score in docs]
        return answer, sources

    def ask_stream(self, question: str) -> Generator[str, None, None]:
        """Streaming version of ask for faster UX."""
        docs = self.faiss_store.search(question, top_k=settings.TOP_K)
        chain = self._get_chain()
        sources = [{"text": text, "score": score} for text, score in docs]
        
        # Use stream for LLM response
        for chunk in chain.stream({"question": question}):
            yield chunk

