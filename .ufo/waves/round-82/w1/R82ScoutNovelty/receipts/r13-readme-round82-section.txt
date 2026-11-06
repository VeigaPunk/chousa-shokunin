# R13 — corpus/README.md round-82 section vs the tree at the landing revision
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
git -C $L show b4a41d251b488f06b4a6ab01a11bc12ce72edd20:corpus/README.md | sed -n '1377,1386p'
echo "--- does corpus/lessons/round-82.md exist at the landing revision?"
git -C $L ls-tree -r --name-only b4a41d251b488f06b4a6ab01a11bc12ce72edd20 -- corpus/lessons/round-82.md
echo "ls-tree rc=$? (empty output = file absent)"
echo "--- and at HEAD?"
git -C $L ls-tree -r --name-only HEAD -- corpus/lessons/round-82.md
echo "ls-tree rc=$? (empty output = file absent)"
echo "--- base Frontier line 859 still naming S008 as queued:"
git -C $L show b4a41d251b488f06b4a6ab01a11bc12ce72edd20:corpus/README.md | sed -n '859p'
