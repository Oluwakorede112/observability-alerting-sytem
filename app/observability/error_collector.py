import time
from collections import defaultdict

class ErrorCollector:
    """ In-memory data store for all errors. it standardizes and aggregates error reports"""
    _errors = defaultdict(list)

    @classmethod
    def capture(cls, event: str, provider: str, error: Exception, metadata: dict = None):
        key = f"{event}:{provider}:{type(error).__name__}"

        cls._errors[key].append({
            "timestamp": time.time(),
            "message": str(error), #add the error message itsefl - ej
            "metadata": metadata or {}
        })
        
        # prevent runaway memory usage
        MAX_ERRORS_PER_KEY = 1000 #1000rpm
        if len(cls._errors[key]) > MAX_ERRORS_PER_KEY:
            cls._errors[key].pop(0)  # remove oldest
        
        # print(f"[ErrorCollector] Captured: {event} | {provider} | {type(error).__name__}")
        # print(f"[ErrorCollector metadata:] \n{metadata}") 
        # print(f"[ErrorCollector error:] \n{error}")
        # print(f"[ErrorCollector _errors:] \n{cls._errors}")
    
    @classmethod
    def get_errors(cls):
        """
        Retrieve all collected errors.
        """
        return cls._errors

    @classmethod
    def clear_error_log(cls):
        """
        Clear all recorded errors.
        """
        cls._errors = defaultdict(list)