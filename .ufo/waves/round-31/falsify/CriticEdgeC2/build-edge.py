#!/usr/bin/env python3
"""Hand-built edge fixtures for C2 (inputs the frozen c2-count.py never generates).

Writes a scratch root: source files of unusual shapes + a claims JSONL whose
records carry pins the counter never emits (non-string pins, duplicate keys,
newline-terminated pins, oversize/symlink/hardlink/unreadable/URL sources).
"""
import hashlib, json, os, shutil, stat, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/chousa-r31/w2/CriticEdgeC2/edge-root"
OUTSIDE = os.path.abspath(os.path.join(os.path.dirname(ROOT), "outside-target.txt"))

if os.path.isdir(ROOT):
    shutil.rmtree(ROOT)
os.makedirs(os.path.join(ROOT, "src"))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def w(rel, data):
    p = os.path.join(ROOT, rel)
    with open(p, "wb") as f:
        f.write(data)
    return p

rows = []          # raw JSONL lines (may be hand-built text)
truth = {}         # id -> note

def rec(cid, source, span, sha_val=None, expect="supported", raw=None, note=""):
    truth[cid] = note
    if raw is not None:
        rows.append(raw)
        return
    r = {"id": cid, "claim": "edge " + cid, "source": source, "span": span, "expect": expect}
    if sha_val is not None:
        r["sha256"] = sha_val
    rows.append(json.dumps(r, ensure_ascii=False))

# --- sources -------------------------------------------------------------
empty = b""
p_empty = w("src/empty.txt", empty)
SHA_EMPTY = sha(empty)

nul = b"alpha\x00beta gamma\n"
p_nul = w("src/nul.txt", nul)
SHA_NUL = sha(nul)
SHA_NUL_STRIPPED = sha(nul.replace(b"\x00", b""))

plain = b"hello marker world\nsecond line here\n"
p_plain = w("src/plain.txt", plain)
SHA_PLAIN = sha(plain)

# over the 8 MiB cap (cap is 8388608; 8388609 must be refused)
OVER = b"x" * 8388609
w("src/over.txt", OVER)
SHA_OVER = sha(OVER)

# exactly at the cap (inclusive boundary per the gate header)
AT = b"cap marker line\n" + b"y" * (8388608 - len(b"cap marker line\n"))
p_at = w("src/at.txt", AT)
SHA_AT = sha(AT)

# symlink inside root -> inside root
os.symlink(os.path.abspath(p_plain), os.path.join(ROOT, "src/link-in.txt"))
# symlink inside root -> outside root
with open(OUTSIDE, "wb") as f:
    f.write(b"outside secret bytes\n")
SHA_OUTSIDE = sha(b"outside secret bytes\n")
os.symlink(OUTSIDE, os.path.join(ROOT, "src/link-out.txt"))

# hardlink inside root (nlink = 2); its own target must not be a used source
p_hard_target = w("src/hard-target.txt", b"hard link marker bytes\n")
SHA_HARD_TARGET = sha(b"hard link marker bytes\n")
os.link(p_hard_target, os.path.join(ROOT, "src/hard.txt"))

# filenames with characters that change sha256sum's output format
p_nl_name = w("src/nl\nname.txt", plain)
SHA_NL_NAME = sha(plain)
p_bs_name = w("src/back\\slash.txt", plain)
SHA_BS_NAME = sha(plain)
p_sp_name = w("src/with space.txt", plain)
SHA_SP_NAME = sha(plain)

# unreadable file
p_unread = w("src/unread.txt", plain)
os.chmod(p_unread, 0)

# --- claims --------------------------------------------------------------
rec("E01_empty_pin", "src/empty.txt", "marker", SHA_EMPTY,
    note="empty file, pin = sha256 of empty bytes -> equal -> span verdict")
rec("E02_nul_pin", "src/nul.txt", "alphabeta", SHA_NUL,
    note="NUL file: span 'alphabeta' exists only after NUL is stripped")
rec("E03_nul_stripped_pin", "src/nul.txt", "alphabeta", SHA_NUL_STRIPPED,
    note="NUL file pinned with the NUL-stripped hash -> must be stale")
rec("E04_over_cap", "src/over.txt", "x", SHA_OVER,
    note="8388609 bytes (> cap) with a pin -> must be refused, never hashed")
rec("E05_at_cap", "src/at.txt", "cap marker line", SHA_AT,
    note="exactly 8388608 bytes (cap inclusive) with a matching pin")
