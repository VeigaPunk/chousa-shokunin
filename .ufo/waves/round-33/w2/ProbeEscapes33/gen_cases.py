#!/usr/bin/env python3
"""Probe fixture: escapes inside read-field VALUES on FLAT claim records.

Each case is one JSONL line, one well-formed flat JSON object (no nesting, no
duplicate keys), plus a source file under <root>/src. The raw line text is
written verbatim so the escape spelling under test survives; a spec reader
(python json.loads) decides the truth independently of the gate.

Writes: <out>/claims.jsonl, <out>/src/*, <out>/cases.json (id -> truth view).
"""
import json
import os
import sys
import hashlib

OUT = os.path.abspath(sys.argv[1])
SRC = os.path.join(OUT, "src")
os.makedirs(SRC, exist_ok=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def srcfile(name, text):
    p = os.path.join(SRC, name)
    with open(p, "wb") as f:
        f.write(text.encode("utf-8"))
    return "src/" + name


def body(span, line=2):
    lines = ["alpha beta gamma delta ipsum.",
             "omega %s tau upsilon." % span if line == 2 else "omega filler tau upsilon.",
             "sigma %s kappa lambda." % span if line == 3 else "sigma filler kappa lambda.",
             "rho mu nu xi omicron pi."]
    return "\n".join(lines) + "\n", line + 1  # 1-based line of the span


# case id -> (raw JSON line, note). The line text is authored by hand so the
# escape spelling is exact; json.loads below is the independent spec reader.
CASES = []


def add(cid, line_text, note):
    CASES.append((cid, line_text, note))


# E01: BMP \u escape in span (decodes to cafe-acute).
add("E01_bmp_u_span",
    r'{"id":"E01_bmp_u_span","source":"src/e01.txt","span":"caf\u00e9 au lait","expect":"supported","line":"2"}',
    "BMP \\u00e9 in span decodes to the UTF-8 e-acute present in the source")
# E02: BMP \u escape spelling ASCII letters.
add("E02_bmp_u_ascii",
    r'{"id":"E02_bmp_u_ascii","source":"src/e02.txt","span":"\u0041LPHA","expect":"supported","line":"2"}',
    "\\u0041 decodes to 'A'")
# E03: surrogate pair, source holds the real astral char.
add("E03_surrogate_pair",
    r'{"id":"E03_surrogate_pair","source":"src/e03.txt","span":"smile \ud83d\ude00 here","expect":"supported","line":"2"}',
    "RFC 8259 surrogate pair = one astral char (U+1F600) present in the source")
# E03b: surrogate pair whose decoded-as-'?' form happens to be in the source.
add("E03b_surrogate_pair_question",
    r'{"id":"E03b_surrogate_pair_question","source":"src/e03b.txt","span":"smile \ud83d\ude00 here","expect":"supported","line":"2"}',
    "spec: span absent (source has 'smile ?? here'); a '?'-substituting reader sees a match")
# E04: lone surrogate (not valid Unicode scalar, still valid JSON string).
add("E04_lone_surrogate",
    r'{"id":"E04_lone_surrogate","source":"src/e04.txt","span":"x\ud800y","expect":"supported","line":"2"}',
    "lone surrogate escape: no scalar; absent from source")
# E05: escaped solidus (\/) in span.
add("E05_solidus_span",
    r'{"id":"E05_solidus_span","source":"src/e05.txt","span":"path\/to\/file","expect":"supported","line":"2"}',
    "\\/ decodes to /")
# E06: escaped backslash in span.
add("E06_backslash_span",
    r'{"id":"E06_backslash_span","source":"src/e06.txt","span":"C:\\dir\\file","expect":"supported","line":"2"}',
    "\\\\ decodes to one backslash; source holds C:\\dir\\file literally")
# E07: escaped quotes inside span.
add("E07_quotes_span",
    r'{"id":"E07_quotes_span","source":"src/e07.txt","span":"he said \"stop\" loudly","expect":"supported","line":"2"}',
    "escaped quotes are string content, decoded")
# E08: escaped quote inside id.
add("E08_quote_id",
    r'{"id":"E08_quote_id\"q","source":"src/e08.txt","span":"bravo charlie","expect":"supported","line":"2"}',
    "id with an escaped quote: the printed id decodes")
# E09: escaped solidus inside source path.
add("E09_solidus_source",
    r'{"id":"E09_solidus_source","source":"src\/e09.txt","span":"delta echo","expect":"supported","line":"2"}',
    "source path with \\/ decodes to src/e09.txt")
# E10: raw non-ASCII UTF-8 span (no escape).
add("E10_raw_utf8_span",
    '{"id":"E10_raw_utf8_span","source":"src/e10.txt","span":"naïve façade","expect":"supported","line":"2"}',
    "raw UTF-8 in the JSON string value")
# E11: key spelled with an escape; scope of the check is a JSON *name*.
add("E11_escaped_line_key",
    r'{"id":"E11_escaped_line_key","source":"src/e11.txt","span":"alpha bravo","expect":"supported","l\u0069ne":"9"}',
    "member name l\\u0069ne decodes to 'line'=9; span is on line 2 (claims.md: keys with escapes are NOT claimed)")
# E12: \t escape in span.
add("E12_tab_span",
    r'{"id":"E12_tab_span","source":"src/e12.txt","span":"a\tb","expect":"supported","line":"2"}',
    "\\t decodes to a tab present in the source")
# E13: flat confuser: a string value whose text looks like a member.
add("E13_flat_confuser",
    r'{"id":"E13_flat_confuser","source":"src/e13.txt","span":"foxtrot golf","expect":"supported","note":"{\"line\": \"9\"}"}',
    "string content that looks like a member (item 3); no top-level line")
# E14: \u0000 inside span (bash cannot hold NUL).
add("E14_nul_span",
    r'{"id":"E14_nul_span","source":"src/e14.txt","span":"a\u0000b","expect":"supported","line":"2"}',
    "spec: span is a,NUL,b (absent); a reader that drops NUL sees 'ab' (present)")
# E15: span ends with a backslash (escaped trailing backslash).
add("E15_trailing_backslash",
    r'{"id":"E15_trailing_backslash","source":"src/e15.txt","span":"trail\\","expect":"supported","line":"2"}',
    "span 'trail\\\\' decodes to trail<backslash>")
# E16: braces via \u escapes.
add("E16_u_braces",
    r'{"id":"E16_u_braces","source":"src/e16.txt","span":"\u007bx\u007d","expect":"supported","line":"2"}',
    "\\u007b/\\u007d decode to braces")
# E17: sha256 pin spelled with a \u escape.
add("E17_sha_u_escape",
    r'{"id":"E17_sha_u_escape","source":"src/e17.txt","span":"hotel india","expect":"supported","line":"2","sha256":"PIN_PLACEHOLDER"}',
    "sha pin where the first hex digit is \\u0036; decoded pin must equal the file sha")
# E18: escaped quote inside the source path (a filename that holds a quote).
add("E18_quote_source",
    r'{"id":"E18_quote_source","source":"src\/qu\"ote.txt","span":"juliett kilo","expect":"supported","line":"2"}',
    "source path decodes to src/qu\"ote.txt")
# E19: escaped quote + solidus + backslash in one span.
add("E19_mixed_span",
    r'{"id":"E19_mixed_span","source":"src/e19.txt","span":"a\"b\/c\\\\d","expect":"supported","line":"2"}',
    "mixed escapes decode to a\"b/c\\\\d (quote, slash, one backslash)")

# E20: a string value carrying an escaped quote, a comma and braces; the read
# keys follow it, so the reader must resynchronise after the string.
add("E20_quote_comma_note",
    r'{"id":"E20_quote_comma_note","note":"a\", b {c}","source":"src/e20.txt","span":"november oscar","expect":"supported","line":"2"}',
    "escaped quote + comma + braces inside a string value before the read keys")
# E21: an empty member name before the read keys (valid JSON, unread).
add("E21_empty_key",
    r'{"":1,"id":"E21_empty_key","source":"src/e21.txt","span":"papa quebec","expect":"supported","line":"2"}',
    "empty member name is valid JSON and must not disturb the scan")
# E22: a read key holding a number instead of a string.
add("E22_line_number",
    r'{"id":"E22_line_number","source":"src/e22.txt","span":"romeo sierra","expect":"supported","line":2}',
    "line is a number: invalid both before and after (r31 rule)")
# E23: escaped quotes spelled as \\u0022 (unicode escape, not \\").
add("E23_u_quote_span",
    r'{"id":"E23_u_quote_span","source":"src/e23.txt","span":"say \u0022hi\u0022","expect":"supported","line":"2"}',
    "\\u0022 decodes to a quote inside the span")

# E24: the line value itself spelled with a \u escape ('2').
add("E24_u_line_value",
    r'{"id":"E24_u_line_value","source":"src/e24.txt","span":"tango uniform","expect":"supported","line":"\u0032"}',
    "line value ('2') spelled with \\u0032")
# E25: a string value ending in an escaped backslash, read keys after it.
add("E25_note_trailing_backslash",
    r'{"id":"E25_note_trailing_backslash","note":"ends with backslash \\","source":"src/e25.txt","span":"victor whiskey","expect":"supported","line":"2"}',
    "note body ends with \\\\ before the closing quote; scanner must not swallow the quote")
# E26: \u005c (backslash spelled as a unicode escape) inside a span.
add("E26_u_backslash_span",
    r'{"id":"E26_u_backslash_span","source":"src/e26.txt","span":"a\u005cb","expect":"supported","line":"2"}',
    "\\u005c decodes to one backslash (source holds a\\b)")
# E27: a note whose text spells a member using \\u0022 quotes (no raw quotes).
add("E27_note_u_quotes",
    r'{"id":"E27_note_u_quotes","note":"\u0022line\u0022: 9","source":"src/e27.txt","span":"xray yankee","expect":"supported","line":"2"}',
    "value containing the escaped spelling of a member: still string content")
# E28: raw astral UTF-8 in the span (4-byte character, no escape).
add("E28_raw_astral_span",
    '{"id":"E28_raw_astral_span","source":"src/e28.txt","span":"smile 😀 here","expect":"supported","line":"2"}',
    "raw UTF-8 astral character in the value, source holds the same bytes")

NAME_OVERRIDE = {"E18_quote_source": 'qu"ote.txt'}

rows = []
cases = {}
for cid, line_text, note in CASES:
    obj = json.loads(line_text)  # independent spec view
    name = NAME_OVERRIDE.get(cid) or (cid.split("_")[0].lower() + ".txt")
    span = obj["span"]
    # source text never holds a lone surrogate or a NUL: those cases put a
    # look-alike line in the source so a lossy reader would falsely match.
    SPECIAL = {"E03b_surrogate_pair_question": "smile ?? here",
               "E04_lone_surrogate": "x z y",
               "E14_nul_span": "ab"}
    text, lno = body(SPECIAL.get(cid, span))
    if cid == "E17_sha_u_escape":
        text, lno = body(span)
        h = sha(text.encode("utf-8"))
        obj["sha256"] = h
        line_text = line_text.replace("PIN_PLACEHOLDER", "\\u00%02x%s" % (ord(h[0]), h[1:]))
        obj = json.loads(line_text)
    rel = srcfile(name, text)
    # the source field in the line must name this file; rewrite via spec value
    if obj["source"] != rel:
        # author wrote it; check the decoded path equals what we wrote
        cases.setdefault("_src_mismatch", []).append((cid, obj["source"], rel))
    rows.append(line_text)
    # independent truth: span presence (naive substring) + line binding
    present = span in text
    line_decl = obj.get("line")
    if line_decl is not None:
        want = str(lno)
        ok_line = line_decl == want
    else:
        ok_line = True
    truth = "supported" if (present and ok_line) else "mislocated"
    cases[cid] = {"note": note, "line": line_text, "spec_span": span,
                  "span_present": present, "line": line_decl,
                  "span_line": lno, "spec_truth": truth,
                  "source_file": rel, "sha256_spec": obj.get("sha256")}

# E18 file name holds a quote: created under src/qu"ote.txt
with open(os.path.join(OUT, "claims.jsonl"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(rows) + "\n")
with open(os.path.join(OUT, "cases.json"), "w", encoding="utf-8") as f:
    json.dump(cases, f, indent=1, ensure_ascii=True)
for cid, got, want in cases.get("_src_mismatch", []):
    print("SRC-MISMATCH", cid, repr(got), repr(want))
print("cases=%d" % len(rows))
