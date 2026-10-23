set -u
GATE=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
W=/tmp/hyaku/chousa-r35/w2/ExecPinModePinDrift/work
D=/tmp/hyaku/chousa-r35/w2/ExecPinModePinDrift
export TMPDIR=$W/tmp
run() { # label mode path env...
  local label=$1 mode=$2 path=$3; shift 3
  local out err rc
  out=$("$@" 2>"$W/m.err"); rc=$?
  err=$(cat "$W/m.err")
  printf '%s\n  exit=%s\n  stdout=%s\n  stderr=%s\n' "$label" "$rc" "${out:-<empty>}" "${err:-<empty>}"
}
clean() { env -u CHOUSA_GREP_PIN_ECHO -u RESEARCH_GATE_GREP -u BASH_ENV -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT "$@"; }
rel() { env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV RESEARCH_GATE_GREP=bin/grep "$@"; }
nong() { env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV RESEARCH_GATE_GREP=$D/nongnu-banner "$@"; }
rm -f $W/m1.baseline $W/m2.baseline $W/m3.baseline
echo "### M1 --pin clean env"
run M1 --pin $W/m1.baseline clean bash "$GATE" --pin $W/m1.baseline
echo "  file: $(ls -l $W/m1.baseline 2>&1 | sed 's/^ *//')"
echo "### M2 --pin refused relative override"
run M2 --pin $W/m2.baseline rel bash "$GATE" --pin $W/m2.baseline
echo "  file: $(ls -l $W/m2.baseline 2>&1 | sed 's/^ *//')"
echo "### M3 --pin refused non-GNU override"
run M3 --pin $W/m3.baseline nong bash "$GATE" --pin $W/m3.baseline
echo "  file: $(ls -l $W/m3.baseline 2>&1 | sed 's/^ *//')"
echo "### M4 --drift clean env (baseline from M1)"
run M4 --drift $W/m1.baseline clean bash "$GATE" --drift $W/m1.baseline
echo "### M5 --drift refused relative override"
run M5 --drift $W/m1.baseline rel bash "$GATE" --drift $W/m1.baseline
echo "### M6 --drift refused non-GNU override"
run M6 --drift $W/m1.baseline nong bash "$GATE" --drift $W/m1.baseline
