import asyncio
import random
import uuid
import time
import json
from src.config import load_config
from src.updater import auto_update_script
from src.proxy_manager import load_proxies
from src.wss_connection import connect_to_wss
from loguru import logger

async def main():
    # Periksa pembaruan skrip dari GitHub
    auto_update_script()

    # Muat konfigurasi dari config.json
    config = load_config()
    proxy_retry_limit = config["proxy_retry_limit"]
    reload_interval = config["reload_interval"]
    max_concurrent_connections = config["max_concurrent_connections"]

    # Muat daftar proxy dari file
    local_proxies = load_proxies()

    # Membuat task queue untuk proxy
    queue = asyncio.Queue()
    for proxy in local_proxies:
        await queue.put(proxy)

    # Semaphore untuk membatasi koneksi bersamaan
    semaphore = asyncio.Semaphore(max_concurrent_connections)

    # Task untuk mengelola proxy
    tasks = []
    for _ in range(len(local_proxies)):
        task = asyncio.create_task(connect_to_wss(queue, semaphore, proxy_retry_limit))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())