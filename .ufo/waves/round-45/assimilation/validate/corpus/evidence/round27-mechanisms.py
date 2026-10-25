#!/usr/bin/env python3
"""Count the exact reported r26 implementation mechanisms, not behavioral safety.

Usage: python3 corpus/evidence/round27-mechanisms.py GATE
This probe exits0 on successful counting; independent regressions/selftests own verdicts.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

text = Path(sys.argv[1]).read_text()

def function(name):
    match = re.search(r'^' + re.escape(name) + r'\(\).*?^}', text, re.M | re.S)
    if not match:
        raise SystemExit('missing production function: ' + name)
    return match.group(0)

iso = function('metadata_iso_date')
add = function('metadata_add_days')
registry = function('metadata_registry_load')
source = function('metadata_registry_check_source')

# Each count is a syntactic historical mechanism. A renamed equivalent defect
# could evade it; do not use this probe as an admission gate.
counts = {
    'C1_faulty_usage_substring': text.count("$out != *'RESEARCH_GATE: '*"),
    'C2_locale_unpinned_date_validator': int('local LC_ALL=C' not in iso),
    'C2_recursive_zero_strip': add.count('digits=${digits##+(0)}'),
    # Anchored to the non-table break branch only; the separator-accept branch
    # (header_found=1; header_candidate=0; continue) is legitimate and must not count.
    'C3_stale_candidate_columns': len(re.findall(r'\(\(header_found\)\) && break\n\s*header_candidate=0\n\s*continue', registry)),
    'C3_consumed_text_rescan': source.count('source_scan=${source_scan#*"$source_match"}'),
    'C3_pointer_predicate_on_registry_path': len(re.findall(r'(?<![a-z_])is_denylist_path\s+"\$(?:path|canon|fdcanon)"', registry)),
}
print(json.dumps({'kind': 'source-mechanism-probe-not-verdict',
                  'sha256': hashlib.sha256(text.encode()).hexdigest(),
                  'counts': counts,
                  'claim_totals': {'C1': counts['C1_faulty_usage_substring'],
                                   'C2': sum(v for k, v in counts.items() if k.startswith('C2_')),
                                   'C3': sum(v for k, v in counts.items() if k.startswith('C3_'))}}, indent=2))
