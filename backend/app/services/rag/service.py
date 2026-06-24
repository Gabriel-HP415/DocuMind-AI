from __future__ import annotations

from typing import List, Tuple

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.core.config import settings
from app.services.vector_store.faiss_store import FaissStore


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are DocuMind AI, a helpful assistant. "
            "Use ONLY the following context to answer the user's question. "
            "If the answer is not in the context, say you don't know. "
            "Do not make up facts.\n\n"
            "Context:\n{context}",
        ),
        ("user", "Question: {question}"),
    ]
)


class RagService:
    def __init__(self, faiss_store: FaissStore) -> None:
        self.faiss_store = faiss_store

    def _format_docs(self, docs: List[Tuple[str, float]]) -> str:
        return "\n\n".join(doc for doc, _ in docs)

    def build_chain(self):
        llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE,
            num_ctx=settings.OLLAMA_NUM_CTX,
        )
        retriever = self.faiss_store

        chain = (
            {
                "context": lambda x: self._format_docs(retriever.search(x["question"], top_k=settings.TOP_K)),
                "question": RunnablePassthrough(),
            }
            | PROMPT
            | llm
            | StrOutputParser()
        )
        return chain

    def ask(self, question: str) -> Tuple[str, List[dict]]:
        docs = self.faiss_store.search(question, top_k=settings.TOP_K)
        chain = self.build_chain()
        answer = chain.invoke({"question": question})
        sources = [{"text": text, "score": score} for text, score in docs]
        return answer, sources
