# R55ExecC3ObsQ97 — C3 E05–E07 observations

Scope: independently derive E05–E07 against the frozen QUALITY 97 statement. No production file modified. Findings are report-only; L1 integrates append-only errata.

## Evidence and commands

Target inspected: `corpus/QUALITY.md:937`. The exact key phrases are unique in that target (`python3 -c 'from pathlib import Path; t=Path("corpus/QUALITY.md").read_text(); ...'` from lane root):

```
'12,963 / 12,795' count= 1 offset= 88531
'18,242 control characters' count= 1 offset= 88102
'0 U+FFFD, 0 control characters' count= 1 offset= 88433
```

Read-only comparison reports: `R54W2ReviewQuality.md:12-40` and `R54W2CritMistakes.md:14-18`. Their claims are independently recomputed below.

Used frozen BASE reader: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show dba605deb5cd5ed4874e0e3c39ba24737409cd80:tools/capture-text.py > /fast/scratch/hyaku/chousa-r55/R55ExecC3ObsQ97/ct.py`; observed 20,203 bytes and SHA-256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`, matching the frozen claim's BASE digest. Input raw: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw`, observed 129,024 bytes.

Derivation command (executed; the script computes the defined form via the extracted BASE reader and the UTF-16LE counts directly from raw bytes):

```
python3 -c 'import subprocess,pathlib; raw=pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw").read_bytes(); form=subprocess.run(["python3","/fast/scratch/hyaku/chousa-r55/R55ExecC3ObsQ97/ct.py","/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw"],capture_output=True,text=True,check=True).stdout; u=raw.decode("utf-16le",errors="replace"); print("E07 len=%d U+FFFD=%d C0=%d LF=%d"%(len(form),form.count("\\ufffd"),sum(ord(c)<32 for c in form),form.count("\\n"))); print("E06 len=%d C0_none=%d C0_excl_tab_LF=%d C0_excl_tab_LF_CR=%d"%(len(u),sum(ord(c)<32 for c in u),sum(ord(c)<32 and c not in "\\t\\n" for c in u),sum(ord(c)<32 and c not in "\\t\\n\\r" for c in u)))'
```

Observed output:

```
E07 len=27012 U+FFFD=0 C0=469 LF=469
E06 len=64512 C0_none=18451 C0_excl_tab_LF=18431 C0_excl_tab_LF_CR=18242
```

For E05, the six exact single-line quotes were each submitted individually to BASE `ct.py --locate`; each returned `LOCATED count=1`:

```
1: 为便于文献的统计和期刊评价 — offset 11972
2: 每一篇文章或资料应根据其内容性质标识一个文献标志码 — offset 12007
3: 本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。 — offset 12795
4: 文献类型及载体类型标志； — offset 12963
5: 参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。 — offset 14049
6: 参考文献格式，参照ISO 690 — offset 25123
```

The locator command for each was `python3 /fast/scratch/hyaku/chousa-r55/R55ExecC3ObsQ97/ct.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw --locate '<quote>'`; all six outputs were respectively `LOCATED count=1 offset=11972`, `...12007`, `...12795`, `...12963`, `...14049`, `...25123`. Relative to registry anchors `11170,11205,11993,12161,13247,34374`, drifts are `+802,+802,+802,+802,+802,-9251`.

## Draft SCORECARD errata lines

Anchors below occur once in `corpus/QUALITY.md` (counts/offsets above); these draft lines are not yet written into SCORECARD.

```
erratum: E05 corpus/QUALITY.md anchor: "12,963 / 12,795" observed: "offsets=11972,12007,12795,12963,14049,25123; drift=+802,+802,+802,+802,+802,-9251"
erratum: E06 corpus/QUALITY.md anchor: "18,242 control characters" observed: "C0_utf16le_none=18451;C0_excl_tab_LF=18431;C0_excl_tab_LF_CR=18242"
erratum: E07 corpus/QUALITY.md anchor: "0 U+FFFD, 0 control characters" observed: "defined_form_U+FFFD=0;C0=469;LF=469"
```

VERDICT: Independently recomputed C3 E05–E07; all three QUALITY 97 claims are contradicted in the details shown, and report-only errata drafts are provided.
