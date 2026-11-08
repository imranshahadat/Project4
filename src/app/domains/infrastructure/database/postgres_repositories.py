"""Adapter: Postgres documents + audit repositories.

Handles the SQLAlchemy 'metadata' reserved-attribute conflict:
  - Document.metadata (class-level) = SQLAlchemy's MetaData object
  - instance.__dict__['metadata']   = the actual JSONB column value
We read/write via __dict__ + flag_modified to bypass the conflict.
"""

from typing import Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.core.exceptions import DocumentNotFoundError
from app.domains.infrastructure.database.models import AuditEvent, Document
from app.domains.interfaces.audit import BaseAuditRepository
from app.domains.interfaces.repositories import BaseDocumentRepository


def _doc_metadata(doc: Document) -> dict[str, Any]:
    """Safely read the metadata JSONB from a Document instance.

    `getattr(doc, 'metadata')` returns SQLAlchemy's MetaData object when the
    attribute name conflicts. Reading from `__dict__` gets the actual column
    value that was loaded from the database.
    """
    raw = doc.__dict__.get("metadata")
    if isinstance(raw, dict):
        return raw
    return {}


class PostgresDocumentRepository(BaseDocumentRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(
        self,
        title: str,
        content: str,
        source: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        doc = Document(title=title, content=content, source=source)
        if metadata is not None:
            # FIXED: Clean attribute assignment. SQLAlchemy tracks this automatically.
            doc.doc_metadata = metadata
        self._session.add(doc)
        self._session.flush()
        return doc.id

    def get(self, doc_id: str) -> Optional[Document]:
        return self._session.get(Document, doc_id)

    def list_all(self, limit: int = 100, offset: int = 0) -> list[Document]:
        return (
            self._session.query(Document)
            .order_by(Document.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def update_status(self, doc_id: str, status: str) -> None:
        doc = self._session.get(Document, doc_id)
        if doc is None:
            raise DocumentNotFoundError(f"Document '{doc_id}' not found")
        doc.status = status
        self._session.flush()

    def set_source(self, doc_id: str, source: str) -> None:
        doc = self._session.get(Document, doc_id)
        if doc is None:
            raise DocumentNotFoundError(f"Document '{doc_id}' not found")
        doc.source = source
        self._session.flush()

    def set_metadata(self, doc_id: str, metadata: dict[str, Any]) -> None:
        doc = self._session.get(Document, doc_id)
        if doc is None:
            raise DocumentNotFoundError(f"Document '{doc_id}' not found")
        # FIXED: Clean attribute assignment
        doc.doc_metadata = metadata
        self._session.flush()

    def delete(self, doc_id: str) -> None:
        doc = self._session.get(Document, doc_id)
        if doc is not None:
            self._session.delete(doc)
            self._session.flush()


class PostgresAuditRepository(BaseAuditRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def append(
        self,
        action: str,
        entity_type: str,
        entity_id: str,
        detail: Optional[dict[str, Any]] = None,
        actor: str = "system",
    ) -> None:
        self._session.add(
            AuditEvent(
                actor=actor,
                actor_type="system",
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                detail=detail,
            )
        )
        self._session.flush()
