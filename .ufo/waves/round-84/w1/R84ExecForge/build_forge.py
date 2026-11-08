#!/usr/bin/env python3
"""Build K2 spec-generalization forgeries for R84ExecForge (scratch only)."""
import os, shutil, subprocess, sys

T = "/fast/scratch/hyaku/chousa-r84/R84ExecForge/tree"
S = "/fast/scratch/hyaku/chousa-r84/R84ExecForge"
FORGE = os.path.join(S, "tree", "forge")
os.makedirs(FORGE, exist_ok=True)
for f in os.listdir(FORGE):
    os.remove(os.path.join(FORGE, f))

def q(s):  # quote file content helper
    return s

# ---- bases (byte-exact from c2-positives.tsv / round-84 records) ----
A203 = 'GATE-RECORD S203 url=https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf fetched=2026-11-06T18:44:29Z tier=A decision=admit capture=corpus/captures/f2489455cc311a4de981e926.txt capture_sha256=31493aa66bfd6625\u2026 words=13 quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."'
A205 = 'GATE-RECORD S205 url=https://www.nlm.nih.gov/bsd/policy/errata.html fetched=2026-11-06T18:44:30Z tier=A decision=admit capture=corpus/captures/371c55117727d526805f030d.txt capture_sha256=08b4b3c0ad9215b0\u2026 words=13 quote="the erratum notice is simply linked to the citation for the corrected article."'
R199 = 'GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 words=12 quote=the battery is fully forgeable through the payload channel on **both** batteries'
R200 = 'GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1056 words=20 quote=A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement'
U208 = 'GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none'
R202 = 'GATE-RECORD S202 rev=3eb4a3cad8febf75698a017cb6c4441f763b3454 path=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt line=11 words=2 quote=SELFCHECK=PASS unresolved=0/3'
# from lesson round-84 (lines 18-20 of round-84.md)
L214 = 'GATE-RECORD S214 url=https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf fetched=2026-11-08T02:21:13Z tier=A decision=admit capture=corpus/captures/a640b15abf781e5c583d7088.txt capture_sha256=4cbf8881578dbc7b\u2026 words=17 quote="Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies."'
L018 = 'GATE-RECORD S018 url=https://aclanthology.org/2026.acl-long.1430/ fetched=2026-11-08T02:15:05Z tier=B decision=admit capture=corpus/captures/248b43277f376e437a356909.txt capture_sha256=0640edfc82212389\u2026 words=13 quote="aiming to link model outputs to supporting evidence to ensure traceability and verifiability"'
L023 = 'GATE-RECORD S023 url=https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ fetched=2026-11-08T02:16:27Z tier=A decision=admit capture=corpus/captures/f5545a194c06ab421875b047.txt capture_sha256=20dc0c3ab7724e1f\u2026 words=10 quote="A related resource from which the described resource is derived."'

# reference data
TREE_HASH = "8bff97f27d9806c15a9d821f576782e0e9c04c92"  # tree of b7803829 (from tool run)
RAW_SHA = "eea13440d89c7b273709a7e8e6a3ad009066eb766a89e978486bebf51583debd"  # .raw bytes of f248 capture
RAW16 = RAW_SHA[:16]

F = []  # (id, line_or_bytes, expected_docstring_code_or_OK_or_none, klass_note)

def add(fid, line, exp, note):
    F.append((fid, line, exp, note))

