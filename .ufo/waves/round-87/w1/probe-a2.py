"""
Probe (a) strongest form: committed-bytes construction where _qual and count disagree
within the instrument's own vocabulary, and D1/D2 builders emit an unservable record.
Key insight: tool's parse requires http=[0-9]{3} (line 151). So a _qual row with http=0203
produces a D2 record with http=0203 which the tool rejects as PARSE (not REFETCH).
The D2 expected code is REFETCH -> WRONG_CODE -> CODES leg fails, but width leg also fails
because count != qual. So disagreeing predicates ARE caught at landing... but what if
both sides are patched together (E1)? Then both return 1 and width passes with class=1.
That is a predicate-consistency failure: the instrument cannot tell whether "qualifying"
means what the claim says.
Alternative committed-bytes case that does NOT require patching both sides:
duplicate (sid,url) rows are already in the committed file? Check: S021/S032 are distinct sid,
so no. But what about a row set where two refetch rows share (sid,url) with different fetched?
_real corpus: does any (sid,url) repeat with rc=0/http!=200 and txt sha? Let's brute-force:
count vs qual sets on committed bytes already agree (3==3). So on committed bytes there is NO
live disagreement. The finding is therefore about the *definition* being ambiguous,
not a live miscount.

But there IS one more subtle difference: count dedups (sid,url) while _qual does not.
If a future refetch.tsv adds attempt=2 for same (sid,url,http=203), _qual yields 2 forges
for one counted row -> D1_WIDTH fails spuriously (false negative). Conversely len-check
difference (len!=3) is unreachable for tool-parseable http (tool requires 3 digits for
unreach, and admit ignores http), but reachable for refetch.tsv rows with 4+ digit http
values in the committed file - the instrument's _qual would then build a record the tool
cannot parse.
Both are definition gaps in "qualifying".
"""
print("(a) definition divergences enumerated; live divergence on landing bytes: none (3==3).")
print(" Divergences:")
print("  D-A: count dedups (sid,url); _qual does not dedup. Integer width can disagree if a")
print("       (sid,url) repeats among qualifying rows (e.g. same sid+url at two fetched times).")
print("  D-B: count requires len(http)==3; _qual accepts any digit-string != 200 (e.g. 0203, 20).")
print("       A 4-digit http row enters _qual (D2 http=0203) but is dropped by count.")
print("  D-C: _qual stores the row's http verbatim into the D2 line; a 3-digit non-2xx non-203")
print("       http (e.g. 404 with rc=0+txt sha) would also qualify! Check: _qual filter is")
print("       curl_rc=0 AND http !=200 AND txt sha matches AND quotable. There is no 203-only")
print("       or non-2xx-exclusion filter. So catch: any committed rc=0 txt-matched row with")
print("       http in {201,202,204...} or {404,...} with a valid capture would join the class.")
print("       On landing bytes only 203 rows qualify - but the predicate SAYS 203, code says non-200.")
