import json
import boto3
from sky_leap.config import get_settings

config = get_settings()


bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name= config.aws_region  # Change to your preferred region
)



def get_titan_embedding(text: str, dimensions: int = config.embed_dimensions) -> list[float]:
    
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