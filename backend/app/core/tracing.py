import time
import functools
import logging
from typing import Callable, Any
from app.modules.admin.models.trace.trace_configuration import TraceConfiguration

from app.modules.admin.models.trace.trace_entry import TraceEntry
from app.core.database import get_db

logger = logging.getLogger(__name__)

def trace_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        db = next(get_db())
        config = db.query(TraceConfiguration).filter_by(service_name="admin").first()
        enabled = config.enabled if config else False
        
        if not enabled:
            return await func(*args, **kwargs)
            
        start_time = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time
            
            trace_entry = TraceEntry(
                function_name=func.__name__,
                module_name=func.__module__,
                duration=duration
            )
            db.add(trace_entry)
            db.commit()
            
            logger.info(f"Function {func.__module__}.{func.__name__} executed in {duration:.4f}s")
            
    return wrapper
