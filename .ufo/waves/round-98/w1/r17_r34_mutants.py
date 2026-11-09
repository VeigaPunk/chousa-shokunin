# Q1 deeper: each r17-r34 must assert what the real tool does. Battery already showed each kills its target mutant.
# But check OVERFIT/UNDERFIT: does r25's digest == ST_NONUTF8_DIGEST actually discriminate str-sort vs byte-sort?
# ST_NONUTF8_DIGEST is claimed sha256 of b"corpus/\xa8.txt\ncorpus/\xc7\x8e.txt\n". Verify directly with hashlib.
import hashlib
want = hashlib.sha256(b"corpus/\xa8.txt\ncorpus/\xc7\x8e.txt\n").hexdigest()
print("r25 digest check:", want, "matches tool const 4d7e31...?", want == "4d7e31c7d2d9d078296d0cab96465d9c4f19dc5e7e023b2d10840c3e020cc87b")
# str-ordered digest would be sha256 of b"corpus/\xc7\x8e.txt\ncorpus/\xa8.txt\n"
other = hashlib.sha256(b"corpus/\xc7\x8e.txt\ncorpus/\xa8.txt\n").hexdigest()
print("str-order digest:", other, "differs:", other != want)
# Check the escape claim: "corpus/\udca8.txt" encoded surrogateescape == b"corpus/\xa8.txt"?
print("surrogateescape bytes:", "corpus/\udca8.txt".encode("utf-8","surrogateescape"), "corpus/\u01ce.txt utf8:", "corpus/\u01ce.txt".encode("utf-8","surrogateescape"))
print("str order: \\u01ce < \\udca8 ?", "corpus/\u01ce.txt" < "corpus/\udca8.txt", "| byte order 0xa8 < 0xc7 :", b"corpus/\xa8.txt" < b"corpus/\xc7\x8e.txt")
# r28: does it test two-static-dirs filtering (u02 tops[0] vs tops)? Battery: u02 killed failed=r28. Verify mechanism: with tops[0] only, paths under b/ filtered out -> got==['a/x.txt'] != expected. Yes.
# r29: blob silent mutant (if False) -> got=b'' returned, case returns (False, ...) -> FAIL. Battery confirms.
# r30: exists-refused mutant (u07): parse_record(os.devnull): islink=False, mutant does exists check: os.path.exists('/dev/null') is True -> raises RECORD_TYPE -> code != SECTION -> FAIL. But ALSO: mutant's exists check would raise for ANY existing file, breaking p01? Battery shows failed=r30 only. Consistent.
# r32: rev-swap mutant (e01 probe): tokens would be [DRIFT, MATCH]. Killed.
# r33: e02 count-lt: hits=1, at_rev=2: lt gives no COUNT_DRIFT; set: at_rev=[a,c] vs set=[a] -> SET_DRIFT only. Want is (2,0,1,[COUNT_DRIFT,SET_DRIFT]) -> fails. Killed.
# r34: u06 timeout=0: subprocess with timeout=0 raises TimeoutExpired immediately? Battery: got killed failed=r34. On this host timeout=0 -> immediate timeout. Matches.
# r26: v01 GIT_ prefix -> startswith("GIT") drops GITFOO. Killed via r26 (env_foo.get GITFOO missing). Note: v01 also breaks r13? Battery shows failed=r26 only for v01... wait r13 checks sorted GIT_ keys == 3; with v01, GIT_NO_... still set (update adds them), and GITFOO kept -> r13 checks keys startswith GIT_ only, GITFOO doesn't match GIT_ -> r13 still passes. And m08? m08 checks GIT_DIR not in env -> passes. So r26 is the sole killer. Good.
# r27: u04 bracket: static_dir("a[b]/c.txt"): mutant ignores [ -> returns "a[b]" != "" -> FAIL. Second conjunct static_dir("a/[x]/c.txt")=="a" holds in both. OK.
# r25 also kills m25? Battery r96 m25 failed=m06-digest,r25. m06 uses clean ASCII paths where sort order same; m25 unsorted preserves input order [b,a] -> digest differs. r25 input [01ce, dca8]: unsorted preserves that order = str order = WRONG order too. So r25 catches m25 as well. Fine (redundant coverage, not a defect).
# r31: m03 startswith: "a PRESS" startswith "PRESS"? No -> hit False -> case fails (expects True). Battery confirms failed=r31 only.
# r17-r24 refusal cases: each refusal() asserts code equality via refused(). g06 (return detail not code) would make ALL refusals fail with detail strings. Battery g06 failed list includes all 28 refusal cases. Confirmed.
# One more: r36? No r36. CASE_IDS order is checked by battery POSITIVE (exact order). Selftest prints g00 first, then _collect order: p01,p02,...j10,r17..r34. CASE_IDS in battery lists g00 first, then p..j, then r17..r34. Battery POSITIVE verified equal order. Good.
