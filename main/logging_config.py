from loguru import logger

def setup_logging():
    """Mengatur konfigurasi logging untuk aplikasi."""
    logger.remove()
    logger.add("logs/app.log", rotation="1 MB", compression="zip", level="INFO", retention="10 days")