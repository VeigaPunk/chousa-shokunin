#!/usr/bin/env python3
"""R83ExecForge — K2 spec-generalization battery for tools/gate-records.py at 81b8117.

Writes one forged GATE-RECORD line per file under <tree>/forge/, runs the landed tool
per file from the tree root, and records the exact line, the docstring check it targets,
my in-class judgment, the tool output and the exit code.

Run: python3 driver.py <tree> <lane repo> <outdir>
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TREE = os.path.abspath(sys.argv[1])
LANE = os.path.abspath(sys.argv[2])
OUT = os.path.abspath(sys.argv[3])
FORGE = os.path.join(TREE, "forge")
TOOL = os.path.join(TREE, "tools", "gate-records.py")

os.makedirs(FORGE, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- base records
pos = []
for ln in open(os.path.join(TREE, "corpus/evidence/round83/c2-positives.tsv"), encoding="utf-8"):
    f, n, raw = ln.rstrip("\n").split("\t", 2)
    pos.append((f, int(n), raw))
by_sid = {}
for f, n, raw in pos:
    sid = re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
    by_sid[sid] = raw

TIP = os.path.join(OUT, "round-83-tip.md")
tip_recs = {}
for ln in open(TIP, encoding="utf-8"):
    if ln.startswith("GATE-RECORD "):
        tip_recs[re.match(r"^GATE-RECORD (S\d+)", ln).group(1)] = ln.rstrip("\n")

A = by_sid["S209"]          # url/admit
B = by_sid["S199"]          # rev
C = by_sid["S208"]          # url/unreach
D = tip_recs["S009"]        # url/admit, round 83
E = tip_recs["S212"]        # url/admit, round 83 (capture with apostrophes and &)

CAP_A = "corpus/captures/213237301753814b95b24684.txt"
SHA_A = hashlib.sha256(open(os.path.join(TREE, CAP_A), "rb").read()).hexdigest()
CAP_E = "corpus/captures/708022d401fd771fc59bd1d9.txt"
SHA_E = hashlib.sha256(open(os.path.join(TREE, CAP_E), "rb").read()).hexdigest()
RAW_A = "64f98dd135b26d3a253eb4c7738a341a4bdc41951602aedd523cea485289fe87"  # refetch row 153 raw_sha256
TREE_B = "8bff97f27d9806c15a9d821f576782e0e9c04c92"                          # b7803829^{tree}
REV_B = "b7803829922770b890e9f4efdd30d12c3695439a"
REV_B_UP = REV_B.upper()
REV_B_MIX = REV_B[:20].upper() + REV_B[20:]


def sub(line, old, new, count=1):
    assert old in line, (old, line[:80])
    return line.replace(old, new, count)


def kv(line, key, val):
    return re.sub(r"(?<= )" + re.escape(key) + r"=\S+", key + "=" + val, line, count=1)


def with_quote(line, q):
    head = line.split(" quote=", 1)[0]
    return head + ' quote="' + q + '"'


def rev_quote(line, q):
    head = line.split(" quote=", 1)[0]
    return head + " quote=" + q


# ---------------------------------------------------------------- case table
# (label, line, target check, in-class judgment, expected codes)
CASES = []


def add(label, line, check, inclass, expect):
    CASES.append(dict(label=label, line=line, check=check, inclass=inclass, expect=expect))


# --- group 1: capture_sha256 spelling
add("sha-upper16", kv(A, "capture_sha256", "8581CA1827F4AE13…"), "CAPTURE_SHA", "yes: not a prefix of the lowercase sha256 hex", "CAPTURE_SHA")
add("sha-mixed16", kv(A, "capture_sha256", "8581ca1827F4ae13…"), "CAPTURE_SHA", "yes: not a prefix of the lowercase sha256 hex", "CAPTURE_SHA")
add("sha-dots3", kv(A, "capture_sha256", "8581ca1827f4ae13..."), "CAPTURE_SHA", "no: >=16 hex prefix of the capture sha; suffix variant accepted by SHA_RE", "OK")
add("sha-full64", kv(A, "capture_sha256", SHA_A), "CAPTURE_SHA", "no: full prefix", "OK")
add("sha-full64-ellipsis", kv(A, "capture_sha256", SHA_A + "…"), "CAPTURE_SHA", "no: full prefix + documented ellipsis", "OK")
add("sha-raw16", kv(A, "capture_sha256", RAW_A[:16] + "…"), "CAPTURE_SHA", "yes: sha of the .raw file, not the .txt", "CAPTURE_SHA")
add("sha-15hex", kv(A, "capture_sha256", "8581ca1827f4ae1…"), "CAPTURE_SHA", "yes: shorter than 16 hex digits", "CAPTURE_SHA")
add("sha-24hex", kv(A, "capture_sha256", SHA_A[:24] + "…"), "CAPTURE_SHA", "no: >=16 hex prefix", "OK")
add("sha-suffix-x", kv(A, "capture_sha256", "8581ca1827f4ae13…x"), "CAPTURE_SHA", "yes: not a bare hex prefix (trailing junk)", "CAPTURE_SHA")

# --- group 2: refetch binding
add("refetch-diff-id-admit", sub(A, "GATE-RECORD S209", "GATE-RECORD S210"), "REFETCH", "yes: the only row with this url/fetched is id S209", "REFETCH")
add("refetch-diff-id-unreach", sub(C, "GATE-RECORD S208", "GATE-RECORD S207"), "REFETCH", "yes: the row is id S208", "REFETCH")
add("refetch-failed-url-lane", kv(A, "url", "https://www.bmj.com/content/387/bmj.q2458.full.txt"), "REFETCH", "yes: S208's only row is a failed attempt (rc 22, 403); the capture key then also differs", "CAPTURE_KEY,REFETCH")
add("refetch-failed-attempt-time", kv(A, "fetched", "2026-11-06T18:44:31Z"), "REFETCH", "yes: that fetched time belongs to S208's failed row", "REFETCH")

# --- group 3: url spelling
add("url-trailing-slash", kv(A, "url", "https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question/"), "CAPTURE_KEY", "yes: key is sha256(url)[:24]", "CAPTURE_KEY,REFETCH")
add("url-fragment", kv(A, "url", "https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question#x"), "CAPTURE_KEY", "yes: key is sha256(url)[:24]", "CAPTURE_KEY,REFETCH")
add("url-http", kv(A, "url", "http://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question"), "CAPTURE_KEY", "yes: key is sha256(url)[:24]", "CAPTURE_KEY,REFETCH")
add("url-upper-scheme", kv(A, "url", "HTTPS://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question"), "PARSE", "yes: url must match https?:// (case-sensitive)", "PARSE")

# --- group 4: tier / decision
add("tier-lower", kv(A, "tier", "a"), "PARSE", "yes: tier is A|B|C", "PARSE")
add("tier-D", kv(A, "tier", "D"), "PARSE", "yes: tier is A|B|C", "PARSE")
add("decision-maybe", kv(A, "decision", "maybe"), "PARSE", "yes: decision is admit|reject", "PARSE")
add("decision-ADMIT", kv(A, "decision", "ADMIT"), "PARSE", "yes: decision is admit|reject", "PARSE")
add("decision-reject-admit-form", kv(A, "decision", "reject"), "none", "no: the url/admit form documents decision=<admit|reject>", "OK")
add("tier-missing", sub(A, " tier=A", ""), "PARSE", "yes: missing key", "PARSE")

# --- group 5: words spelling
add("words-leading-zero", kv(A, "words", "020"), "PARSE", "yes: bad value for <n>", "PARSE")
add("words-plus", kv(A, "words", "+20"), "PARSE", "yes: bad value for <n>", "PARSE")
add("words-arabic-trailing", kv(A, "words", "2٠"), "WORDS", "yes: token count is 20, the token is not '20'", "WORDS")
add("words-arabic-leading", kv(A, "words", "٢٠"), "PARSE", "yes: bad value for <n>", "PARSE")
add("words-genuine", kv(A, "words", "20"), "none", "no: genuine", "OK")

# --- group 6: quote normalization
q_a = A.split(' quote="', 1)[1][:-1]
add("quote-nbsp", with_quote(A, q_a.replace(" ", "\u00a0", 1)), "none", "no: U+00A0 is whitespace for str.split, the documented normalization", "OK")
add("quote-tab", with_quote(A, q_a.replace(" ", "\t", 1)), "none", "no: tab is whitespace for str.split", "OK")
add("quote-zwsp", with_quote(A, q_a.replace("If ", "If\u200b ", 1)), "QUOTE_ABSENT", "yes: U+200B is Cf, not whitespace, so the quote does not occur", "QUOTE_ABSENT")
q_e = "The Cochrane Collaboration's tool for assessing risk of bias in randomised trials."
add("quote-straight-apostrophe", kv(with_quote(E, q_e), "words", "12"), "none", "no: genuine", "OK")
add("quote-curly-apostrophe", kv(with_quote(E, q_e.replace("'", "\u2019")), "words", "12"), "none", "no: U+2019 folds to ' by the documented normalization", "OK")
add("quote-entity", kv(with_quote(E, "registered in England &amp; Wales."), "words", "5"), "QUOTE_ABSENT", "yes: markup is kept, the capture has '&' not '&amp;'", "QUOTE_ABSENT")
add("quote-entity-genuine", kv(with_quote(E, "registered in England & Wales."), "words", "5"), "none", "no: genuine", "OK")
add("quote-linebreak", kv(with_quote(E, "English Español فارسی Français"), "words", "4"), "none", "no: whitespace runs (including newlines) collapse", "OK")
add("quote-other-capture", kv(with_quote(A, q_e), "words", "12"), "QUOTE_ABSENT", "yes: the quote is in S212's capture, not S209's", "QUOTE_ABSENT")
add("quote-case", with_quote(A, q_a.replace("If changes", "If Changes")), "QUOTE_ABSENT", "yes: matching keeps case", "QUOTE_ABSENT")

# --- group 7: rev form
add("rev-short12", kv(B, "rev", REV_B[:12]), "REV", "yes: rev must be 40 hex", "REV")
add("rev-tag-name", kv(B, "rev", "round-79"), "REV", "yes: rev must be 40 hex", "REV")
add("rev-HEAD", kv(B, "rev", "HEAD"), "REV", "yes: rev must be 40 hex", "REV")
add("rev-tree", kv(B, "rev", TREE_B), "REV", "yes: a tree hash is not a commit", "REV")
add("rev-upper", kv(B, "rev", REV_B_UP), "REV", "yes: not 40 lowercase hex; git does resolve the uppercase id (harm candidate)", "REV")
add("rev-mixed", kv(B, "rev", REV_B_MIX), "REV", "yes: not 40 lowercase hex (harm candidate)", "REV")
add("path-dotdot", kv(B, "path", "corpus/lessons/../lessons/round-79-verifier-spotcheck.md"), "REV", "yes: git does not resolve a '..' path", "REV")
add("path-dot-slash", kv(B, "path", "./corpus/lessons/round-79-verifier-spotcheck.md"), "REV", "yes: git does not resolve a './' path", "REV")
add("path-trailing-slash", kv(B, "path", "corpus/lessons/round-79-verifier-spotcheck.md/"), "REV", "yes: a trailing slash is not a blob path", "REV")
add("path-absolute", kv(B, "path", "/corpus/lessons/round-79-verifier-spotcheck.md"), "REV", "yes: absolute path is not repo-relative", "REV")
add("line-zero", kv(B, "line", "0"), "PARSE", "yes: line=0 is a bad value (LINE would also fire)", "PARSE")
add("line-00", kv(B, "line", "00"), "PARSE", "yes: bad value", "PARSE")
add("line-011", kv(B, "line", "011"), "PARSE", "yes: bad value (leading zero); harm candidate", "PARSE")
add("line-arabic-222", kv(B, "line", "2\u0662\u0662"), "PARSE", "yes: mixed-script numeral; int() silently reads it as 222", "OK")
add("line-arabic-223", kv(B, "line", "2\u0662\u0663"), "LINE", "yes: mixed-script numeral (int() reads 223, quote is on 222)", "LINE")
add("line-plus", kv(B, "line", "+222"), "PARSE", "yes: bad value", "PARSE")
add("line-minus", kv(B, "line", "-222"), "PARSE", "yes: bad value", "PARSE")
add("line-arabic-only", kv(B, "line", "\u0662\u0662\u0662"), "PARSE", "yes: bad value", "PARSE")
add("rev-quote-leading-dquote", rev_quote(kv(kv(kv(kv(B, "rev", "81b81173f19d175e2b2a6b409b2a496d09d0b258"), "path", "tools/gate-records.py"), "line", "8"), "words", "2"), '"Location command".'), "PARSE", "yes/no: the rev form documents quote=<text to end of line>; a leading quote is text (harm candidate)", "PARSE")
add("rev-words-arabic", kv(B, "words", "1\u0662"), "WORDS", "yes: token count is 12, the token is not '12'", "WORDS")
add("rev-genuine-control", B, "none", "no: genuine", "OK")

# --- group 8: class, encoding, key order
add("crlf", A + "\r", "none", "no: universal newlines; genuine record with CRLF", "OK")
add("bom", "\ufeff" + A, "none", "no: U+FEFF is Cf and stripped by the documented class", "OK")
add("zwsp-prefix", "\u200b" + A, "none", "no: U+200B is Cf and stripped by the documented class", "OK")
add("zwsp-inside-key", sub(A, "tier=A", "tier=A\u200b"), "PARSE", "yes: tier value is not A|B|C", "PARSE")
add("second-quote-key", with_quote(A, q_a + " quote=none"), "QUOTE_ABSENT", "yes: the quote text then does not occur", "QUOTE_ABSENT")
add("keys-after-quote", A + " words=20", "PARSE", "yes: extra text after quote=", "PARSE")
add("keys-after-quote-quoted", A + ' words=20"', "QUOTE_ABSENT", "yes: the quote text then does not occur", "QUOTE_ABSENT")
add("dup-id-lines", A + "\n" + A, "none", "no: no check forbids a repeated id", "OK")
add("extra-key", sub(A, " decision=", " note=x decision="), "PARSE", "yes: unknown key", "PARSE")
add("tab-after-gate-record", "GATE-RECORD\t" + A[len("GATE-RECORD "):], "PARSE", "yes: the form requires a space after GATE-RECORD (in class per REC_RE)", "PARSE")
add("double-space-keys", sub(A, " tier=A decision=", " tier=A  decision="), "PARSE", "yes: empty token; harm candidate (keys are whitespace-separated)", "PARSE")
add("tab-between-keys", sub(A, " tier=A decision=", " tier=A\tdecision="), "PARSE", "yes: harm candidate (keys are whitespace-separated)", "PARSE")
add("quote-key-first", "GATE-RECORD S209 quote=\"" + q_a + "\" " + A.split(" quote=")[0][len("GATE-RECORD S209 "):], "PARSE", "yes: quote= must be last", "PARSE")
add("capture-none-admit", kv(A, "capture", "none"), "CAPTURE_PATH", "yes: capture must be corpus/captures/<24 hex>.txt", "CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT")
add("sha-empty", kv(A, "capture_sha256", ""), "PARSE", "yes: empty value", "PARSE")
add("bare-gate-record", "GATE-RECORD", "PARSE", "yes: fits no form", "PARSE")
add("html-comment-block", "<!--\n" + A + "\n-->", "class", "ambiguous: claims.md says an HTML-comment mention is out of class; the docstring's first sentence says any line whose first text is GATE-RECORD is a record", "OK")
add("prose-only", "# no records here\n\nGATE-RECORDS are described in prose only.\n", "class", "no: 'GATE-RECORDS' is not followed by whitespace", "rc1")
add("empty", "# nothing\n", "class", "no: no record", "rc1")
add("mixed-ok-fail", A + "\n" + kv(A, "tier", "B"), "exit", "yes: one genuine, one forged", "rc1")
add("genuine-admit", A, "none", "no: genuine", "OK")
add("genuine-rev", B, "none", "no: genuine", "OK")
add("genuine-unreach", C, "none", "no: genuine", "OK")
add("genuine-s009", D, "none", "no: genuine", "OK")
add("genuine-s212", E, "none", "no: genuine", "OK")
# --- controls isolating the two decisive findings
add("rev-dquote-control", rev_quote(kv(kv(kv(kv(B, "rev", "81b81173f19d175e2b2a6b409b2a496d09d0b258"), "path", "tools/gate-records.py"), "line", "8"), "words", "2"), 'Location command".'), "none", "no: same record as rev-quote-leading-dquote without the leading quote character", "OK")
add("rev-blob", kv(B, "rev", "e688309308e22480b7aff28e30f9b87c1682df67"), "REV", "yes: a blob hash is not a commit", "REV")
add("words-arabic-trailing-control", kv(A, "words", "20"), "none", "no: genuine ASCII form of the same value", "OK")
add("html-comment-inline", "<!-- " + A + " -->", "class", "no: the mention is not the line's first text", "rc1")
add("list-item", "- " + A, "class", "no: the mention is not the line's first text", "rc1")
add("inline-code", "`" + A + "`", "class", "no: the mention is not the line's first text", "rc1")

# ---------------------------------------------------------------- fixture-capture probe
FIX_KEY = hashlib.sha256(b"https://www.bmj.com/content/387/bmj.q2458.full.txt").hexdigest()[:24]
FIX_PATH = "corpus/captures/%s.txt" % FIX_KEY
FIX_TEXT = "A fixture capture written by R83ExecForge for a behaviour probe: the failed-attempt row is the only row for this url.\n"
with open(os.path.join(TREE, FIX_PATH), "w", encoding="utf-8") as fh:
    fh.write(FIX_TEXT)
FIX_SHA = hashlib.sha256(FIX_TEXT.encode()).hexdigest()
add("refetch-failed-url-fixture", kv(kv(sub(A, "url=https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question", "url=https://www.bmj.com/content/387/bmj.q2458.full.txt"), "capture", FIX_PATH), "capture_sha256", FIX_SHA[:24] + "…"), "REFETCH", "yes (fixture capture, not lane bytes): S208's only row is a failed attempt", "REFETCH")
# fix the quote/words for the fixture probe: replace the quote and words
i = len(CASES) - 1
_fq = "the failed-attempt row is the only row for this url."
CASES[i]["line"] = kv(with_quote(CASES[i]["line"], _fq), "words", str(len(_fq.split())))

# ---------------------------------------------------------------- run
def run(files, root=TREE):
    p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", root, "--repo", LANE] + files,
                       cwd=TREE, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


rows = []
for idx, c in enumerate(CASES, 1):
    name = "c%03d-%s.md" % (idx, re.sub(r"[^a-z0-9-]+", "-", c["label"]))
    path = os.path.join(FORGE, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(c["line"] + "\n")
    rc, out, err = run(["forge/" + name])
    line_out = [l for l in out.splitlines() if l.startswith("GATE_RECORD ")]
    got = line_out[0] if line_out else ""
    all_lines = line_out
    codes = ""
    m = re.search(r" (OK|FAIL)(?: (\S+))?$", got)
    if m:
        codes = "OK" if m.group(1) == "OK" else m.group(2)
    rows.append(dict(id=idx, label=c["label"], file="forge/" + name, check=c["check"],
                     inclass=c["inclass"], expect=c["expect"], line=c["line"], got=got, codes=codes,
                     rc=rc, all_lines=all_lines,
                     summary=[l for l in out.splitlines() if l.startswith("GATE_RECORDS ")], err=err.strip()))

# aggregate run over every forged file
all_files = [r["file"] for r in rows]
rc_all, out_all, err_all = run(all_files)
open(os.path.join(OUT, "aggregate-forge-run.txt"), "w", encoding="utf-8").write(
    "$ python3 tools/gate-records.py verify --root %s --repo %s forge/*.md\n%s%s\nrc=%d\n"
    % (TREE, LANE, out_all, err_all, rc_all))

# positive controls: the 15 frozen positives + the 3 round-83 records
lessons = sorted({p[0] for p in pos})
rc_p, out_p, err_p = run(lessons)
open(os.path.join(OUT, "positives-15.txt"), "w", encoding="utf-8").write(
    "$ python3 tools/gate-records.py verify --root %s --repo %s %s\n%s%s\nrc=%d\n"
    % (TREE, LANE, " ".join(lessons), out_p, err_p, rc_p))
rc_t, out_t, err_t = run([os.path.join(OUT, "round-83-tip.md")])
open(os.path.join(OUT, "positives-round83.txt"), "w", encoding="utf-8").write(
    "$ python3 tools/gate-records.py verify --root %s --repo %s %s\n%s%s\nrc=%d\n"
    % (TREE, LANE, os.path.join(OUT, "round-83-tip.md"), out_t, err_t, rc_t))

# exit-contract probes
probes = []
probes.append(("missing-file", run(["forge/no-such-file.md"])))
tmp_root = os.path.join(OUT, "root-no-registry")
shutil.rmtree(tmp_root, ignore_errors=True)
os.makedirs(os.path.join(tmp_root, "corpus", "evidence", "round57"), exist_ok=True)
shutil.copy(os.path.join(TREE, "corpus/evidence/round57/refetch.tsv"), os.path.join(tmp_root, "corpus/evidence/round57/refetch.tsv"))
probes.append(("missing-registry", run(["forge/c001-sha-upper16.md"], root=tmp_root)))
probes.append(("empty-file-rc", run(["forge/c%03d-empty.md" % [r["id"] for r in rows if r["label"] == "empty"][0]])))
probes.append(("prose-only-rc", run(["forge/c%03d-prose-only.md" % [r["id"] for r in rows if r["label"] == "prose-only"][0]])))
with open(os.path.join(OUT, "exit-contract-probes.txt"), "w", encoding="utf-8") as fh:
    for name, (rc, out, err) in probes:
        fh.write("### %s\n%s%s\nrc=%d\n\n" % (name, out, err, rc))

# ---------------------------------------------------------------- receipts
with open(os.path.join(OUT, "cases.json"), "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "cases.tsv"), "w", encoding="utf-8") as fh:
    fh.write("id\tlabel\tcheck\tinclass\texpect\tgot\tcodes\trc\tline\tsummary\n")
    for r in rows:
        fh.write("\t".join([
            str(r["id"]), r["label"], r["check"], r["inclass"], r["expect"],
            r["got"].replace("\t", "\\t"), r["codes"], str(r["rc"]),
            r["line"].encode("unicode_escape").decode("ascii").replace("\t", "\\t"),
            r["summary"][0] if r["summary"] else "",
        ]) + "\n")

print("cases", len(rows))
for r in rows:
    flag = ""
    if r["codes"] == "OK" and r["expect"] != "OK":
        flag = "  <<< ACCEPTED, EXPECTED " + r["expect"]
    elif r["codes"] != r["expect"] and r["expect"] not in ("rc1",):
        flag = "  <<< expected " + r["expect"]
    print("%3d %-32s rc=%d %-28s %s" % (r["id"], r["label"], r["rc"], r["codes"], flag))
print("aggregate rc", rc_all)
print("positives rc", rc_p, [l for l in out_p.splitlines() if l.startswith("GATE_RECORDS ")])
print("round83 rc", rc_t, [l for l in out_t.splitlines() if l.startswith("GATE_RECORDS ")])
for name, (rc, out, err) in probes:
    print("probe", name, "rc", rc, (out.strip().splitlines() or [""])[-1], err.strip()[:80])
