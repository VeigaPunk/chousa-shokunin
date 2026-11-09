# r28 attack: does run_at_rev on pre-filled cache REALLY run no git, or could a mutant smuggle a git call the case wouldn't see?
# run_at_rev calls files_at_rev (cache hit -> return immediately) then blob() per path (all o1/o2/o3 pre-cached -> no subprocess). static_dir is pure. matches/hit pure.
# But: cache.setdefault("blobs", {}) in run_at_rev line 309 — cache already has "blobs". blob() checks obj in blobs first. So zero.
# What if cache[tops] filtering... no subprocess anywhere else in path. Confirmed by subprocess.run spy (0 calls) + strace (exactly 2 git execs: r29 cat-file, r34 rev-parse).
# Now the deeper question for the claim: the claim says selftest "runs no git" was UPDATED to "reads /dev/null and runs git -C /dev/null twice (r29, r34), which cannot open a repository". Verified: exactly 2 git processes, both with -C /dev/null, both read-only subcommands. r28 adds none.
# r30 reads /dev/null via parse_record (open read) — file read, not git.
# Audit-hook proof (alternative, stronger): run selftest under audit hook raising on any subprocess with non-/dev/null repo.
import sys
events = []
def hook(event, args):
    if event in ("subprocess.Popen",):
        cmd = args[0]
        events.append(cmd)
sys.addaudithook(hook)
import importlib.util
spec = importlib.util.spec_from_file_location("sr2", "/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py")
sr2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr2)
rc = sr2.selftest()
print("selftest rc", rc)
print("Popen cmds:", events)
