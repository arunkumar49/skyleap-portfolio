from sky_leap.repository.vector_store import query_vectors
from sky_leap.services.rag.embedding import get_titan_embedding


def retrieve(query: str, top_k: int = 5):
    vector = get_titan_embedding(query)
    
    response = query_vectors(vector, namespace="client", top_k=top_k)
    
    for match in response.matches:
        metadata = match.metadata or {}
        text = metadata.get("text", "")
        print(text)
    # print(response)
