def load_proxies():
    """Memuat daftar proxy dari file local_proxies.txt."""
    if not os.path.exists('data/local_proxies.txt'):
        raise FileNotFoundError("File local_proxies.txt tidak ditemukan!")
    
    with open('data/local_proxies.txt', 'r') as file:
        proxies = file.read().splitlines()
    return proxies