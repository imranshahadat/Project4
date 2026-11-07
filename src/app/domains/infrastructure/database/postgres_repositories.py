from typing import Any, Optional

from sqlalchemy.orm import Session

from app.domains.infrastructure.database.models import Document
from app.domains.interfaces.repositories import BaseDocumentRepository


class PostgresDocumentRepository(BaseDocumentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, title: str, content: str) -> str:
        doc = Document(title=title, content=content)
        self._session.add(doc)
        self._session.flush()  # gets the id NOW; the actual commit belongs to get_db_session
        return doc.id

    def get(self, doc_id: str) -> Optional[dict[str, Any]]:
        doc = self._session.get(Document, doc_id)
        if doc is None:
            return None
        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at,
        }

    def list(self, limit: int = 50) -> list[dict[str, Any]]:
        docs = (
            self._session.query(Document)
            .order_by(Document.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": d.id,
                "title": d.title,
                "content": d.content,
                "created_at": d.created_at,
            }
            for d in docs
        ]
