from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sky_leap.api.dependencies import get_generation_service
from sky_leap.schema.chat import Answer, Query
from sky_leap.services.rag.generation import GenerateAnswer



router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/query")
async def answer_query(
    query: Annotated[Query, Body(examples=[{"question": "What projects has he worked on?"}])],
    service: Annotated[GenerateAnswer, Depends(get_generation_service)]
) -> Answer:
    
    answer = await service.generate_answer(query.question)
    return Answer(ans=answer)

    
    