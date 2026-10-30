from pathlib import Path
import shutil, subprocess, sys
lane=Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
scratch=Path('/fast/scratch/hyaku/chousa-r64/G02Probe06')
candidate=lane/'corpus/evidence/round64/controls/ref-preflight-v3.py'
work=scratch/'work'; work.mkdir(exist_ok=True)
def run(case, add_gitkeep, add_nonmd):
    base=scratch/case
    if base.exists(): shutil.rmtree(base)
    (base/'corpus/knowledge/sub').mkdir(parents=True)
    (base/'corpus/README.md').write_text('knowledge/good.md\n', encoding='utf-8')
    (base/'corpus/knowledge/good.md').write_text('ok\n', encoding='utf-8')
    if add_gitkeep: (base/'corpus/knowledge/sub/.gitkeep').write_text('', encoding='utf-8')
    if add_nonmd: (base/'corpus/knowledge/sub/notes.txt').write_text('unexpected\n', encoding='utf-8')
    cmd=[sys.executable,str(candidate),'--root',str(base),'--only','G02','--work',str(work)]
    p=subprocess.run(cmd, text=True, capture_output=True)
    print('CASE',case,'COMMAND',cmd,'EXIT',p.returncode,'STDOUT',repr(p.stdout),'STDERR',repr(p.stderr))
    (scratch/f'{case}.stdout').write_text(p.stdout,encoding='utf-8')
    (scratch/f'{case}.stderr').write_text(p.stderr,encoding='utf-8')
    (scratch/f'{case}.exit').write_text(str(p.returncode)+'\n',encoding='ascii')
run('nested-gitkeep', True, False)
run('nested-nonmarkdown', False, True)
