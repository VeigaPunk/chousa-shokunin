#!/bin/bash
cat <<'EOL'
CLAIM id=cbfa0ea5ed9 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=cbfa0ea5ed9 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c3c0d07b72f expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=cbd6a8355ee expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c8d29ec9c21 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=ce5d6611c29 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c07c07dbcd9 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c59ebe8d0e0 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=caf325f2b55 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=cc6f5c49098 expected=supported observed=mislocated source=src at=- verdict=match
CLAIM id=c5868bb6af6 expected=supported observed=mislocated source=src at=- verdict=match
CLAIM id=c39efa74f7f expected=supported observed=supported source=src at=- verdict=match
CLAIM id=cc52a6dca24 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c4226c7350a expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c56c5461957 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c58efdd54e8 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c12810bff4d expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c93c31269a5 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c2ff6752a75 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=ce58c437d23 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c43983a6659 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=cc06287a46f expected=supported observed=mislocated source=src at=- verdict=match
CLAIM id=cefdf8a62f0 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c8005bf9cbb expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c09a5fafca0 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c2b14efc34f expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c0d58ce7b2a expected=supported observed=supported source=src at=- verdict=match
CLAIM id=cd1705494a1 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=cdba8760bd0 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c4517d1104d expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=cfe0e279d53 expected=supported observed=supported source=src at=- verdict=match
CLAIM id=cd344822674 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c251b8e71af expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c3d7e85974e expected=supported observed=mislocated source=src at=- verdict=match
CLAIM id=c9cc1a7f886 expected=supported observed=unsupported source=src at=- verdict=match
CLAIM id=c73e38c70ce expected=supported observed=supported source=src at=- verdict=match
CLAIM id=c9d146f9b8c expected=supported observed=supported source=src at=- verdict=match
CLAIM id=ce316195207 expected=supported observed=unsupported source=src at=- verdict=match
FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=cc6f5c49098 line=1-2 first_delimited_occurrence=line:1
FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=c5868bb6af6 line=1-2 first_delimited_occurrence=line:1
FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=cc06287a46f line=1-2 first_delimited_occurrence=line:1
FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=cbfa0ea5ed9 line=1-2 first_delimited_occurrence=line:1
RESEARCH_GATE: DRIFT
EOL
exit 1
