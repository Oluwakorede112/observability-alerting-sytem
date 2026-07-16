import time
from app.observability.slack_notifier import SlackNotifier
import asyncio
from app.observability.error_collector import ErrorCollector
from app.utils.logger import get_logger
 
logger = get_logger()

WINDOW = 60 #120 in seconds - sliding window of errors to monitor 
THRESHOLD = 2  #5 # min req / errors allowed in window


class AlertManager:
    
    def __init__(self): 
        self.notifier = SlackNotifier()
        self.window = WINDOW 
        self.threshold = THRESHOLD 
        self.last_alerted = {} #prevents deduplicated alerts

    async def evaluate(self):
        now = time.time()
        errors = ErrorCollector.get_errors()
        # print(f"[AlertManager] Errors: {errors}")
        
        # get recent errors
        for key, entries in errors.items():
            recent_errors = [e for e in entries if now - e["timestamp"] < self.window]

            if len(recent_errors) >= self.threshold:
                if self._should_alert(key):
                    await self._trigger_alert(key, recent_errors)
                     # clear the errorcollector after evaluting
                    ErrorCollector.clear_error_log()
            else:
                logger.infor("[INFO:] Errors not upto threshold.")
                pass

    def _should_alert(self, key):
        now = time.time()

        # don't alert same issue repeatedly within the window
        if key in self.last_alerted:
            if now - self.last_alerted[key] < self.window:
                return False

        self.last_alerted[key] = now
        return True

    async def _trigger_alert(self, key, recent_errors):
        event, provider, error_type = key.split(":")
        count = len(recent_errors)
        # print(f"[AlertManager] Triggering alert for {key} with {count} errors")

        message = f"""
                        🚨 CRITICAL: {event.replace('_', ' ').title()}

                        Provider: {provider}
                        Error: {error_type}
                        Failures: {count} req (last {self.window // 60} mins)
                        Status: Ongoing
                    """
        await self.notifier.send(message.strip())
        print("[AlertManager] Alert sent!")


# run alert manager in the background
alert_manager = AlertManager()

async def monitor_errors():
    try:
        while True:
            await alert_manager.evaluate()
            print("[Monitor] Running evaluation cycle")
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        # clean up resources 
        logger.info("Alert manager stopped.")

        









    
