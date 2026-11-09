# Task Q3 second half: r29/r34 `git -C /dev/null` cannot touch any repository on any host (what if /dev/null were replaced?)
# git -C /dev/null: -C chdirs into /dev/null. If /dev/null is the device, chdir fails (ENOTDIR) -> git exits 128, no repo touched. Confirmed: selftest showed rc=128 for rev-parse.
# Attack surface: if an attacker REPLACED /dev/null with a directory (possible for root? On most systems /dev is devtmpfs; creating a dir at /dev/null requires removing the device node). Then git -C /dev/null would enter that directory. If it were inside a git repo, git rev-parse --show-toplevel would print the toplevel, rc=0 -> r34 FAILs (rc in (0,None) check) rather than touching anything. blob cat-file with rev would fail unless objects exist. git operations are read-only (rev-parse, cat-file blob). No writes. So even worst case: r34 fails (false negative) but no repo mutation. Also git -C <dir> where dir is a file fails ENOTDIR.
# Verify each r29/r34 command's git subcommands are read-only: rev-parse (read-only), cat-file blob (read-only). files_at_rev uses ls-tree (read-only) but r28 pre-fills cache so ls-tree never runs; r29 uses blob() with empty blobs dict -> cat-file blob. r34 uses git(...rev-parse). All read-only.
# What about `git -C /dev/null` searching parent dirs? No: -C changes dir; git then discovers repo from the CURRENT DIR (i.e., /dev/null as dir after chdir). If /dev/null is a char device, chdir fails before any discovery. If replaced by dir inside a repo, discovery finds that repo but only reads.
# Also check: does git write .git/index.lock or similar on rev-parse/cat-file? No, read-only commands don't lock.
# Test the replaced-/dev/null scenario safely in scratch (fake device dir inside a fixture repo).
import subprocess, os, tempfile
D = subprocess.run(["mktemp","-d","-p","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack"],capture_output=True,text=True).stdout.strip()
print("fixture", D)
open(os.path.join(D,"f.txt"),"w").write("hello\n")
subprocess.run(["git","-C",D,"init","-q"])
subprocess.run(["git","-C",D,"-c","user.name=fixture","-c","user.email=fixture@invalid","add","f.txt"])
subprocess.run(["git","-C",D,"-c","user.name=fixture","-c","user.email=fixture@invalid","commit","-qm","x"])
fake = os.path.join(D,"fake-devnull-dir"); os.mkdir(fake)
# git -C fake rev-parse
p = subprocess.run(["git","-C",fake,"rev-parse"],capture_output=True,text=True)
print("git -C fake-dir rev-parse rc", p.returncode, "out", p.stdout[:60])
# git -C /dev/null (real device)
p2 = subprocess.run(["git","-C","/dev/null","rev-parse"],capture_output=True,text=True)
print("git -C /dev/null rc", p2.returncode, "out", repr(p2.stdout[:60]), "err", repr(p2.stderr[:80]))
p3 = subprocess.run(["git","-C","/dev/null","cat-file","blob","0"*40],capture_output=True,text=True)
print("git -C /dev/null cat-file rc", p3.returncode)
import shutil; shutil.rmtree(D)
