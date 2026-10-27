#!/usr/bin/env python3
"""Extract the pinned round-55 baseline and make a refuse-all control."""
from pathlib import Path
import subprocess
root=Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
out=Path(__file__).resolve().parent
blob=subprocess.run(['git','-C',str(root),'show','b13ca7b5c8bbb40d2d29a37fb443c64ca043f791:tools/build-spans.py'],capture_output=True,check=True).stdout
(out/'build-spans-r55.py').write_bytes(blob)
(out/'REFUSEALL.py').write_text('''#!/usr/bin/env python3\nimport sys\nprint("build-spans: refused REFUSEALL control", file=sys.stderr)\nsys.exit(1)\n''',encoding='utf-8')
(out/'build-spans-r55.py').chmod(0o755)
(out/'REFUSEALL.py').chmod(0o755)
print('BASELINE_SHA256_PINNED_BYTES='+__import__('hashlib').sha256(blob).hexdigest())
print('CONTROLS=build-spans-r55.py,REFUSEALL.py')
