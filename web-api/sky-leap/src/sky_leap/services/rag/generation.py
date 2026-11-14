from sky_leap.infrastructure.bedrock.aws_bedrock import invoke_bedrock_model, invoke_converse
from sky_leap.core.config import get_settings
from sky_leap.services.rag.embedding import get_titan_embedding
from sky_leap.services.rag.retrieval import retrieve_vectors

config = get_settings()

class GenerateAnswer():
    
    async def generate_answer(self, query: str) -> str:
        
        results = retrieve_vectors(query, 3)
        
        # 2. Build a context string from the matched chunks
        context = "\n\n".join(
            f"[{i + 1}] {match['metadata']['text']}"
            for i, match in enumerate(results["matches"])
        )
        
        response = await invoke_converse(context, query, config.bedrock_llm_model_id)
        
        if response is not None:
            return response["output"]["message"]["content"][0]["text"]

        return "The quesion you asked is not in the context, please contact the owner Arun."
    
# if __name__ == "__main__":
#     generate_answer("Does he read books?")