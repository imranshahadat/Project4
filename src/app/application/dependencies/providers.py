"""Composition root: the only place where adapters are built and cached."""

from functools import lru_cache

from app.domains.infrastructure.embeddings.factory import build_embeddings
from app.domains.infrastructure.llm.factory import build_llm
from app.domains.interfaces.embeddings import BaseEmbeddings
from app.domains.interfaces.llm import BaseLLM


@lru_cache(maxsize=1)
def get_llm() -> BaseLLM:
    return build_llm()


@lru_cache(maxsize=1)
def get_embeddings() -> BaseEmbeddings:
    return build_embeddings()


@lru_cache(maxsize=1)
def get_vector_store():
    """Next step: PineconeVectorStore(embeddings=get_embeddings(), settings=get_settings())."""
    raise NotImplementedError("Pinecone adapter comes next")


def reset_all_caches() -> None:
    for fn in (get_llm, get_embeddings, get_vector_store):
        fn.cache_clear()


if __name__ == "__main__":
    llm = get_llm()
