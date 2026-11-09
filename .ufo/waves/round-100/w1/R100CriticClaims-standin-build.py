# C1 stand-in 2: oracles miss keying on battery FIXTURE keys (kc/kd) vs lane captures.
# Proposal: refuse iff oid in capture_oids AND is_challenge(ctext) — that's the claim. Need something battery DOESN'T catch.
# Battery keys: k230,k234,k233 lane keys + kc=key("https://fixture.invalid/cpage"), kd=key("https://fixture.invalid/dpage").
# A forger tool that refuses lane keys but admits kc/kd (fixture-only captures) — battery would... r6 (kc.raw), r8 (notes/c-copy = CPAGE bytes, is kc capture at fixture rev? yes kc.txt CPAGE), r11 (kd.txt). All refused by claim. A stand-in refusing only LANE keys (from git log?) would fail r6/r11 -> caught.
# Opposite: tool refuses everything EXCEPT when url contains "fixture.invalid"? rev records have no url. can't key.
# Tool keying on fixture repo: o7 (repo==root) and o8 (repo!=root) BOTH rejected — so repo-keying is covered.
# Remaining gap candidate: rev value in record vs capture set at a DIFFERENT rev: tool builds capture set from HEAD (not record's rev). Battery fixture repo has single commit frev; PROD legs use BASE rev with the lane's --repo default (=lane root). HEAD of lane == F != BASE. capture_oids(repo, HEAD)? If stand-in used HEAD always: PROD rev-* cases (rev=BASE) would look up oids at F. At F, the same .txt paths still hold same blobs (caps committed before base? S230 capture at BASE: earlier host listing shows same blob). So indistinguishable in battery! My probe v1/v2 (rev A vs rev B, same path different content) distinguishes: tool reading HEAD tree (my E) would judge B-record by E's set -> v2 (B non-challenge, E raw-challenge?) k1 at E: E has k1.txt challenge (from trap file? E commit before trap: k1.txt at E = "An ordinary..."? Let me recheck: commits: A k1=CHALLENGE; B k1=NONE; C k2.raw=CH2; D k2.raw=clean; E k2.raw=challenge,k2.txt=clean.)
# At HEAD=E: k1.txt = non-challenge (B version). So HEAD-tree tool: v1 (A, challenge) -> oid(A:k1)=challenge-blob oid; is that oid in E's capture set? E's set includes k1.txt oid = non-challenge oid, k2.* oids. challenge-oid NOT in E set -> admit -> v1 fails differently. So HEAD-tree variant IS distinguishable -- v1 OK (bad), v2 OK (good), v3: notes/blob oid = k2.txt oid at B; at E k2.txt=clean; oid present in E set? k2.txt oid at E is clean-text oid, blob(text=CH2) oid != -> admit -> distinguished too.
# So build that stand-in and check battery result.
import os
LANE="/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo"
src=open(os.path.join(LANE,"tools/gate-records.py")).read()
old="    name = capture_oids(repo, rev).get(p.stdout.strip()) if p.returncode == 0 else None"
new="    name = capture_oids(repo, \"HEAD\").get(p.stdout.strip()) if p.returncode == 0 else None"
assert src.count(old)==1
open("/fast/scratch/hyaku/chousa-r100/R100CriticClaims/standin-head-tree.py","w").write(src.replace(old,new))
print("ok")
