import importlib.util
import os
from pathlib import Path
import random
from collections import Counter

p = Path(__file__).resolve().parents[5] / "corpus/evidence/round30/c1-count.py"
s = importlib.util.spec_from_file_location("frozen_c1_v4", p)
c1 = importlib.util.module_from_spec(s)
s.loader.exec_module(c1)
_, items, *_ = c1.build(random.Random(int.from_bytes(os.urandom(8), "big")))
normal = [it for it in items if it[4] != "order"]
words = Counter(w.lower() for it in normal for w in it[2].split())
print("normal_items=", len(normal), "shared_normal_words=", sum(n > 1 for n in words.values()))
long_item = next(it for it in items if it[5] == "too-long-unreachable")
urlless = next(it for it in items if it[5] == "no-source-urlless")
print("order_quote_duplicated=", long_item[2] == urlless[2], "words=", len(long_item[2].split()))
for framing in ("cl", "chunked"):
    server = object.__new__(c1.H.Server)
    server.docs = {"/probe": (200, [("Content-Type", "text/html")], b"x" * 2400, framing, 5.0)}
    server.kinds = {"/probe": "slow-ok"}
    sends, gaps = [], []
    sink = type("Sink", (), {"sendall": lambda self, data: sends.append(data)})()
    sleep = c1.H.time.sleep
    c1.H.time.sleep = gaps.append
    try:
        server._serve(sink, "/probe")
    finally:
        c1.H.time.sleep = sleep
    print("slow-ok", framing, "gaps=", len(gaps), "completion_s=", sum(gaps), "terminal_ok=", framing != "chunked" or sends[-1].endswith(b"0\r\n\r\n"))
