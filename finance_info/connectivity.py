# check if we can reach the server first

import socket

from .errors import ConnectionProblem


def ensure_reachable(host: str, port: int = 443, timeout: float = 3.0) -> None:
    try:
        socket.create_connection((host, port), timeout=timeout).close()
    except socket.gaierror:
        raise ConnectionProblem(
            "No internet connection (could not resolve the server name)."
        ) from None
    except OSError:
        raise ConnectionProblem(
            f"Could not reach {host}. Check your connection or firewall."
        ) from None
