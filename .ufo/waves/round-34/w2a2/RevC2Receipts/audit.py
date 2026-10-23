#!/usr/bin/env python3
import ast
import datetime
import hashlib
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
PIN = "707da8184a0fc4d10ab3f17271556cdf364f0af5"
BEFORE = "bf7c931a"
COUNTER = "corpus/evidence/round34/c2-count.py"
GATE = "tools/research-gate.sh"
DIR = ".ufo/waves/round-34/measure-a2"
NAMES = [f"c2-{phase}-s{seed}.json" for phase, seeds in (("before", (5011, 5023)), ("after", (5011, 5023, 5033, 5047))) for seed in seeds]
EXPECTED = {"before": {5011, 5023}, "after": {5011, 5023, 5033, 5047}}


def git(*args):
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    return subprocess.check_output(["git", "-C", LANE, *args], env=env)


def blob(rev, path):
    return git("show", f"{rev}:{path}")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def grep_paths(rev, needle):
    p = subprocess.run(["git", "-C", LANE, "grep", "-l", "-F", needle, rev, "--"],
                       capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise RuntimeError(p.stderr)
    return sorted(line.split(":", 1)[1] for line in p.stdout.splitlines())


def scan(rev, counter_sha, expected_schema_paths=None):
    schema_paths = grep_paths(rev, "chousa-r34-c2-receipt/v1")
    digest_paths = grep_paths(rev, counter_sha)
    matching = []
    for path in sorted(set(schema_paths + digest_paths)):
        if not path.endswith(".json"):
            continue
        try:
            obj = json.loads(blob(rev, path))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(obj, dict) and obj.get("counter_sha256") == counter_sha:
            matching.append((path, obj))
    return schema_paths, digest_paths, matching


def main():
    counter_bytes = blob(PIN, COUNTER)
    counter_sha = sha(counter_bytes)
    gate_before = sha(blob(BEFORE, GATE))
    gate_after = sha(blob(PIN, GATE))
    tree = ast.parse(counter_bytes.decode())
    class_counts = next(ast.literal_eval(n.value) for n in tree.body
                        if isinstance(n, ast.Assign) and len(n.targets) == 1
                        and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "CLASS_COUNTS")
    classes = {name: count for name, count, _truth in class_counts}
    total = sum(classes.values())
    assert total == 37
    expected_keys = {"schema", "counter_sha256", "gate", "gate_sha256", "seed", "utc", "elapsed_s", "gate_rc", "gate_timed_out", "gate_stderr_tail", "total", "matched", "label", "predicate_holds", "per_class", "misses"}
    seeds = {"before": set(), "after": set()}
    for name in NAMES:
        path = f"{DIR}/{name}"
        raw = blob(PIN, path)
        live = open(os.path.join(LANE, path), "rb").read()
        assert raw == live, f"worktree differs from pinned blob: {path}"
        r = json.loads(raw)
        phase = name.split("-", 2)[1]
        assert set(r) == expected_keys, f"fields {path}: {sorted(set(r) ^ expected_keys)}"
        assert r["schema"] == "chousa-r34-c2-receipt/v1"
        assert r["counter_sha256"] == counter_sha
        assert r["gate"] == GATE
        assert r["gate_sha256"] == (gate_before if phase == "before" else gate_after)
        assert type(r["seed"]) is int and r["seed"] in EXPECTED[phase]
        assert r["seed"] not in seeds[phase], f"duplicate {phase} seed"
        seeds[phase].add(r["seed"])
        datetime.datetime.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ")
        assert type(r["elapsed_s"]) in (int, float) and r["elapsed_s"] >= 0
        assert r["gate_rc"] == 1 and r["gate_timed_out"] is False
        assert isinstance(r["gate_stderr_tail"], str)
        assert r["total"] == total
        assert r["label"] == f"DEADZONE_MATCH={r['matched']}/{total}"
        assert type(r["matched"]) is int and 0 <= r["matched"] <= total
        assert type(r["predicate_holds"]) is bool and r["predicate_holds"] == (r["matched"] == total)
        pc = r["per_class"]
        assert set(pc) == set(classes)
        parsed = {}
        for cls, value in pc.items():
            assert isinstance(value, str) and value.count("/") == 1
            got, denom = map(int, value.split("/"))
            assert denom == classes[cls] and 0 <= got <= denom
            parsed[cls] = (got, denom)
        assert sum(denom for _, denom in parsed.values()) == total
        assert sum(got for got, _ in parsed.values()) == r["matched"]
        assert isinstance(r["misses"], list) and len(r["misses"]) == total - r["matched"]
        if phase == "before":
            assert r["matched"] == 21 and r["predicate_holds"] is False
            assert "regular expression is too large" in r["gate_stderr_tail"]
        else:
            assert r["matched"] == total and r["predicate_holds"] is True
            assert r["gate_stderr_tail"] == ""
        print(f"RECEIPT_OK {path} seed={r['seed']} gate={r['gate_sha256'][:16]} label={r['label']} predicate_holds={str(r['predicate_holds']).lower()} class-denominators={sum(x[1] for x in parsed.values())} class-matches={sum(x[0] for x in parsed.values())}")
    assert seeds == EXPECTED
    print(f"SEEDS_DISTINCT_WITHIN_PHASE before={sorted(seeds['before'])} after={sorted(seeds['after'])}; paired controls intentionally reuse 5011,5023")
    print(f"HASHES counter@{PIN[:8]}={counter_sha} gate@{BEFORE}={gate_before} gate@{PIN[:8]}={gate_after}")
    for rev in (PIN, "HEAD"):
        schema_paths, digest_paths, matches = scan(rev, counter_sha)
        print(f"CENSUS {rev}: schema_paths={len(schema_paths)} current_counter_json={len(matches)}")
        for path, obj in matches:
            print(f"  {path}: gate={obj.get('gate_sha256')} label={obj.get('label')} matched={obj.get('matched')} predicate_holds={obj.get('predicate_holds')}")
        if rev == PIN:
            assert {path for path, _obj in matches} == {f"{DIR}/{n}" for n in NAMES}
            assert len(matches) == 6
            low_landed = [(path, obj.get("label")) for path, obj in matches
                          if obj.get("gate_sha256") == gate_after and obj.get("matched", total) < total]
            assert not low_landed, f"below-target receipt on landed gate: {low_landed}"
        else:
            assert {path for path, _obj in matches} == {f"{DIR}/{n}" for n in NAMES}
    head = git("rev-parse", "HEAD").decode().strip()
    print(f"OBSERVED_HEAD={head}; PINNED={PIN}; same={head == PIN}")


if __name__ == "__main__":
    main()