# ---------- F001 sha prefix / suffix ----------
add("F001-upper-sha", A203.replace("capture_sha256=31493aa66bfd6625", "capture_sha256=31493AA66BFD6625"), "CAPTURE_SHA", "SHA_RE lowercase [0-9a-f] only; docstring CAPTURE_SHA check")
add("F002-dots-suffix", A203.replace("\u2026", "..."), "OK-ACCEPTED?", "docstring SHA_RE allows (?:\u2026|\\.\\.\\.)? \u2014 both suffixes legitimate \u2192 not a forgery unless refused (K3 harm candidate)")
add("F003-no-suffix", A203.replace("31493aa66bfd6625\u2026", "31493aa66bfd6625"), "OK-ACCEPTED?", "suffix optional in SHA_RE; prefix >=16 \u2192 meets every check \u2192 not a forgery; accepted = fine, refused = K3")
add("F004-raw-sha", A203.replace("capture_sha256=31493aa66bfd6625", f"capture_sha256={RAW16}"), "CAPTURE_SHA", "txt_sha256 != raw bytes; CAPTURE_SHA not prefix of sha256(txt bytes); also crypto drift class")
add("F005-sha17-overhang", A203.replace("capture_sha256=31493aa66bfd6625\u2026", "capture_sha256=31493aa66bfd66259\u2026"), "CAPTURE_SHA", "17-hex prefix crossing the prefix boundary: 31493aa66bfd6625|9 \u2014 wait, full cap sha = 31493aa66bfd66259cc9\u2026 so 17 chars IS a valid prefix \u2192 meets checks \u2192 harm candidate if refused, else not forgery. Hold on: full sha 31493aa66bfd66259cc9 - 17-hex IS prefix \u2192 OK. Verdict: not forgery.")

# ---------- F006-F008 refetch mismatch ----------
add("F006-sameurl-diffid", A203.replace("GATE-RECORD S203", "GATE-RECORD S204"), "REFETCH", "claim up to S204 but url+key+fetched of S203: no refetch row for (S204, S203url...) \u2192 REFETCH; also tests id binding")
add("F007-s208-failed-row", U208.replace("fetched=2026-11-06T18:44:31Z", "fetched=2026-11-06T18:44:32Z"), "REFETCH", "unreach row with fetched +1s: no row with that time \u2192 REFETCH")
add("F008-fetched-diffsec", A203.replace("fetched=2026-11-06T18:44:29Z", "fetched=2026-11-06T18:44:30Z"), "REFETCH", "admit fetched second drifted (still a real fetched of some row of another id, but not this id+key) \u2192 REFETCH")

# ---------- url mutations ----------
add("F009-trailing-slash", A205.replace("url=https://www.nlm.nih.gov/bsd/policy/errata.html", "url=https://www.nlm.nih.gov/bsd/policy/errata.html/"), "CAPTURE_KEY", "trailing slash changes sha256(url)[:24] key \u2260 capture key \u2192 CAPTURE_KEY (docstring); REFETCH also fires")
add("F010-fragment", A205.replace("errata.html ", "errata.html#x "), "CAPTURE_KEY", "fragment changes key \u2192 CAPTURE_KEY")
add("F011-http-scheme", A205.replace("url=https://www.nlm.nih.gov", "url=http://www.nlm.nih.gov"), "CAPTURE_KEY", "http vs https changes key \u2192 CAPTURE_KEY; PARSE passes (https? allowed)")
add("F012-case-scheme", A205.replace("url=https://www.nlm.nih.gov", "url=https://WWW.nlm.nih.gov"), "CAPTURE_KEY", "host case changes key \u2192 CAPTURE_KEY")

# ---------- tier / decision ----------
add("F013-tier-lower-a", A203.replace("tier=A", "tier=a"), "PARSE", "tier must be A|B|C uppercase; PARSE (parse() checks kv[tier] in (A,B,C))")
add("F014-decision-case", A203.replace("decision=admit", "decision=Admit"), "PARSE", "decision must be admit|reject lowercase; PARSE")
add("F015-decision-other", A203.replace("decision=admit", "decision=accept"), "PARSE", "decision=accept not in {admit,reject}; PARSE")

# ---------- numerals (beyond 9 survivors; new classes) ----------
add("F016-words-plus", A203.replace("words=13", "words=+13"), "PARSE", "plus sign: INT_RE 0|[1-9][0-9]{0,6} rejects +13; PARSE")
add("F017-words-unicode-fullwidth", A203.replace("words=13", "words=\uff11\uff13"), "PARSE", "fullwidth digits: unicode digit class pre-repair bug class; INT_RE ASCII-only \u2192 PARSE")
add("F018-line-unicode-devanagari", R199.replace("line=222", "line=\u0968\u0968\u0968"), "PARSE", "Devanagari digits: INT_RE rejects \u2192 PARSE (rev line)")
add("F019-curlrc-superscript", U208.replace("curl_rc=22", "curl_rc=\xb2\xb2"), "PARSE", "superscript two: not ASCII \u2192 PARSE")
add("F020-http-superscript", U208.replace("http=403", "http=\uff14\uff10\uff13"), "PARSE", "fullwidth http \u2192 PARSE")

