import json
import boto3
from sky_leap.core.config import get_settings
from sky_leap.infrastructure.bedrock.aws_bedrock import invoke_bedrock_model

config = get_settings()

def get_titan_embedding(text: str, dimensions: int = config.embed_dimensions) -> list[float]:
    
    body = json.dumps({
        "inputText": text,
        "dimensions": dimensions,
        "normalize": True
    })
    
    response = invoke_bedrock_model(body, config.embed_model_id)
    
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]