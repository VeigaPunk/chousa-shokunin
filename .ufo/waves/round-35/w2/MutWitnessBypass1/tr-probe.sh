f() { set +x; echo hidden-a; set -x; echo visible-b; }
f
set +x
echo hidden-c
set -x
echo visible-d