# ---------- quotes (chars/spans/cross-capture) ----------
add("F021-nbsp-words", A203.replace("words=13", "words=12"), "WORDS", "NBSP inside quote: norm() splits on any whitespace incl NBSP (str.split) \u2192 13 vs 12 \u2192 WORDS. OBS check: actual counts may differ; report raw. Base quote uses regular spaces; inject NBSP between 'Backward' and 'and'. Expected WORDS if counter differs, else QUOTE_ABSENT\u2192 wait NBSP normalizes same \u2192 if words=13 then OK (meets every check, not a forgery). Put words=12 to force WORDS; but if split counts differently report actual.")
# (F021 crafted below in file section since needs NBSP bytes)

add("F022-zwsp-quote", A203.replace('"Backward', '"Backward\u200b'), "QUOTE_ABSENT", "zero-width space Cf inside quote: norm() leaves it in token; not present in capture \u2192 QUOTE_ABSENT (capture text has no ZWSP)")
add("F023-curly-quotes", A203.replace('quote="Backward', "quote=\u2018Backward").replace('searching (Figure 1)."', "searching (Figure 1).\u2019"), "QUOTE_ABSENT", "curly quote delimiters: parse requires straight double-quote delimiters -> PARSE.")
add("F024-html-entity", A203.replace("searching (Figure 1).", "searching (Figure 1)&#46;"), "QUOTE_ABSENT", "&#46; for '.' : norm() does NOT decode entities (docstring: only U+2018..U+201D + ws) \u2192 quote text \u2260 capture \u2192 QUOTE_ABSENT")
add("F025-multiline-quote", A203.replace('quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."', 'quote="Backward and forward citation searching are known as direct citation searching (Figure 1). They\ncan be" \nwords=15'), "WORDS/PARSE", "quote spanning a line break in the capture: rev form quote to EOL; admit quote is one line \u2014 breaking onto next file line splits record \u2192 second file line has no GATE-RECORD \u2192 PARSE-ish. This tests detection: the truncated first physical line parses as admit with quote 'Backward..They' closed mid-line \u2192 actually still on one line until \\n. Rebuild: see forge file writing (special multi-line file).")

add("F026-cross-capture", A205.replace('quote="the erratum notice is simply linked to the citation for the corrected article."', 'quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."'), "QUOTE_ABSENT", "quote located only in S203's capture, not S205's capture \u2192 QUOTE_ABSENT (already M08-ish but cross-capture is the point: words=13 matches either capture's quote)")

# ---------- rev forms ----------
add("F027-short-rev", R199.replace("rev=b7803829922770b890e9f4efdd30d12c3695439a", "rev=b7803829"), "PARSE-or-REV", "short rev (10 hex): docstring rev=<40 hex>; parse() does NOT check rev format (git_blob only) \u2192 check() HEX40_RE fails \u2192 REV(+LINE). So expected REV not PARSE. Report actual codes.")
add("F028-tag-rev", R199.replace("rev=b7803829922770b890e9f4efdd30d12c3695439a", "rev=v1.0"), "REV", "tag name: HEX40_RE fails \u2192 REV")
add("F029-HEAD-rev", R199.replace("rev=b7803829922770b890e9f4efdd30d12c3695439a", "rev=HEAD"), "REV", "HEAD: HEX40_RE fails \u2192 REV")
add("F030-tree-hash", R199.replace("rev=b7803829922770b890e9f4efdd30d12c3695439a", f"rev={TREE_HASH}"), "REV", "tree hash: git cat-file -t rev^{commit} != commit \u2192 git_blob None \u2192 REV")
add("F031-space-path", R199.replace("path=corpus/lessons/round-79-verifier-spotcheck.md", "path=corpus/lessons/round 79.md"), "PARSE+REV?", "space in path: kv head split on space \u2192 token '79.md' has no '=' \u2192 parse() None \u2192 PARSE")
add("F032-nonascii-path", R199.replace("path=corpus/lessons/round-79-verifier-spotcheck.md", "path=corpus/lessons/round-79-verifier-spotcheck.\xe0d"), "REV", "non-ASCII path: parses, blob absent \u2192 REV")
add("F033-line-offbyone", R199.replace("line=222", "line=223"), "LINE", "line+1: normalized quote not in that one line (LINE docstring: quote must occur in that one line) \u2192 LINE")
add("F034-line-offbyone-minus", R199.replace("line=222", "line=221"), "LINE", "line-1 similarly \u2192 LINE")

