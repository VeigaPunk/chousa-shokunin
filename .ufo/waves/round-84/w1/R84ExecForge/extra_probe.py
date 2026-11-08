#!/usr/bin/env python3
"""Extra probes: CRLF, curly-inside, unicode spaces, BOM, quote-break, second-line quote, path-traversal, symlinks, duplicate key, wrong S-id format."""
import os, subprocess, sys

T = "/fast/scratch/hyaku/chousa-r84/R84ExecForge/tree"
FORGE = os.path.join(T, "forge")
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"

A203 = 'GATE-RECORD S203 url=https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf fetched=2026-11-06T18:44:29Z tier=A decision=admit capture=corpus/captures/f2489455cc311a4de981e926.txt capture_sha256=31493aa66bfd6625… words=13 quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."'
R199 = 'GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 words=12 quote=the battery is fully forgeable through the payload channel on **both** batteries'
A205 = 'GATE-RECORD S205 url=https://www.nlm.nih.gov/bsd/policy/errata.html fetched=2026-11-06T18:44:30Z tier=A decision=admit capture=corpus/captures/371c55117727d526805f030d.txt capture_sha256=08b4b3c0ad9215b0… words=13 quote="the erratum notice is simply linked to the citation for the corrected article."'

probes = {}

def w(fid, content_bytes):
    p = os.path.join(FORGE, fid + ".md")
    with open(p, "wb") as fh:
        fh.write(content_bytes)
    probes[fid] = p
    return p

U = lambda s: s.encode("utf-8")

# CRLF line endings (record at line 2 with \r\n)
w("X001-crlf", U("pre\r\n") + U(A203) + U("\r\n"))

# NBSP: words=13 and 12 already done; add quote=... NBSP replacing ALL internal spaces (join with NBSP)
nbsp_q = A203.split('quote="')[1].split('"')[0].replace(' ', '\u00a0')
w("X002-nbsp-all", U('pre\n') + U(A203.split('quote="')[0] + 'quote="' + nbsp_q + '"') + U('\n'))

# curly inside: capture contains "(Figure 1)." straightforward; use apostrophe quote from a capture that has straight '
# S206 quote: "The journal should archive all prior versions of the article." -> no apostrophe; instead test curly single inside
# Take A205 and replace "'" there is none; craft: quote with U+2019 folding: capture has no ' ; test: replace "direct citation" with curly-apostrophe variant
w("X003-curly-inside", U("pre\n") + U(A203.replace("direct citation", "direct\u2019sitation")) + U("\n"))

# unicode line separator / paragraph separator inside quote
w("X004-line-sep", U("pre\n") + U(A203.replace("Backward and forward", "Backward\u2028and forward")) + U("\n"))
w("X005-para-sep", U("pre\n") + U(A203.replace("Backward and forward", "Backward\u2029and forward")) + U("\n"))

# BOM before GATE-RECORD (Cf class in lead_strip)
w("X006-bom", b"pre\n" + b"\xef\xbb\xbf" + U(A203) + b"\n")
# ZWSP before record
w("X007-zwsp-lead", U("pre\n") + b"\xe2\x80\x8b" + U(A203.replace("known", "Zyzzyva")) + b"\n")

# quote spanning line break in capture -> put actual newline inside quote (file line splits)
w("X008-quote-break", U("pre\n") + U(A203.replace("searching are known", "searching are\nknown")) + U("\n"))

# words with tab separator inside quote but words field 13
w("X009-tab-all", U("pre\n") + U(A203.replace(" ", "\t", 3)) + U("\n"))

# capture path with extra slash / dot segments
w("X010-capture-dotseg", U("pre\n") + U(A203.replace("corpus/captures/f2489455cc311a4de981e926.txt", "corpus/captures/./f2489455cc311a4de981e926.txt")) + U("\n"))
w("X011-capture-double-slash", U("pre\n") + U(A203.replace("corpus/captures/", "corpus//captures/")) + U("\n"))
w("X012-capture-uppercase", U("pre\n") + U(A203.replace("f2489455cc311a4de981e926", "F2489455CC311A4DE981E926")) + U("\n"))

# duplicate rev key (parse: first wins, second in head -> dup detected PARSE)
w("X013-dup-rev-key", U("pre\n") + U(R199.replace(" rev=", " rev=" + R199.split("rev=")[1].split()[0] + " rev=")) + U("\n"))

# unknown extra key (PARSE: keys != sets; added kv key extra=1 -> PARSE)
w("X014-extra-key", U("pre\n") + U(A203.replace(" words=", " extra=1 words=")) + U("\n"))

# wrong-case keys (Tier= instead of tier= -> PARSE)
w("X015-case-key", U("pre\n") + U(A203.replace("tier=", "Tier=")) + U("\n"))

# S-id too short / wrong shape
w("X016-sid-short", U("pre\n") + U(A203.replace("S203", "S20")) + U("\n"))
w("X017-sid-4digit", U("pre\n") + U(A203.replace("S203", "S0203")) + U("\n"))

# fetched with offset / fractional
w("X018-fetched-offset", U("pre\n") + U(A203.replace("fetched=2026-11-06T18:44:29Z", "fetched=2026-11-06T18:44:29+00:00")) + U("\n"))

# curl_rc leading zero / http with leading zero
w("X019-curlrc-leadingzero", U("pre\n") + U('GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=reject capture=none curl_rc=022 http=403 words=0 quote=none') + U("\n"))

# tier B lowercase on rev (no tier key in rev form)
# rev quote case-mutated (case exactness in matching)
w("X020-rev-case", U("pre\n") + U(R199.replace("The battery", "the battery").replace("the battery is", "The battery is", 1).replace("the battery", "The battery")) + U("\n"))

# admit quote of next line only: point at S205 but quote first word uppercase diff
w("X021-quote-case", U("pre\n") + U(A205.replace('"the erratum', '"The erratum')) + U("\n"))

# S202 off-by-one and txt-sha of atk file
w("X022-r202-badline", U("pre\n") + U('GATE-RECORD S202 rev=3eb4a3cad8febf75698a017cb6c4441f763b3454 path=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt line=10 words=2 quote=SELFCHECK=PASS unresolved=0/3') + U("\n"))

for fid, p in sorted(probes.items()):
    r = subprocess.run([sys.executable, "-B", os.path.join(T, "tools/gate-records.py"), "verify", "--root", T, "--repo", REPO, p], capture_output=True, text=True)
    print(f"### {fid} rc={r.returncode}")
    print(r.stdout.strip())
    if r.stderr.strip():
        print("STDERR:", r.stderr.strip())
