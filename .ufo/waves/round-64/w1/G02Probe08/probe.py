from pathlib import Path
import shutil, subprocess, sys
lane=Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch=Path('/fast/scratch/hyaku/chousa-r64/G02Probe08')
root=scratch/'fixture'
shutil.rmtree(root, ignore_errors=True)
(root/'corpus/knowledge/real').mkdir(parents=True)
(root/'corpus/knowledge/real/valid.md').write_text('valid fixture\n', encoding='utf-8')
(root/'corpus/README.md').write_text('A valid pointer: valid.md. Phantom knowledge path: `knowledge/real/missing.md`.\n', encoding='utf-8')
cmd=[sys.executable,'-B',str(lane/'corpus/evidence/round64/controls/ref-preflight-v3.py'),'--root',str(root),'--only','G02','--work',str(scratch/'work')]
p=subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(scratch/'stdout.txt').write_text(p.stdout, encoding='utf-8')
(scratch/'stderr.txt').write_text(p.stderr, encoding='utf-8')
print('COMMAND='+' '.join(cmd))
print('EXIT='+str(p.returncode))
print('STDOUT_BEGIN'); print(p.stdout, end=''); print('STDOUT_END')
print('STDERR_BEGIN'); print(p.stderr, end=''); print('STDERR_END')
