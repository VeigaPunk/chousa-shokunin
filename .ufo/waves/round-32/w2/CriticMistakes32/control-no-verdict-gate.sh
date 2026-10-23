#!/usr/bin/env bash
# Review-only wrong-output control. The underlying landed gate is not mutated.
set -o pipefail
bash /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/lane/tools/research-gate.sh "$@" |
  while IFS= read -r line; do
    case "$line" in
      'RESEARCH_GATE:'*) ;;
      *) printf '%s\n' "$line" ;;
    esac
  done
exit "${PIPESTATUS[0]}"
