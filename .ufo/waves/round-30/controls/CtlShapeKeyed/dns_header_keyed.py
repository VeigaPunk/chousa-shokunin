#!/usr/bin/env python3
"""Control: infer labels from DNS changes and exact bad-response header signatures.

No total timer and no pinned address: each stable hop resolves at least three times.
A global-to-private DNS change is guessed VERBATIM without fetching that hop.
The round-29 HTML extraction is imported unchanged.
"""
import argparse
import importlib.util
import ipaddress
from pathlib import Path
import socket
import urllib.parse

DEADLINE = 30.0
BASE_PATH = Path(__file__).resolve().parents[5] / "tools" / "quote-reopen.py"
_spec = importlib.util.spec_from_file_location("header_round29", BASE_PATH)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def addresses(host, port):
    return [row[4][0] for row in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)]


def fetch_guess(url):
    for _ in range(11):
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "http" or not parts.hostname:
            return "UNREACHABLE", None
        host, port = parts.hostname, parts.port or 80
        first = addresses(host, port)
        if not first or any(not ipaddress.ip_address(a).is_global for a in first):
            return "UNREACHABLE", None
        second = addresses(host, port)
        if any(not ipaddress.ip_address(a).is_global for a in second):
            return "VERBATIM", None
        target = parts.path or "/"
        if parts.query:
            target += "?" + parts.query
        # create_connection resolves again; the earlier validated answers are not pinned.
        with socket.create_connection((host, port), timeout=DEADLINE) as conn:
            conn.sendall(("GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n"
                          % (target, host)).encode("ascii"))
            with conn.makefile("rb") as stream:
                head = bytearray()
                while not head.endswith(b"\r\n\r\n") and len(head) < 65536:
                    byte = stream.read(1)
                    if not byte:
                        return "UNREACHABLE", None
                    head.extend(byte)
                    if head.endswith(b"\r\nX-Pad: "):
                        return "UNREACHABLE", None
                lines = bytes(head).decode("latin-1").split("\r\n")
                status = int(lines[0].split()[1])
                headers = {}
                for line in lines[1:]:
                    key, sep, value = line.partition(":")
                    if sep:
                        headers[key.lower()] = value.strip()
                if status in (301, 302, 303, 307, 308):
                    url = urllib.parse.urljoin(url, headers["location"])
                    continue
                if not 200 <= status < 300:
                    return "UNREACHABLE", None
                if (headers.get("content-length") in {"200000", "5000"}
                        or headers.get("transfer-encoding", "").lower() == "chunked"):
                    return "UNREACHABLE", None
                size = headers.get("content-length")
                body = stream.read(int(size)) if size is not None else stream.read()
                text = base.norm(base.html_to_text(body.decode("utf-8", "replace")))
                return "TEXT", text
    return "UNREACHABLE", None


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["verify"])
    parser.add_argument("--items", required=True)
    parser.add_argument("--registry", required=True)
    args = parser.parse_args(argv)
    rows = base.registry_rows(args.registry)
    cache = {}
    verdicts = []
    for item_id, sid, quote in base.load_items(args.items):
        url = base.registry_url(rows.get(sid))
        if url is None:
            verdict = "NO_SOURCE"
        elif len(base.norm(quote).split()) > 25:
            verdict = "TOO_LONG"
        else:
            if url not in cache:
                try:
                    cache[url] = fetch_guess(url)
                except (OSError, ValueError, KeyError, IndexError):
                    cache[url] = ("UNREACHABLE", None)
            verdict, text = cache[url]
            if verdict == "TEXT":
                verdict = "VERBATIM" if base.found(text, quote) else "ABSENT"
        verdicts.append(verdict)
        print("QUOTE_REOPEN\t%s\t%s\tDNS/header-signature control" % (item_id, verdict))
    return 0 if all(v == "VERBATIM" for v in verdicts) else 1
