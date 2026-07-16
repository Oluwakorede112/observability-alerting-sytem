import os
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from app.observability.error_collector import ErrorCollector
from app.utils.logger import get_logger

logger = get_logger()

# Load environment variables from .env file
load_dotenv()

# client = AsyncWebClient(token=os.environ['SLACK_ACCESS_TOKEN'])

# async def post_message(message: str) -> None:
#     """
#     Function to send messages of model depletion to slack channel"""
#     try:
#         response = await client.chat_postMessage(channel='#ai_model_alarms', text=message)
#         # assert response["message"]["text"] == message
#         if not response['ok']:
#             logger.error("slack message failed.")

#     except SlackApiError as e:
#         assert e.response["ok"] is False
#         assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#         logger.error(f"Got an error: {e.response['error']}", exc_info=True)    #log error




class SlackNotifier:
    def __init__(self):
        self.client = AsyncWebClient(token=os.environ['SLACK_ACCESS_TOKEN'])
        self.channel = "#ai_model_alarms"

    async def send(self, message: str):
        """ 
        Function to send failure alerts to slack channel
        """
        try:
            response = await self.client.chat_postMessage(
                channel=self.channel,
                text=message
            )
            logger.info("slack message sent successfully")
            if not response['ok']:
                logger.error("slack message failed")

        except SlackApiError as e:
            logger.error(
                f"Slack error: {e.response['error']}",
                exc_info=True
            )
 