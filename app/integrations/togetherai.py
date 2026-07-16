import os
from together import Together, AsyncClient

class TogetherClient:
    def __init__(self):
        self.client = Together(
            api_key=os.getenv("TOGETHER_AI_API_KEY")
        )
        self.model = "Qwen/Qwen3-Next-80B-A3B-Instruct"

    async def query_together(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        response =response.choices[0].message.content
        return response