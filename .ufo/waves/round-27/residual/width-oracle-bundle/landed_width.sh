#!/usr/bin/env bash
# Landed cb895a2 header-width expression, verbatim, over the corpus.
# Emits: <row>\t<landed_width>
while IFS= read -r row; do
  orig=$row
  [[ $row == *'|'*'|'* ]] || { printf '%s\tSKIP\n' "$orig"; continue; }
  row=${row#"${row%%[![:space:]]*}"}
  row=${row%"${row##*[![:space:]]}"}
  [[ $row == '|'* ]] && row=${row#|}
  [[ $row == *'|' ]] && row=${row%|}
  local -a wc=()
  IFS='|' read -r -a wc <<<"${row//'\|'/}|__chousa_registry_end__"
  printf '%s\t%s\n' "$orig" "$((${#wc[@]} - 1))"
done < "$1"
