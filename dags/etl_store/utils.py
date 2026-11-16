import logging
from functools import wraps
import sqlalchemy as sqal
from contextlib import contextmanager

logger = logging.getLogger("ProjectAlpha")
def log_step(step_name : str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"------STARTING {step_name}-------")

            result = func(*args, **kwargs)

            logger.info(f"[COMPLETED] {step_name}")

            return result
        return wrapper
    return decorator

@contextmanager
def database_connection(db_string : str):
    logger.debug("[DATABASE] Opening engine to database...")
    engine = sqal.create_engine(db_string)
    conn = engine.connect()

    try:
        yield conn
    finally:
        logger.debug("[DATABASE] Closing engine (Cleaning momentum)")
        conn.close()
        engine.dispose()