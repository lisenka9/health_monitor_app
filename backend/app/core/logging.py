import structlog
import logging
import sys

def setup_logging():
    """Настройка структурного логирования в JSON"""
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(handler)

def get_logger(name: str):
    """Получить структурированный логгер"""
    return structlog.get_logger(name)