# ---------- admit/unreach decision edges ----------
add("F035-admit-capnone", A203.replace("capture=corpus/captures/f2489455cc311a4de981e926.txt", "capture=none"), "CAPTURE_PATH", "admit form with capture=none: CAP_RE fails \u2192 CAPTURE_PATH (also CAPTURE_KEY? cm None so key check skipped; CAPTURE_SHA cap None \u2192 also CAPTURE_SHA, QUOTE_ABSENT, REFETCH)")
add("F036-unreach-claims-ok", U208.replace("curl_rc=22", "curl_rc=0").replace("http=403", "http=200"), "REFETCH", "unreach claiming success (curl_rc 0 http 2xx): docstring REFETCH \u2014 record's curl_rc/http denote a success \u2192 REFETCH (M24 class, distinct ids)")
add("F037-unreach-with-sha", U208.replace("capture=none", "capture_sha256=31493aa66bfd6625"), "PARSE", "unreach key set changed (adds capture_sha256, drops nothing? keys become {url,fetched,tier,decision,capture_sha256,curl_rc,http,words} != URL_UNREACH and != REV/ADMIT \u2192 parse None \u2192 PARSE")
add("F038-admit-words0", A203.replace("words=13", "words=0"), "WORDS", "words=0 parses (INT_RE allows 0) \u2192 WORDS (0 != 13) + QUOTE_LEN maybe not (len 13 in range). Expected WORDS.")

# ---------- detection edges ----------
add("F039-leading-ws-badquote", "  " + A203.replace("searching are known", "searching are Zyzzyva"), "QUOTE_ABSENT", "indented + bad quote: lead_strip detects record \u2192 QUOTE_ABSENT (M14 class with 2-space indent; 3-space indent also within ROW_RE? detection is not ROW_RE \u2014 lead strips all ws)")
add("F040-tab-indent", "\t" + R199.replace("fully forgeable", "fully Zyzzyva"), "LINE", "tab-indented: lead_strip drops tab \u2192 detected \u2192 LINE (quote absent on that blob line)")
add("F041-4space-indent", "    " + A203.replace("searching are known", "searching are Zyzzyva"), "QUOTE_ABSENT?", "4-space indent: docstring 'first text, after leading whitespace' strips ALL leading ws \u2192 detected \u2192 QUOTE_ABSENT. If tool skipped it, it'd print no record line (detect-edge finding: record silently skipped, rc 0 if alone? n=0 \u2192 exit 1 no records. Alone: records=0 rc1. Note carefully: if skipped, batch shows records=0. In batch with others present, silently missing = hole.")
add("F042-fenced", '```\n' + A203.replace("searching are known", "searching are Zyzzyva") + "\n```", "QUOTE_ABSENT", "fenced code block: docstring says inline code/list/blockquote are prose \u2014 but fenced block content starts at line start \u2192 detected \u2192 QUOTE_ABSENT. Contract: 'such a line is checked, never skipped' \u2014 fence is not in the prose exclusion list explicitly for fenced? Docstring: '(inline code, list item, blockquote, HTML comment)' \u2014 no fenced mention \u2192 detected.")
add("F043-blockquote", "> " + A203.replace("searching are known", "searching are Zyzzyva"), "NONE-detected?", "blockquote: lead_strip drops ws/Cf only, '>' remains \u2192 REC_RE ^GATE-RECORD fails \u2192 NOT a record, skipped (docstring: blockquote = prose \u2192 none expected). Expect: no GATE_RECORD line for it. If tool lacks batch companion... in batch, count records to confirm skipped.")
add("F044-list-marker", "- " + A203.replace("searching are known", "searching are Zyzzyva"), "NONE-detected?", "list item: '-' remains after lead_strip \u2192 skipped per docstring.")
add("F045-extra-text", A203 + " trailing", "PARSE", "extra text after closing quote: admit qraw does not end with closing quote -> parse None -> PARSE")
add("F046-dup-quote-key", A203.replace('quote="Backward', 'quote="Backward" quote="x'), "QUOTE_ABSENT+", "two quote keys: parse splits at first quote= -> QUOTE_ABSENT + WORDS.")

