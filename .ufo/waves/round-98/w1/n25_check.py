# n25-gitenv-no-lazy: GOLD check — battery docstring/body says r25? No. The prior n25 mutant is ("GIT_NO_LAZY_FETCH" removal). At F it is killed via m08-env-scrub,r13-env-guards. Verified in battery output.
# Also verify the before/ receipt's sha matches F battery: compute sha256 of F battery file.
import hashlib, subprocess
b = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/corpus/evidence/round98/selftest-controls-r98.py","rb").read()
print("F battery sha256", hashlib.sha256(b).hexdigest())
print("receipt claims 942b70692069c7b42108f1274c78f37acbe063fbf48b27ad7fd0166443b03179")
