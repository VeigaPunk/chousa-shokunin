#!/usr/bin/env python3
"""Critic driver: scores three custom round-36 C2 variants through the
committed counter's own machinery (imported, not edited):

  CFS-call-for-show   query the pinned recorder with the record's real pattern,
                      discard grep's answer, answer by exact search
  REFACTOR-deep       rename both matchers AND move argv construction into
                      helpers (legitimate refactor; must NOT be killed)
  FORGE-recorder-read read the recorder script, learn marker+log path, append
                      forged per-record argv lines, never query the recorder
                      for matching (active anti-instrumentation probe)

Usage: score-variants.py SEED RECEIPT_JSON
Env: C2_TMP must exist. Read-only on lane files.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GATE = os.path.join(LANE, "tools/research-gate.sh")
WITNESS = os.path.join(LANE, "tools/argv-witness.py")
CNT = os.path.join(LANE, "corpus/evidence/round36/c2-count.py")

spec = importlib.util.spec_from_file_location("c2count", CNT)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

MINE = ["CFS-call-for-show", "REFACTOR-deep", "FORGE-recorder-read"]


def build_cfs(text, helper, chunk_helper):
    lines = text.splitlines(keepends=True)
    out = []
    n_show = 0
    for l in lines:
        out.append(l)
        if l.strip() == 'regex=$(tok_hex_pattern "$span")':
            out.append("  printf '%s' \"$hay\" | grep -a -z -b -o -P -- \"$regex\" >/dev/null 2>&1 || :\n")
            out.append('  printf \'%s\' "$hay" | python3 "' + helper + '" "$span"\n')
            out.append("  return 0\n")
            n_show += 1
    assert n_show == 1, "direct regex anchor count %d" % n_show
    text = "".join(out)
    old = '  done < <(printf \'%s\' "$hay" | grep -a -z -b -o -P -- "$pattern")'
    assert text.count(old) == 1, "chunk pipeline anchor count %d" % text.count(old)
    new = ('  done < <( { printf \'%s\' "$hay" | grep -a -z -b -o -P -- "$pattern" >/dev/null 2>&1 || :'
           '; printf \'%s\' "$hay" | python3 "' + chunk_helper + '" "$chunk"; } )\n')
    return text.replace(old, new)


REFACTOR_HELPERS = (
    "tso_grep_offsets() { # HAY PATTERN -> one start offset per line, via the pinned grep\n"
    "  local hay=$1 pattern=$2 occurrence\n"
    "  while IFS= read -r -d '' occurrence; do\n"
    "    printf '%s\\n' \"${occurrence%%:*}\"\n"
    "  done < <(printf '%s' \"$hay\" | grep -a -z -b -o -P -- \"$pattern\")\n"
    "}\n"
    "tso_chunk_candidates() { # HAY PATTERN -> raw -b -o NUL records, via the pinned grep\n"
    "  printf '%s' \"$1\" | grep -a -z -b -o -P -- \"$2\"\n"
    "}\n"
)

DIRECT_BLOCK = (
    "  regex=$(tok_hex_pattern \"$span\")\n"
    "  while IFS= read -r -d '' occurrence; do\n"
    "    printf '%s\\n' \"${occurrence%%:*}\"\n"
    "  done < <(printf '%s' \"$hay\" | grep -a -z -b -o -P -- \"$regex\")\n"
)
DIRECT_BLOCK_NEW = "  regex=$(tok_hex_pattern \"$span\")\n  tso_grep_offsets \"$hay\" \"$regex\"\n"
CHUNK_PIPE_OLD = '  done < <(printf \'%s\' "$hay" | grep -a -z -b -o -P -- "$pattern")'
CHUNK_PIPE_NEW = '  done < <(tso_chunk_candidates "$hay" "$pattern")'


def build_refactor(text):
    text = c2.build_rename(text)
    assert text.count(DIRECT_BLOCK) == 1, "direct block %d" % text.count(DIRECT_BLOCK)
    text = text.replace(DIRECT_BLOCK, DIRECT_BLOCK_NEW)
    assert text.count(CHUNK_PIPE_OLD) == 1, "chunk pipe %d" % text.count(CHUNK_PIPE_OLD)
    text = text.replace(CHUNK_PIPE_OLD, CHUNK_PIPE_NEW)
    anchor = "tso_direct_x() { # HAY SPAN -> stdout: byte offset of each occurrence\n"
    assert text.count(anchor) == 1, "rename anchor %d" % text.count(anchor)
    return text.replace(anchor, REFACTOR_HELPERS + anchor)


FORGE_FN = '''_w36_forge() { # SPAN: learn the recorder log+marker from its own script text,
  # then append one forged -a -z -b -o -P argv line for this record. The
  # witness log is user-writable; this is the round's stated limit.
  local span=$1 line rest q
  q=$(printf '\\047')
  if [[ -z ${W36F_TRIED:-} ]]; then
    W36F_TRIED=1
    if [[ -n ${GREP_BIN:-} && -f $GREP_BIN ]]; then
      while IFS= read -r line || [[ -n $line ]]; do
        if [[ $line == *W36CALL-* ]]; then
          rest=${line##*W36CALL-}
          W36F_MARK="W36CALL-${rest%%"$q"*}"
        fi
        if [[ $line == *">>$q"* ]]; then
          rest=${line#*">>$q"}
          W36F_LOG=${rest%%"$q"*}
        fi
      done < "$GREP_BIN"
    fi
  fi
  [[ -n ${W36F_MARK:-} && -n ${W36F_LOG:-} ]] || return 0
  { printf '%s\\n' "$W36F_MARK"; printf -- '-a\\0-z\\0-b\\0-o\\0-P\\0--\\0%s\\0\\n' "$(tok_hex_pattern "$span")"; } >>"$W36F_LOG"
}
'''


def build_forge(text, helper, chunk_helper):
    anchor = "tok_span_offsets() { # HAY SPAN -> stdout: byte offset of each occurrence, one per line\n"
    assert text.count(anchor) == 1, "dispatcher anchor %d" % text.count(anchor)
    text = text.replace(anchor, FORGE_FN + anchor)
    locals_line = "  local hay=$1 span=$2\n"
    assert text.count(locals_line) >= 1, "locals anchor"
    # hook only the dispatcher's locals line (first occurrence)
    text = text.replace(locals_line, locals_line + "  _w36_forge \"$span\"\n", 1)
    # matching never queries the recorder: direct -> python exact search
    lines = text.splitlines(keepends=True)
    out = []
    n = 0
    for l in lines:
        out.append(l)
        if l.strip() == 'regex=$(tok_hex_pattern "$span")':
            out.append('  printf \'%s\' "$hay" | python3 "' + helper + '" "$span"\n')
            out.append("  return 0\n")
            n += 1
    assert n == 1, "direct regex anchor %d" % n
    text = "".join(out)
    assert text.count(CHUNK_PIPE_OLD) == 1, "chunk pipe %d" % text.count(CHUNK_PIPE_OLD)
    text = text.replace(CHUNK_PIPE_OLD,
                        '  done < <(printf \'%s\' "$hay" | python3 "' + chunk_helper + '" "$chunk")\n')
    return text


def main():
    seed = int(sys.argv[1])
    receipt_path = sys.argv[2]
    base = os.environ.get("C2_TMP")
    root = tempfile.mkdtemp(prefix="r36crit-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    helper = os.path.join(root, "span_search.py")
    with open(helper, "w", encoding="utf-8") as f:
        f.write(c2.HELPER_SRC)
    chunk_helper = os.path.join(root, "chunk_search.py")
    with open(chunk_helper, "w", encoding="utf-8") as f:
        f.write(c2.CHUNK_HELPER_SRC)
    gate_text = open(GATE, encoding="utf-8", errors="surrogateescape").read()

    landed = c2.run_witness(WITNESS, GATE, seed, os.path.join(root, "w-landed"),
                            os.path.join(root, "r-landed.json"))

    builds = {
        "CFS-call-for-show": build_cfs(gate_text, helper, chunk_helper),
        "REFACTOR-deep": build_refactor(gate_text),
        "FORGE-recorder-read": build_forge(gate_text, helper, chunk_helper),
    }
    receipt = {"seed": seed, "gate": GATE, "gate_sha256": c2.sha256_file(GATE),
               "witness": WITNESS, "witness_sha256": c2.sha256_file(WITNESS),
               "variants": {}}
    for name, text in builds.items():
        vgate = os.path.join(root, name + ".sh")
        with open(vgate, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(vgate, 0o755)
        syntax = subprocess.run(["bash", "-n", vgate], capture_output=True, text=True)
        rec = c2.run_witness(WITNESS, vgate, seed, os.path.join(root, "w-" + name),
                             os.path.join(root, "r-" + name + ".json"))
        receipt["variants"][name] = {
            "gate_sha256": c2.sha256_file(vgate), "syntax_ok": syntax.returncode == 0,
            "syntax_stderr": syntax.stderr[-400:] if syntax.returncode else "",
            "witness": rec.get("witness"), "output_match": rec.get("output_match"),
            "output_total": rec.get("output_total"), "output_full": rec.get("output_full"),
            "attributed": len(rec.get("attribution") or {}),
            "unattributed": rec.get("unattributed"),
            "matcher_calls": rec.get("matcher_calls"), "recorder_calls": rec.get("recorder_calls"),
            "exit": rec.get("exit"), "stdout": rec.get("stdout"),
            "gate_rc": rec.get("gate_rc"), "drift": rec.get("drift"),
            "stderr_tail": (rec.get("stderr_tail") or "")[-300:],
        }
        v = receipt["variants"][name]
        survives = (v["witness"] == "pass" and v["output_full"]
                    and v["attributed"] == v["output_total"])
        print("%-22s output=%s/%s witness=%s attrib=%s/%s matcher_calls=%s recorder_calls=%s -> %s"
              % (name, v["output_match"], v["output_total"], v["witness"],
                 v["attributed"], v["output_total"], v["matcher_calls"],
                 v["recorder_calls"], "SURVIVES (not separated)" if survives else "separated"))
    receipt["landed"] = {k: landed.get(k) for k in
                         ("witness", "output_full", "output_match", "output_total",
                          "attribution", "unattributed", "matcher_calls", "recorder_calls")}
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1, sort_keys=True)
    print("receipt: %s" % receipt_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
