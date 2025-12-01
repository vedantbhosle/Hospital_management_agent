import functools
import time
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("Tracer")

def trace_agent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        agent_name = args[0].__class__.__name__ if args else "UnknownAgent"
        method_name = func.__name__
        
        logger.info(f"[{agent_name}] Starting {method_name}")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"[{agent_name}] Completed {method_name} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"[{agent_name}] Failed {method_name} after {duration:.2f}s: {str(e)}")
            raise e
            
    return wrapper

def trace_tool(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = args[0].__class__.__name__ if args else "UnknownTool"
        method_name = func.__name__
        
        logger.info(f"[Tool:{tool_name}] Calling {method_name}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"[Tool:{tool_name}] Error in {method_name}: {str(e)}")
            raise e
    return wrapper
