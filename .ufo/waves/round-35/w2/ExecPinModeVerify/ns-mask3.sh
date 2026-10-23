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
  env -i HOME=/tmp PATH=/usr/local/bin:/usr/bin:/bin CHOUSA_NOW_EPOCH=1750000000 \
    bash tools/research-gate.sh verify --record corpus/fixtures/archives-r9/A-r9.md --root "$D/root" \
    >"$D/out4/ns-default-noshim.out" 2>"$D/out4/ns-default-noshim.err"
  echo "ns-default-noshim rc=$?" > "$D/out4/ns-default-noshim.rc"
  env -i HOME=/tmp PATH="$D/shim4:/usr/local/bin:/usr/bin:/bin" CHOUSA_GREP_PIN_ECHO=1 CHOUSA_NOW_EPOCH=1750000000 \
    bash tools/research-gate.sh verify --record corpus/fixtures/archives-r9/A-r9.md --root "$D/root" \
    >"$D/out4/ns-default-headshim.out" 2>"$D/out4/ns-default-headshim.err"
  echo "ns-default-headshim rc=$?" > "$D/out4/ns-default-headshim.rc"
  env -i HOME=/tmp PATH="$D/nsbin:/usr/local/bin:/usr/bin:/bin" CHOUSA_NOW_EPOCH=1750000000 \
    bash tools/research-gate.sh verify --record corpus/fixtures/archives-r9/A-r9.md --root "$D/root" \
    >"$D/out4/ns-pathfallback.out" 2>"$D/out4/ns-pathfallback.err"
  echo "ns-pathfallback rc=$?" > "$D/out4/ns-pathfallback.rc"
'
