
while IFS= read -r row; do
  [[ $row == *'|'*'|'* ]] || { printf 'SKIP\n'; continue; }
  row=${row#"${row%%[![:space:]]*}"}
  row=${row%"${row##*[![:space:]]}"}
  [[ $row == '|'* ]] && row=${row#|}
  [[ $row == *'|' && $row != *'\|' ]] && row=${row%|}
  split_row=${row//\\/\\\\}
  split_row=${split_row//'\\|'/'\|'}
  IFS='|' read -a cells <<<"${split_row}|__chousa_registry_end__"
  cells=("${cells[@]:0:${#cells[@]}-1}")
  out=""
  for c in "${cells[@]}"; do
    c=${c#"${c%%[![:space:]]*}"}
    c=${c%"${c##*[![:space:]]}"}
    out+="${c}"$'\x1f'
  done
  printf '%s\n' "${out%$'\x1f'}"
done < "$1"
