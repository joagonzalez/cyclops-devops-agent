"""
API endpoints for sending prompts to Large Language Models (LLMs)
from external tools and applications.
"""
from typing import Any
from fastapi import APIRouter, status
from src.config.settings import config
from src.services.chatgpt import ChatGPTService
from fastapi import Body


router = APIRouter()
llmClient = ChatGPTService(
    api_key=config["OPENAI"]["API_KEY"], model=config["OPENAI"]["MODEL"]
)

@router.post("/query/", tags=["LLM"], status_code=status.HTTP_200_OK)
async def query_llm(prompt: str = Body(..., embed=True), secret: str = 'letmepass') -> Any:
    """
    Sends a prompt to the instantiated LLM and returns the response.

    Args:
        prompt (str): The input prompt to send to the LLM.

    Returns:
        Any: The LLM's response.
    """
    if secret != 'cyclops2025':
        return {"error": "Unauthorized access. Invalid secret."}
    
    response = llmClient.chat(
        prompt=prompt,
        system_prompt=config["OPENAI"]["SYSTEM_PROMPT"],
        temperature=config["OPENAI"]["TEMPERATURE"],
    )
    return {"response": response}