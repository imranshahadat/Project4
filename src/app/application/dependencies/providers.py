"""Composition root: the only place where adapters are built and cached."""

from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy.orm import Session

from app.domains.infrastructure.database.engine import get_session_factory
from app.domains.infrastructure.database.postgres_repositories import (
    PostgresDocumentRepository,
)
from app.domains.infrastructure.embeddings.factory import build_embeddings
from app.domains.infrastructure.llm.factory import build_llm
from app.domains.interfaces.embeddings import BaseEmbeddings
from app.domains.interfaces.llm import BaseLLM
from app.domains.interfaces.repositories import BaseDocumentRepository

from app.domains.infrastructure.storage.factory import build_storage
from app.domains.infrastructure.vector_store.factory import build_vector_store
from app.domains.interfaces.storage import BaseStorage
from app.domains.interfaces.vector_store import BaseVectorStore

from app.domains.infrastructure.database.postgres_repositories import (
    PostgresAuditRepository,
    PostgresDocumentRepository,
)
from app.domains.interfaces.audit import BaseAuditRepository


# ---------------- LLM ----------------
@lru_cache(maxsize=1)
def get_llm() -> BaseLLM:
    return build_llm()


# ---------------- Embeddings ----------------
@lru_cache(maxsize=1)
def get_embeddings() -> BaseEmbeddings:
    return build_embeddings()


# ---------------- Vector store (next: Pinecone) ----------------
@lru_cache(maxsize=1)
def get_vector_store():
    raise NotImplementedError("Pinecone adapter comes next")


# ---------------- Vector store ----------------
@lru_cache(maxsize=1)
def get_vector_store() -> BaseVectorStore:
    return build_vector_store()


# ---------------- Object storage (S3) ----------------
@lru_cache(maxsize=1)
def get_storage() -> BaseStorage:
    return build_storage()


def reset_all_caches() -> None:
    for fn in (get_llm, get_embeddings, get_vector_store, get_storage):
        fn.cache_clear()


# ---------------- Database ----------------
@contextmanager
def get_db_session() -> Iterator[Session]:
    """One transaction per `with` block: commit on success, rollback on error."""
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@lru_cache(maxsize=1)
def build_document_repository(session: Session) -> BaseDocumentRepository:
    """Attach a repository to a session you already opened."""
    return PostgresDocumentRepository(session)


@lru_cache(maxsize=1)
def build_audit_repository(session: Session) -> BaseAuditRepository:
    """Attach an audit repository to a session you already opened."""
    return PostgresAuditRepository(session)


# ---------------- Testing helper ----------------
def reset_all_caches() -> None:
    for fn in (get_llm, get_embeddings, get_vector_store):
        fn.cache_clear()
