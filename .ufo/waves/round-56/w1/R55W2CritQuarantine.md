# R55W2CritQuarantine — S125 lesson verdict

## Attack
Attacked round 55 lesson’s S125 quarantine claim: that `absent-as-written` is appropriate because two of three strings occur in the defined form and the third differs only by curly quotes; also tested the sentence that the register’s `payload-absent` is wrong for two quotes.

## Evidence
Register evidence: `grep -n 'round6 | S125' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` returned row 56, S125, class `payload-absent`, containing the three quoted strings and the statement that the quote is in none of the checked materials.

Defined form: ran `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw`, saving stdout to scratch. Its length was 13,718 characters. Counts and offsets from exact search:

| Form | Quote 1 | Quote 2 | Quote 3 exact | Quote 3 with curly quotes around 灰色文献 |
|---|---:|---:|---:|---:|
| capture-text stdout (defined OLE form) | 1 @ 4625 | 1 @ 761 | 0 | 1 @ 994 |
| `.txt` sidecar | 0 | 0 | 0 | 0 |
| raw decoded as UTF-16LE | 1 @ 57444 | 1 @ 53524 | 0 | 1 @ 53757 |

The lesson’s round-55 S125 paragraph (line 63) says the same essential thing: two exact strings occur, and the third is exact only with curly quotation marks. Its own all-located-quotes section lines 83–86 records the relevant OLE-form contents and offsets: the first quote begins at 4625, the second at 761, and the third sentence with `“灰色文献”` begins at 994. Its stated defined form is capture-text stdout, not the sidecar or UTF-16LE decoding.

The lesson itself explains the class at line 38: `absent-as-written` means a mismatch in written form, while not asserting fabrication. Round-48 precedent includes materially non-exact composites and quote/layout mismatches under that class (round-48 lesson lines 43–51, including a row with one quote exact and others misquoted).

Commands run: the register grep above; the capture-text invocation above; a Python exact-string count/offset calculation for all three forms; and `grep -rn 'absent-as-written' .../corpus/lessons | head`, which surfaced round-48’s class definition and examples.

## Finding
`absent-as-written` is the right class under the lane’s observed usage: the register’s *three-string payload* is not present as written because its third string lacks the source’s curly quotes. The evidence does not support changing the lesson verdict to `present` merely because the underlying statement is present with altered punctuation; that would conflate substance with exact written presence. The narrow note should say explicitly that two strings match exactly and the third is present with curly quotes around 灰色文献. The sentence “the register’s payload-absent is wrong for two quotes” is correct: two of its quoted strings are in fact present in the defined form. The third is not present exactly as written, so this evidence does not establish that the full payload is present as written.

## Axes
- **Calibration:** supports the lesson’s distinction between exact written form and substance; the claimed punctuation mismatch is confirmed.
- **Depth:** three representations were independently counted; only capture-text stdout is the defined form, and the other two were not used to override it.
- **Operability:** the derivation is reproducible from the documented capture command and exact string searches.

VERDICT: S125’s `absent-as-written` lesson verdict survives; two quote strings make the register’s `payload-absent` assertion wrong as to those strings, while the third remains absent as written.