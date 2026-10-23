#!/bin/bash
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
cat > "$D/non-gnu-grep" <<'G'
#!/bin/sh
case "$1" in --version|-V) printf '%s\n' "grep (pi-uu-grep) 0.2.0"; exit 0;; esac
exit 0
G
chmod 755 "$D/non-gnu-grep"
unshare --user --map-root-user --mount --propagation private bash -c '
  set -u
  D=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
  mount --bind "$D/non-gnu-grep" /usr/bin/grep || exit 93
  cd "$D/clone"
  echo "  GNU grep on PATH: $(PATH=$D/nsbin:/usr/local/bin:/usr/bin:/bin grep --version 2>&1 | head -1)"
  echo "  BASE gate (round-34 blob), PATH has GNU grep:"
  env -i HOME=/tmp PATH="$D/nsbin:/usr/local/bin:/usr/bin:/bin" CHOUSA_NOW_EPOCH=1750000000 \
    bash .ufo/waves/round-35/repairs/base-gate.sh verify --record corpus/fixtures/archives-r9/A-r9.md --root "$D/root" \
    >"$D/out4/ns-base.out" 2>"$D/out4/ns-base.err"
  echo "    base rc=$?"
  grep -hE "^RESEARCH_GATE: " "$D/out4/ns-base.out" | sed "s/^/    /"
  echo "  LANDED gate, same PATH:"
  env -i HOME=/tmp PATH="$D/nsbin:/usr/local/bin:/usr/bin:/bin" CHOUSA_NOW_EPOCH=1750000000 \
    bash tools/research-gate.sh verify --record corpus/fixtures/archives-r9/A-r9.md --root "$D/root" \
    >"$D/out4/ns-landed.out" 2>"$D/out4/ns-landed.err"
  echo "    landed rc=$?"
  grep -hE "^RESEARCH_GATE: |GREP_PROVENANCE" "$D/out4/ns-landed.out" "$D/out4/ns-landed.err" | sed "s/^/    /"
'
