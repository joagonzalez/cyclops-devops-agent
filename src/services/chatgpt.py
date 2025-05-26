import json
import sys
sys.path.append("../..")
from openai import OpenAI
from typing import Any, Dict
from src.config.settings import config


class ChatGPTService:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, prompt: str, system_prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Sends a chat message to the OpenAI API and returns the response.

        Args:
            prompt (str): The user input to send to the model.
            system_prompt (str): The system prompt to set the context for the model.
            temperature (float, optional): The sampling temperature to use for the model. Defaults to 0.7.
            max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 256.

        Returns:
            str: The model's response as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages= [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                temperature=temperature,
            )
        except Exception as e:
            print(f"Error communicating with OpenAI API: {e}")
            return {"error": "An error occurred while processing your request."}
        
        return json.loads(response.choices[0].message.content) # type: ignore

if __name__ == "__main__":
    # Example usage
    llmClient = ChatGPTService(
        api_key=config["OPENAI"]["API_KEY"], model=config["OPENAI"]["MODEL"]
    )    
    
    response = llmClient.chat(
        prompt="How do I monitor CPU usage in Kubernetes?",
        system_prompt=config["OPENAI"]["SYSTEM_PROMPT"],
        temperature=config["OPENAI"]["TEMPERATURE"],
    )
    print(response)