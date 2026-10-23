#!/usr/bin/env python3
"""Does a per-operation socket timeout bound a TLS handshake against a dripping server?

Loopback only. The server accepts, sends a TLS record header announcing a 16 KiB handshake
record, then one byte every DRIP seconds. The client wraps the socket exactly as
http.client.HTTPSConnection.connect does (create_connection with timeout, then
context.wrap_socket(server_hostname=...)) with timeout TIMEOUT. Wall time is capped at CAP.
"""
import socket
import ssl
import sys
import threading
import time

DRIP, TIMEOUT, CAP = 0.2, 1.0, 8.0


def server(ls, stop):
    c, _ = ls.accept()
    try:
        c.recv(65536)
        c.sendall(b"\x16\x03\x03\x40\x00")
        while not stop.is_set():
            c.sendall(b"\x02")
            time.sleep(DRIP)
    except OSError:
        pass
    finally:
        c.close()


def main():
    ls = socket.socket()
    ls.bind(("127.0.0.1", 0))
    ls.listen(1)
    stop = threading.Event()
    threading.Thread(target=server, args=(ls, stop), daemon=True).start()
    ctx = ssl.create_default_context()
    t0 = time.monotonic()
    result = ["running"]

    def client():
        try:
            s = socket.create_connection(("127.0.0.1", ls.getsockname()[1]), timeout=TIMEOUT)
            ctx.wrap_socket(s, server_hostname="example.test")
            result[0] = "handshake completed"
        except Exception as e:
            result[0] = "%s after %.2fs" % (type(e).__name__, time.monotonic() - t0)

    th = threading.Thread(target=client, daemon=True)
    th.start()
    th.join(CAP)
    wall = time.monotonic() - t0
    stop.set()
    print("socket timeout=%.1fs drip=%.1fs cap=%.1fs wall=%.2fs client=%s" % (TIMEOUT, DRIP, CAP, wall, result[0]))
    print("UNBOUNDED-BY-PER-OP-TIMEOUT" if result[0] == "running" else "BOUNDED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
