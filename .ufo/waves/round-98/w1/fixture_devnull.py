import subprocess, os
D = "/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/fx-devnull"
import shutil
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
open(os.path.join(D,"f.txt"),"w").write("hello\n")
subprocess.run(["git","-C",D,"init","-q"])
subprocess.run(["git","-C",D,"-c","user.name=fixture","-c","user.email=fixture@invalid","add","f.txt"])
subprocess.run(["git","-C",D,"-c","user.name=fixture","-c","user.email=fixture@invalid","commit","-qm","x"])
top = subprocess.run(["git","-C",D,"rev-parse","--show-toplevel"],capture_output=True,text=True)
print("toplevel", top.returncode, repr(top.stdout))
fake = os.path.join(D,"fake-null"); os.mkdir(fake)
p = subprocess.run(["git","-C",fake,"rev-parse"],capture_output=True,text=True)
print("fake-dir rev-parse rc", p.returncode, repr(p.stdout), repr(p.stderr[:80]))
p2 = subprocess.run(["git","-C",fake,"rev-parse","--show-toplevel"],capture_output=True,text=True)
print("fake-dir toplevel", p2.returncode, repr(p2.stdout[:80]))
p3 = subprocess.run(["git","-C",fake,"cat-file","blob","0"*40],capture_output=True,text=True)
print("fake-dir cat-file rc", p3.returncode, repr(p3.stderr[:100]))
shutil.rmtree(D)
