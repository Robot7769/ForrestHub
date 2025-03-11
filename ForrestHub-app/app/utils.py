import socket


def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def is_port_free(ip: str, port: int) -> bool:
    """Check if port is free on given IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Timeout pro rychlejší odpověď
        return s.connect_ex((ip, port)) != 0


def find_free_port(ip: str, port: int) -> int:
    """Find free port on given IP address."""
    while not is_port_free(ip, port):
        port += 1
    return port
