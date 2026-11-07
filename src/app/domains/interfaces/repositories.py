# domains/interfaces/repositories.py  — PORT, vendor-neutral
from abc import ABC, abstractmethod
from typing import Optional


class BaseDocumentRepository(ABC):
    @abstractmethod
    def add(self, title: str, content: str) -> str: ...
    @abstractmethod
    def get(self, doc_id: str) -> Optional[dict]: ...
    @abstractmethod
    def list(self, limit: int = 50) -> list[dict]: ...
