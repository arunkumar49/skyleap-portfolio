from pinecone import QueryResponse, ScoredVector
from sky_leap.infrastructure.vector_store.pc_vector_store import query_vectors
from sky_leap.services.rag.embedding import get_titan_embedding


def retrieve_vectors(query: str, top_k: int = 5) -> QueryResponse:
    vector = get_titan_embedding(query)
    
    response = query_vectors(vector, namespace="client", top_k=top_k)
    
    return response
    # print(response)
