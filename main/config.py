import json
import os
from loguru import logger

def load_config():
    """Membaca konfigurasi dari file config.json."""
    if not os.path.exists('config.json'):
        logger.warning("File config.json tidak ditemukan, menggunakan nilai default.")
        return {
            "proxy_retry_limit": 5,
            "reload_interval": 60,
            "max_concurrent_connections": 50
        }
    with open('config.json', 'r') as f:
        return json.load(f)