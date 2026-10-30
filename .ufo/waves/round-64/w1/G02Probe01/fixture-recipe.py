import importlib.util
import pathlib
import tempfile

CANDIDATE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py')
spec = importlib.util.spec_from_file_location('candidate', CANDIDATE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cases = [
    ('whole-token bare', 'alpha'),
    ('left word boundary rejected', 'xalpha'),
    ('left dot boundary rejected', 'x.alpha'),
    ('left hyphen boundary rejected', 'x-alpha'),
    ('right word boundary rejected', 'alphaX'),
    ('right hyphen boundary rejected', 'alpha-x'),
    ('right dot boundary allowed', 'alpha.md.'),
    ('prefixed whole token', 'knowledge/alpha.md'),
]
for label, token in cases:
    with tempfile.TemporaryDirectory(prefix='g02-boundary-') as td:
        root = pathlib.Path(td)
        kd = root / 'corpus' / 'knowledge'
        kd.mkdir(parents=True)
        (kd / 'alpha.md').write_text('fixture\n', encoding='utf-8')
        (root / 'corpus' / 'README.md').write_text(token + '\n', encoding='utf-8')
        work = root / 'work'
        work.mkdir()
        status, detail = mod.g02(root, object(), {}, work)
        print(f'{label}: {status} | {detail}')