rec("E06_url", "https://example.invalid/research.md", "remote text", SHA_PLAIN,
    note="external URL source with a pin -> must be refused, never hashed")
rec("E07_link_in", "src/link-in.txt", "hello marker world", SHA_PLAIN,
    note="symlink to an in-root file")
rec("E08_link_out", "src/link-out.txt", "outside secret bytes", SHA_OUTSIDE,
    note="symlink to an out-of-root file -> must be refused")
rec("E09_hard", "src/hard.txt", "hard link marker bytes", SHA_HARD_TARGET,
    note="hardlink (nlink=2) -> must be refused, never hashed")
rec("E26_nl_filename", "src/nl\nname.txt", "hello marker world", SHA_NL_NAME,
    note="source filename contains a newline (sha256sum escapes it)")
rec("E27_bs_filename", "src/back\\slash.txt", "hello marker world", SHA_BS_NAME,
    note="source filename contains a backslash")
rec("E28_sp_filename", "src/with space.txt", "hello marker world", SHA_SP_NAME,
    note="source filename contains a space (control)")
rec("E10_unread", "src/unread.txt", "hello marker world", SHA_PLAIN,
    note="chmod 000 file with a pin -> must never be a match")
rec("E11_num", "src/plain.txt", "hello marker world", 12345678901234567890,
    note="pin as a JSON number -> must be invalid")
rec("E12_null", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E12_null","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":null}',
    note="pin as JSON null -> must be invalid")
rec("E13_true", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E13_true","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":true}',
    note="pin as JSON true -> must be invalid")
rec("E14_false", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E14_false","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":false}',
    note="pin as JSON false -> must be invalid")
rec("E15_dup_ok_first", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E15_dup_ok_first","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s","sha256":"%s"}' % (SHA_PLAIN, sha(b"other")),
    note="duplicate sha256 keys: first = matching hash")
rec("E16_dup_bad_first", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E16_dup_bad_first","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s","sha256":"%s"}' % (sha(b"other").upper(), SHA_PLAIN),
    note="duplicate sha256 keys: first = UPPERCASE (invalid), second = matching")
rec("E17_dup_stale_first", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E17_dup_stale_first","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s","sha256":"%s"}' % (sha(b"other"), SHA_PLAIN),
    note="duplicate sha256 keys: first = stale, second = matching")
rec("E18_nl_pin", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E18_nl_pin","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s\\n"}' % SHA_PLAIN,
    note="pin = 64 hex + escaped trailing newline -> value is 65 chars")
rec("E19_nl2_pin", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E19_nl2_pin","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s\\n\\n"}' % SHA_PLAIN,
    note="pin = 64 hex + two escaped trailing newlines")
rec("E20_space_pin", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E20_space_pin","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s "}' % SHA_PLAIN,
    note="control: pin = 64 hex + trailing space (must be invalid)")
rec("E21_cr_pin", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E21_cr_pin","source":"src/plain.txt","span":"hello marker world","expect":"supported","sha256":"%s\\r"}' % SHA_PLAIN,
    note="control: pin = 64 hex + escaped CR")
rec("E22_dup_id_key", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E22_dup_id_key","source":"src/plain.txt","span":"hello marker world","expect":"supported","id":"E22b","sha256":"%s"}' % SHA_PLAIN,
    note="duplicate id key, one sha256 -> which id is reported?")

# both fields: C1 line + C2 sha256 (neither counter generates this combination)
rec("E23_line_and_stale", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E23_line_and_stale","source":"src/plain.txt","span":"hello marker world","expect":"supported","line":"7","sha256":"%s"}' % sha(b"other"),
    note="both 'line' (mislocated) and stale 'sha256' -> which observed/finding?")
rec("E24_line_and_match", "src/plain.txt", "hello marker world", None,
    raw='{"id":"E24_line_and_match","source":"src/plain.txt","span":"hello marker world","expect":"supported","line":"7","sha256":"%s"}' % SHA_PLAIN,
    note="both 'line' (mislocated) and matching 'sha256'")
rec("E25_dir_source", "src", "hello marker world", SHA_PLAIN,
    note="directory as source with a pin")

claims = os.path.join(ROOT, "claims.jsonl")
with open(claims, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(rows) + "\n")
with open(os.path.join(ROOT, "truth.json"), "w") as f:
    json.dump(truth, f, indent=1)
print(claims)
