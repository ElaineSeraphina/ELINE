import asyncio
import random
import uuid
import json
import ssl
from loguru import logger

async def generate_random_user_agent():
    """Menghasilkan user agent acak untuk setiap koneksi."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    ]
    return random.choice(user_agents)

async def connect_to_wss(queue, semaphore, proxy_retry_limit):
    """Menghubungkan ke WebSocket dengan proxy yang diberikan."""
    while not queue.empty():
        socks5_proxy = await queue.get()
        retries = 0
        backoff = 0.5  # Backoff mulai dari 0.5 detik

        while retries < proxy_retry_limit:
            try:
                # Buat header acak
                custom_headers = {
                    "User-Agent": await generate_random_user_agent(),
                    "Accept-Language": random.choice(["en-US", "en-GB", "id-ID"]),
                    "Referer": random.choice(["https://www.google.com/", "https://www.bing.com/"]),
                    "X-Forwarded-For": ".".join(map(str, (random.randint(1, 255) for _ in range(4)))),
                    "DNT": "1",  
                    "Connection": "keep-alive"
                }

                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                uri = random.choice(["wss://proxy.wynd.network:4444/", "wss://proxy.wynd.network:4650/"])

                # Menghubungkan ke WebSocket
                async with websockets.connect(uri, ssl=ssl_context, extra_headers=custom_headers) as websocket:
                    # Lakukan pengiriman ping secara berkala
                    async def send_ping():
                        while True:
                            ping_message = json.dumps({
                                "id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}
                            })
                            await websocket.send(ping_message)
                            await asyncio.sleep(random.uniform(1, 3))

                    asyncio.create_task(send_ping())

                    while True:
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=5)
                            message = json.loads(response)

                            if message.get("action") == "AUTH":
                                # Kirim respons otentikasi
                                auth_response = {
                                    "id": message["id"],
                                    "origin_action": "AUTH",
                                    "result": {
                                        "browser_id": str(uuid.uuid4()),
                                        "user_agent": custom_headers['User-Agent'],
                                        "timestamp": int(time.time()),
                                        "device_type": "desktop",
                                        "version": "4.28.1",
                                    }
                                }
                                await websocket.send(json.dumps(auth_response))

                            elif message.get("action") == "PONG":
                                logger.success("BERHASIL", color="<green>")
                                await websocket.send(json.dumps({"id": message["id"], "origin_action": "PONG"}))

                        except asyncio.TimeoutError:
                            logger.warning("Koneksi Ulang", color="<yellow>")
                            break

            except Exception as e:
                retries += 1
                logger.error(f"ERROR: {e}", color="<red>")
                await asyncio.sleep(min(backoff, 2))  # Exponential backoff
                backoff *= 1.2  # Meningkatkan backoff setelah kegagalan