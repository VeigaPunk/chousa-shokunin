#!/usr/bin/env python3
"""Recheck pinned quotes against checked-in source snapshots.

Usage: python3 corpus/instruments/source-recheck.py --manifest PATH [--source ID]
       python3 corpus/instruments/source-recheck.py --selftest

Manifest paths are relative to the manifest directory. This instrument reads
only local files; a successful check verifies captured bytes, not current
upstream availability or freshness.

Round-30 Q9 enforcement (C1 B1/B2):
- B1: every record's `path` stem must equal its `id`
  (reason=stem-mismatch, exit 1).
- B2: a quote whose normalized text occurs more than once passes only when
  its declared `anchor` line verifies (anchor=N-ok); a missing, out-of-range,
  or broken anchor fails with reason=occurrence-not-unique /
  reason=anchor-out-of-range / reason=anchor-broken (exit 1).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA_VERSION = 1
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
MARKUP_RE = re.compile(r"</?u>")
MIN_QUOTE_CHARS = 12   # normalized minimum: a shorter "quote" matches any capture


def normalize(text):
    """Collapse whitespace and drop capture markup (<u>/</u>) before matching."""
    return " ".join(MARKUP_RE.sub("", text).split())


def emit(out, stable_id, status, detail=""):
    line = f"{stable_id} {status}"
    if detail:
        line += f" {detail}"
    print(line, file=out)


def valid_id(value):
    return isinstance(value, str) and ID_RE.fullmatch(value) is not None


def load_manifest(path, out):
    try:
        manifest_path = Path(path).resolve(strict=True)
        raw = manifest_path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        emit(out, "manifest", "UNAVAILABLE", "reason=missing")
        return None, None
    except (OSError, UnicodeError, json.JSONDecodeError):
        emit(out, "manifest", "UNAVAILABLE", "reason=unreadable-or-invalid")
        return None, None

    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != SCHEMA_VERSION:
        emit(out, "manifest", "UNAVAILABLE", "reason=unsupported-schema")
        return None, None
    records = data.get("sources")
    if not isinstance(records, list) or not records:
        emit(out, "manifest", "UNAVAILABLE", "reason=missing-sources")
        return None, None

    seen = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict) or not valid_id(record.get("id")):
            emit(out, f"manifest:record-{index}", "UNAVAILABLE", "reason=invalid-source-id")
            return None, None
        if record["id"] in seen:
            emit(out, "manifest", "UNAVAILABLE", "reason=duplicate-source-id")
            return None, None
        seen.add(record["id"])

    return manifest_path, records


def anchor_verdict(assertion, raw_lines, occurrences):
    """Return (note, verdict) for one assertion (QUALITY Q9).

    note is the receipt's anchor note; verdict is one of:
      "unique"        — quote occurs once; no anchor required
      "ok"           — declared anchor verifies (anchor=N-ok)
      "missing"       — non-unique quote carries no anchor
      "out-of-range"  — declared anchor outside the snapshot
      "broken"        — declared anchor does not hold the normalized quote

    A quote that occurs more than once must carry an `anchor` line number: the
    pin is verified against the raw snapshot, so a non-unique quote names where
    it is meant to be read instead of relying on substring presence. A unique
    quote needs no anchor and reports no note; a declared anchor that does not
    hold the quote is reported as `anchor=N-BROKEN`. The caller decides whether
    the verdict is fatal (B2: any verdict other than "ok" on a non-unique
    quote is a failure).
    """
    anchor = assertion.get("anchor")
    if anchor is None:
        if occurrences <= 1:
            return "", "unique"
        return " anchor=MISSING", "missing"
    if type(anchor) is not int or anchor < 1 or anchor > len(raw_lines):
        return " anchor=OUT-OF-RANGE", "out-of-range"
    window = " ".join(raw_lines[max(0, anchor - 1):anchor + 3])
    expected = normalize(assertion["quote"])
    if expected and expected in normalize(window):
        return " anchor=%d-ok" % anchor, "ok"
    return " anchor=%d-BROKEN" % anchor, "broken"


def check_source(manifest_path, record, out):
    source_id = record["id"]
    path = record.get("path")
    if not isinstance(path, str) or not path or Path(path).is_absolute():
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-path")
        return 2
    # B1: the capture file stem must equal the record id (QUALITY Q9).
    if Path(path).stem != source_id:
        emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch")
        return 1

    expected = record.get("sha256")
    if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-sha256")
        return 2

    quotes = record.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=missing-quotes")
        return 2
    quote_ids = set()
    for index, assertion in enumerate(quotes, start=1):
        if not isinstance(assertion, dict) or not valid_id(assertion.get("id")):
            emit(out, f"{source_id}:quote-{index}", "UNAVAILABLE", "reason=invalid-quote-id")
            return 2
        if assertion["id"] in quote_ids:
            emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=duplicate-quote-id")
            return 2
        quote_ids.add(assertion["id"])
        if not isinstance(assertion.get("quote"), str) or not assertion["quote"]:
            emit(out, f"{source_id}:{assertion['id']}", "UNAVAILABLE", "reason=empty-quote")
            return 2
        # A quote with no substance after normalization (' ', '<u></u>') matched
        # any capture and would pass silently (r24 RevC1Control forgery route).
        if len(normalize(assertion["quote"])) < MIN_QUOTE_CHARS:
            emit(out, f"{source_id}:{assertion['id']}", "UNAVAILABLE",
                 "reason=quote-too-short-to-be-evidence")
            return 2

    base = manifest_path.parent
    try:
        base = base.resolve(strict=True)
        resolved = (base / path).resolve(strict=True)
        if os.path.commonpath((str(base), str(resolved))) != str(base):
            emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=outside-manifest-directory")
            return 2
        source_bytes = resolved.read_bytes()
    except FileNotFoundError:
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=missing")
        return 2
    except (OSError, RuntimeError, ValueError):
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=unreadable")
        return 2

    actual = hashlib.sha256(source_bytes).hexdigest()
    if actual != expected:
        emit(out, f"{source_id}:sha256", "MISMATCH", f"expected={expected} actual={actual}")
        return 1

    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError:
        emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=not-utf8")
        return 2

    emit(out, f"{source_id}:sha256", "OK")
    status = 0
    normalized_source = normalize(source_text)
    raw_lines = source_text.splitlines()
    for assertion in sorted(quotes, key=lambda item: item["id"]):
        quote_id = assertion["id"]
        occurrences = normalized_source.count(normalize(assertion["quote"]))
        anchor_note, anchor_verdict_result = anchor_verdict(assertion, raw_lines, occurrences)
        # B2: a non-unique quote passes only when its anchor verifies; a
        # missing, out-of-range, or broken anchor is a failure (QUALITY Q9).
        if occurrences > 1 and anchor_verdict_result != "ok":
            anchor_reasons = {
                "missing": "reason=occurrence-not-unique",
                "out-of-range": "reason=anchor-out-of-range",
                "broken": "reason=anchor-broken",
            }
            emit(out, f"{source_id}:{quote_id}", "MISMATCH", anchor_reasons[anchor_verdict_result])
            status = 1
            continue
        if assertion["quote"] in source_text:
            emit(out, f"{source_id}:{quote_id}", "OK",
                 "occurrences=%d%s" % (occurrences, anchor_note))
        elif occurrences:
            # Declared normalization (considerthese/2026-10-24 proposal 1):
            # reader captures carry markup such as <u>…</u>; the receipt names
            # the transformation instead of forcing the entry to quote tags.
            emit(out, f"{source_id}:{quote_id}", "OK",
                 "normalized=markup-whitespace occurrences=%d%s" % (occurrences, anchor_note))
        else:
            emit(out, f"{source_id}:{quote_id}", "MISMATCH", "reason=quote-not-found")
            status = 1
    return status


def recheck(manifest_arg, source_id, out=sys.stdout):
    if source_id is not None and not valid_id(source_id):
        emit(out, "manifest:selection", "UNAVAILABLE", "reason=invalid-source-id")
        return 2

    manifest_path, records = load_manifest(manifest_arg, out)
    if records is None:
        return 2

    if source_id is not None:
        records = [record for record in records if record["id"] == source_id]
        if not records:
            emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=not-listed")
            return 2

    status = 0
    for record in sorted(records, key=lambda item: item["id"]):
        result = check_source(manifest_path, record, out)
        if result == 2:
            status = 2
        elif result == 1 and status == 0:
            status = 1
    return status


def selftest(out=sys.stdout):
    script = Path(__file__).resolve()
    payload = b"Captured fixture supports a verifiable local rule.\n"
    snapshot_digest = hashlib.sha256(payload).hexdigest()

    # Double-occurrence capture: the normalized quote appears on lines 6 and 10,
    # so anchor=6 verifies, anchor=2 is broken, anchor=99 is out of range.
    double_payload = (
        b"filler start A A A\n"
        b"filler B B B\n"
        b"filler C C C\n"
        b"filler D D D\n"
        b"filler E E E\n"
        b"a verifiable local rule occurrence\n"
        b"filler F F F\n"
        b"filler G G G\n"
        b"filler H H H\n"
        b"a verifiable local rule again\n"
        b"filler I I I\n"
    )

    with tempfile.TemporaryDirectory(prefix="source-recheck-") as directory:
        root = Path(directory)
        manifest_path = root / "manifest.json"
        source_path = root / "S900.txt"
        source_path.write_bytes(payload)
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "sources": [{
                "id": "S900",
                "path": source_path.name,
                "sha256": snapshot_digest,
                "quotes": [{
                    "id": "Q1",
                    "quote": "verifiable local rule",
                    "location": "fixture line 1",
                }],
            }],
        }
        manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

        cases = []

        def make_manifest(name, source_id, quotes, capture=payload, capture_name=None):
            path = root / (name + ".json")
            if capture_name is None:
                capture_name = source_id + ".txt"
            (root / capture_name).write_bytes(capture)
            doc = {
                "schema_version": SCHEMA_VERSION,
                "sources": [{
                    "id": source_id,
                    "path": capture_name,
                    "sha256": hashlib.sha256(capture).hexdigest(),
                    "quotes": quotes,
                }],
            }
            path.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="utf-8")
            return path

        def run_case(name, manifest_arg, expected_status, expected_ids,
                     source_id="S900", expected_substr=None):
            try:
                result = subprocess.run(
                    [sys.executable, str(script), "--manifest", str(manifest_arg), "--source", source_id],
                    cwd=str(root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
                observed_ids = [line.split(maxsplit=1)[0] for line in result.stdout.splitlines() if line.strip()]
                passed = (
                    result.returncode == expected_status
                    and observed_ids == expected_ids
                    and not result.stderr
                    and (expected_substr is None or expected_substr in result.stdout)
                )
                observed_status = result.returncode
            except OSError:
                passed = False
                observed_ids = []
                observed_status = "unavailable"
            state = "PASS" if passed else "FAIL"
            print(
                f"SELFTEST {name} {state} expected-exit={expected_status} observed-exit={observed_status} "
                f"expected-ids={','.join(expected_ids)} observed-ids={','.join(observed_ids)}",
                file=out,
            )
            cases.append(passed)

        run_case("clean", manifest_path, 0, ["S900:sha256", "S900:Q1"])

        source_path.write_bytes(payload + b"corruption\n")
        run_case("corrupt", manifest_path, 1, ["S900:sha256"])

        source_path.unlink()
        run_case("missing-source", manifest_path, 2, ["S900:source"])

        run_case("missing-manifest", root / "absent.json", 2, ["manifest"])

        stem_manifest = make_manifest(
            "stem",
            "S901",
            [{"id": "Q1", "quote": "verifiable local rule", "location": "fixture line 1"}],
            capture_name="S900.txt",
        )
        run_case(
            "stem-mismatch", stem_manifest, 1, ["S901:manifest"],
            source_id="S901", expected_substr="reason=stem-mismatch",
        )

        q9_quote = {"id": "Q1", "quote": "verifiable local rule"}
        double_missing = make_manifest("double-missing", "S900", [dict(q9_quote)], capture=double_payload)
        run_case(
            "double-occurrence", double_missing, 1, ["S900:sha256", "S900:Q1"],
            expected_substr="reason=occurrence-not-unique",
        )

        double_ok = make_manifest("double-ok", "S900", [dict(q9_quote, anchor=6)], capture=double_payload)
        run_case(
            "double-occurrence-anchored", double_ok, 0, ["S900:sha256", "S900:Q1"],
            expected_substr="anchor=6-ok",
        )

        double_range = make_manifest("double-range", "S900", [dict(q9_quote, anchor=99)], capture=double_payload)
        run_case(
            "double-occurrence-out-of-range", double_range, 1, ["S900:sha256", "S900:Q1"],
            expected_substr="reason=anchor-out-of-range",
        )

        double_broken = make_manifest("double-broken", "S900", [dict(q9_quote, anchor=2)], capture=double_payload)
        run_case(
            "double-occurrence-broken", double_broken, 1, ["S900:sha256", "S900:Q1"],
            expected_substr="reason=anchor-broken",
        )

        # Round-31: the final `else` (a quote absent from the capture) had no
        # failing case, so accepting a not-found quote survived the selftest
        # (MutSRExisting M5). This case pins that rejection path.
        absent_quote = make_manifest(
            "quote-absent", "S900",
            [{"id": "Q1", "quote": "absent from the fixture capture"}],
        )
        run_case(
            "quote-absent", absent_quote, 1, ["S900:sha256", "S900:Q1"],
            expected_substr="S900:Q1 MISMATCH reason=quote-not-found",
        )

    failed = sum(1 for passed in cases if not passed)
    print(f"selftest cases={len(cases)} failures={failed}", file=out)
    return 0 if failed == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Recheck exact quotes in pinned local source snapshots.")
    parser.add_argument("--manifest", help="JSON manifest with local source paths, SHA-256 pins, and quote assertions")
    parser.add_argument("--source", help="check one source ID from the manifest")
    parser.add_argument("--selftest", action="store_true",
                        help="run isolated controls: clean/corrupt/missing plus B1 stem, B2 anchor and quote-absent limbs")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.manifest is not None or args.source is not None:
            emit(sys.stdout, "manifest:selection", "UNAVAILABLE", "reason=selftest-takes-no-manifest-or-source")
            return 2
        return selftest()
    if args.manifest is None:
        emit(sys.stdout, "manifest", "UNAVAILABLE", "reason=missing-required-argument")
        return 2
    return recheck(args.manifest, args.source)


if __name__ == "__main__":
    sys.exit(main())
