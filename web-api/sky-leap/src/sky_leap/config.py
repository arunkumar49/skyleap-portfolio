"""Settings for ingestion and search, read from environment variables.

Locally they come from .env (``uv run --env-file .env ...``). Ingestion and
search both import from here, so they always agree on the embedding model,
dimensions, index and namespace.
"""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    pinecone_api_key: str
    pinecone_index: str = "portfolio-rag"
    pinecone_namespace: str = "v1"
    aws_region: str = "ap-south-1"
    embed_model_id: str = "amazon.titan-embed-text-v2:0"
    embed_dimensions: int = 1024


def _env(name: str, default: str) -> str:
    """Return the variable's value, or the default when unset or blank."""
    value = os.environ.get(name, "").strip()
    return value or default


@lru_cache
def get_settings() -> Settings:
    api_key = os.environ.get("PINECONE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "PINECONE_API_KEY is not set. Copy .env.example to .env, fill it in, "
            "and run with: uv run --env-file .env <command>"
        )

    dimensions_raw = _env("EMBED_DIMENSIONS", "1024")
    try:
        dimensions = int(dimensions_raw)
    except ValueError:
        raise RuntimeError(
            f"EMBED_DIMENSIONS must be an integer, got {dimensions_raw!r}."
        ) from None
    if dimensions <= 0:
        raise RuntimeError(f"EMBED_DIMENSIONS must be positive, got {dimensions}.")

    return Settings(
        pinecone_api_key=api_key,
        pinecone_index=_env("PINECONE_INDEX", "portfolio-rag"),
        pinecone_namespace=_env("PINECONE_NAMESPACE", "v1"),
        aws_region=_env("AWS_REGION", "us-east-1"),
        embed_model_id=_env("EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        embed_dimensions=dimensions,
    )
