from app.integrations.fireworksai import FireworksClient
from app.integrations.togetherai import TogetherClient
from app.observability.error_collector import ErrorCollector

class AIService:
    def __init__(self):
        self.fireworks = FireworksClient()
        self.together = TogetherClient()

    async def generate_with_fireworks(self, prompt: str):
        try:
            return await self.fireworks.query_fireworks(prompt)

        except Exception as e:
            ErrorCollector.capture(
                event="fireworks_failure",
                provider="fireworks",
                error=e,
                metadata={"prompt": prompt}
            )
            # raise
            pass

    async def generate_with_together(self, prompt: str):
        try:
            return await self.together.query_together(prompt)

        except Exception as e:
            ErrorCollector.capture(
                event="together_failure",
                provider="together",
                error=e,
                metadata={"prompt": prompt} 
            )
            raise