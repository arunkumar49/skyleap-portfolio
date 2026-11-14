import asyncio
from typing import Any
import boto3
from sky_leap.core.config import get_settings
from botocore.exceptions import ClientError

config = get_settings()

client = boto3.client(
    service_name='bedrock-runtime',
    region_name= config.aws_region  # Change to your preferred region
)


def invoke_bedrock_model(body: str, model: str) -> dict[str, Any]:
    
    response = client.invoke_model(
            modelId= model,
            contentType="application/json",
            accept="application/json",
            body=body
        )
    
    return response


async def invoke_converse(context: str, query: str, model_id: str) -> dict[str, Any] | None:
    
    try:
        response = await asyncio.to_thread(
            client.converse,
            modelId=model_id,
            system=[{
                "text": "Answer the question using only the provided context. "
                "If the answer is not in the context, say you don't know."
            }],
            messages=[{
                "role": "user",
                "content": [{"text": f"Context:\n{context}\n\nQuestion: {query}"}],
            }],
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )
        
        return response
        
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")