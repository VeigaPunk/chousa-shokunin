import importlib.util
from pathlib import Path

lane = Path(__file__).resolve().parents[5]
p = lane / "corpus/evidence/round30/c2-count.py"
s = importlib.util.spec_from_file_location("frozen_c2_v3", p)
c2 = importlib.util.module_from_spec(s)
s.loader.exec_module(c2)
body = b"x" * 2400
n = -(-len(body) // 6)
for framing in ("cl", "chunked"):
    wire = c2.H.Server._frame(body, framing, lambda b: [b[i:i + n] for i in range(0, len(b), n)])
    completion = len(wire) * (6.0 - 0.8) / 6.0
    print("slow-ok", framing, "pieces=", len(wire), "deadline=6.0 completion_s=", completion)
spec = {"id": "probe", "kind": "rebind-redirect", "label": "VERBATIM", "routed": ["8.8.8.8", "1.1.1.1"], "deadline": 3.0, "bound": 4.5}
net = [{"ev": "resolve", "host": "first.test", "result": ["8.8.8.8"]},
       {"ev": "connect", "dest": "8.8.8.8", "port": 80},
       {"ev": "resolve", "host": "redirect.test", "result": ["1.1.1.1"]},
       {"ev": "connect", "dest": "8.8.8.8", "port": 80}]
for name, events, wall in [("wrong-hop-address", net, 0.1), ("no-resolution", [net[1]], 0.1), ("beyond-DEADLINE", net[:2], 4.4)]:
    ok, row = c2.score(spec, {"verdicts": {"probe": "VERBATIM"}, "net": events, "wall": wall, "killed": False, "rc": 0})
    print(name, "match=", ok, "validated_only=", row["validated_only"], "bound_ok=", row["bound_ok"])
