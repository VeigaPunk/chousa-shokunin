#!/usr/bin/env python3
"""R65-C2 structural sourced-entry counter; does not establish entailment."""
from pathlib import Path
import sys
L=Path(__file__).resolve().parents[3]
f=L/'corpus/knowledge/receipt-identity-r65.md'; text=f.read_text() if f.exists() else ''
s=(L/'corpus/SOURCES.md').read_text();idx=(L/'corpus/README.md').read_text()
checks=[text.startswith('source:'), '\nverified-at:' in text, '\nrecheck:' in text, all(x in text for x in ['S154','S155','S156']), all(('| '+x+' |') in s for x in ['S154','S155','S156']), 'receipt-identity-r65.md' in idx, '## Claims' in text, '## Limits' in text, 'authenticity' in text, 'working tree' in text]
n=sum(checks); print(f'ENTRY_CHECKS={n}/10 C2={"PASS" if n==10 else "FAIL"}');sys.exit(0 if n==10 else 1)