# ---------- high-value conformance probes (should be accepted \u2014 K3 harm candidates if refused) ----------
add("H1-dotdot-suffix", A203.replace("\u2026", "..."), "OK", "\u2026 vs ... conformance")
add("H2-no-suffix", A203.replace("31493aa66bfd6625\u2026", "31493aa66bfd6625"), "OK", "no-suffix 16-hex conformance")
add("H3-curly-inside-quote", None, "OK?", "quote text with U+2019 where capture has U+2019 or straight ' \u2014 norm folds both ways; build from S206 quote if it has an apostrophe; else skip-check actual")
add("H4-tab-in-quote", None, "OK?", "tab between words inside quote: norm splits on any ws \u2192 matches capture's space \u2192 OK expected")
add("H5-crlf", None, "?", "CRLF line ending: parse rstrip \\r\\n on admit qraw; rev quote='...'.rstrip() \u2014 trailing \\r stripped. Write with \\r\\n.")
add("H6-15vs16-sha", A203.replace("capture_sha256=31493aa66bfd6625\u2026", "capture_sha256=31493aa66bfd662\u2026"), "OK", "15-hex prefix: docstring says >=16 hex digits \u2192 CAPTURE_SHA (shorter than 16). So expected CAPTURE_SHA, not OK. Label as forgery #4-adjacent.")

# ---------- L214/L018/L023-derived ----------
add("F047-l214-rev-words-plus", L214.replace("words=17", "words=018"), "PARSE", "leading-zero words (018): INT_RE rejects \u2192 PARSE (M31 class, fresh id)")
add("F048-l018-tier-flip", L018.replace("tier=B", "tier=A"), "TIER", "tier differs from registry (B) \u2192 TIER")
add("F049-l023-quote-word", L023.replace("resource from which", "resource from Zyzzyva"), "QUOTE_ABSENT", "quote word swapped in L023 \u2192 QUOTE_ABSENT")
add("F050-r202-line-plus", R202.replace("line=11", "line=12"), "LINE", "R202 line 12 empty/missing \u2192 LINE")

# ---------- setup leg (non-git --repo) \u2014 handled in separate run ----------
# fixup special builds
import re
newF = []
for fid, line, exp, note in F:
    if line is None:
        continue
    newF.append((fid, line, exp, note))
F = newF

# NBSP TAB ZWSP H3/H4/H5 specials (bytes)
nbsp = A203.replace("Backward and forward", "Backward\u00a0and forward")
F.append(("F021-nbsp-words12", nbsp.replace("words=13", "words=12"), "WORDS?", "NBSP in quote, words claims 12. norm text also splits NBSP? Python str.split() treats NBSP as whitespace \u2192 quote words stay 13 \u2192 WORDS expected; if split differs report actual."))
F.append(("F021b-nbsp-words13", nbsp, "OK?", "same NBSP quote, words=13: if norm matches capture \u2192 OK (genuine normalization, not forgery); if refused \u2192 K3 harm candidate."))
F.append(("F05xx-tab", A203.replace("Backward and forward", "Backward\tand forward"), "OK?", "tab inside quote \u2192 norm collapse \u2192 quote matches capture \u2192 OK expected. Refused \u2192 K3."))

# write files
receipts = []
for fid, line, exp, note in F:
    p = os.path.join(FORGE, fid + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("preamble prose, not a record\n")
        fh.write(line + "\n")
        fh.write("postamble\n")
    receipts.append((fid, p, exp, note))

print(f"Wrote {len(receipts)} forge files")
for fid, p, exp, note in receipts:
    print(fid, exp)
