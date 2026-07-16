from dotenv import load_dotenv
import os
from fireworks.client import Fireworks, AsyncFireworks

load_dotenv()
class FireworksClient:
    def __init__(self):
        self.client = Fireworks(
            api_key=os.getenv("FIREWORKS_AI_API_KEY")
        )
        self.model = "accounts/fireworks/models/kimi-k2p7-code4"

    async def query_fireworks(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        response = response.choices[0].message.content
        print("\nresponse:\n", response)
        return response