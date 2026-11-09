import json
from pathlib import Path
import boto3
from sky_leap.config import get_settings
from sky_leap.services.rag.ingestion import chunk_document


config = get_settings()

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name= config.aws_region  # Change to your preferred region
)



def get_titan_embedding(text: str, dimensions: int = 1024) -> list[float]:
    
    body = json.dumps({
        "inputText": text,
        "dimensions": dimensions,
        "normalize": True
    })
    response = bedrock_runtime.invoke_model(
        modelId=config.embed_model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]



def embed_file(file: str):
    
    # 3. Embed each Element and keep its metadata for your vector DB
    embedded_records = []
    
    chunks = chunk_document(file)
    
    for chunk in chunks:
        # Skip empty chunks
        if not chunk.text or not chunk.text.strip():
            continue
    
        text_to_embed = chunk.text
        vector = get_titan_embedding(text_to_embed)
        
        # print(vector)

        embedded_records.append({
            "id": chunk.id,
            "text": text_to_embed,
            "embedding": vector,
            "metadata": chunk.metadata.to_dict()
        })
        
    print(f"Embedded {embedded_records} chunks.")
    
    
if __name__ == "__main__":
    embed_file("D:\\Applications\\skyleap-portfolio\\docs\\rag\\early-life-education.md")