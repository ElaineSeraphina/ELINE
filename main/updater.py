import os
from subprocess import call
from loguru import logger

def auto_update_script():
    """Pembaruan otomatis dari GitHub jika diperlukan."""
    if os.path.isdir(".git"):
        logger.info("Memeriksa pembaruan skrip di GitHub...")
        call(["git", "pull"])
        logger.info("Skrip diperbarui dari GitHub.")
    else:
        logger.warning("Repositori ini belum di-clone menggunakan git. Silakan clone menggunakan git untuk fitur auto-update.")