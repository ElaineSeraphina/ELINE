import os  # Pastikan modul os diimpor

def load_proxies():
    """Memuat daftar proxy dari file local_proxies.txt."""
    proxy_file = 'data/local_proxies.txt'
    
    # Mengecek apakah file ada
    if not os.path.exists(proxy_file):
        raise FileNotFoundError(f"File {proxy_file} tidak ditemukan!")
    
    # Membaca isi file
    with open(proxy_file, 'r') as file:
        proxies = file.read().splitlines()
    
    return proxies
