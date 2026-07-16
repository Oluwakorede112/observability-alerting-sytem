import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.services.ai_service import AIService
from app.integrations.llm_prompt import LLM_PROMPT
from app.observability.alert_manager import monitor_errors
from contextlib import asynccontextmanager
from app.utils.logger import get_logger
import asyncio

logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    alert_task = asyncio.create_task(monitor_errors())
    logger.info("Background AI model alert manager started") 

    yield 

    # SHUTDOWN
    logger.info("Stopping background AI model alert manager")
    alert_task.cancel()

    try:
        await alert_task
    except asyncio.CancelledError:
        logger.info("Background AI model alert manager stopped")


app = FastAPI(title = "AI Observability + alerting system", lifespan=lifespan)
service = AIService()

PORT=int(os.environ.get("PORT", 8050))


@app.get("/fireworks")
async def test_fireworks():
    return await service.generate_with_fireworks(LLM_PROMPT)

@app.get("/together")
async def test_together():
    return await service.generate_with_together(LLM_PROMPT)


if __name__ == "__main__":
    import uvicorn    
    
    uvicorn.run(
        "main:app", 
        port=PORT,
        reload=True,
        log_level=os.environ.get("LOG_LEVEL", "debug"),
    )
