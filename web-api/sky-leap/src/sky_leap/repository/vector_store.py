from html.entities import name2codepoint
from typing import Any, Sequence
from pinecone.exceptions import PineconeException
from pinecone import GrpcIndex, Index, Pinecone, QueryResponse, ServerlessSpec
from pydantic import conint
from sky_leap.config import get_settings
import time

config = get_settings()

pc = Pinecone(api_key=config.pinecone_api_key)


def _get_index() -> Index | GrpcIndex:
    
    if not pc.has_index(config.pinecone_index):
        pc.create_index(
            name=config.pinecone_index,
            dimension=config.embed_dimensions,   # must match Titan output size
            metric="cosine",        # Titan V2 vectors are normalized by default
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        
        # wait until the index is ready
        while not pc.describe_index(config.pinecone_index).status["ready"]:
            time.sleep(1)

    return pc.Index(config.pinecone_index)


def upsert_vector(vectors: Sequence[Any], namespace: str):
    try:
        index = _get_index()
        index.upsert(
            vectors=vectors,
            namespace=namespace
        )
    except PineconeException as e:
        raise Exception(f"Failed to upsert the vecotrs into pinecone database {e}")
    
    
def query_vectors(vector: Sequence[Any], namespace: str, top_k: int = config.chunk_num, meta_filter: dict = {}) -> QueryResponse:
    try:
        index = _get_index()
        
        vectors = index.query(
                    namespace=namespace,
                    vector=vector,
                    top_k=top_k,
                    include_metadata=True,
                    include_values=True,
                    filter=meta_filter
                )
        
        return vectors
    except PineconeException as e:
        raise Exception(f"Failed to query the vecotrs from pinecone database {e}")