from sky_leap.infrastructure.bedrock.aws_bedrock import invoke_bedrock_model, invoke_converse
from sky_leap.core.config import get_settings
from sky_leap.services.rag.embedding import get_titan_embedding
from sky_leap.services.rag.retrieval import retrieve_vectors

config = get_settings()


def generate_answer(query: str):
    
    results = retrieve_vectors(query, 3)
    
    # 2. Build a context string from the matched chunks
    context = "\n\n".join(
        f"[{i + 1}] {match['metadata']['text']}"
        for i, match in enumerate(results["matches"])
    )
    
    response = invoke_converse(context, query, config.bedrock_llm_model_id)
    
    print(response)
    if response is not None:
        print(response["output"]["message"]["content"][0]["text"])
    
    
if __name__ == "__main__":
    generate_answer("Does he read books?")