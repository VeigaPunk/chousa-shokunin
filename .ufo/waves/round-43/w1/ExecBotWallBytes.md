# ExecBotWallBytes

Axes: operability (capture present, both counters exit 0), calibration (267 bytes is not a correction of 265 characters), depth (verbatim command output, not a restated expectation).

File measured, read-only, no fetch:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt`

That directory is the campaign cache named by `tools/absent-split.py` (`CACHE`, line 43–45). The file is the staged S077 bot-wall capture. Decoded text contains `Client Challenge`.

## wc -c

Command: `wc -c` on that path.

```
267 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt
wc_exit=0
```

## python len()

Command: `Path.read_text(encoding="utf-8")` then `len(text)`.

```
265
py_exit=0
```

A first probe of the same decode also printed `bytes 267` and `len 265` and exited 0. Expectation was 267 bytes and 265 characters. Both match.

## Why the two numbers differ

One non-ASCII character, index 79, `U+2019` (UTF-8 length 3, `repr` `'’'`). 264 ASCII characters plus that one character is 265. 264 + 3 = 267 bytes. `endswith_newline` is True, so the published 265 is the decoded length including the trailing newline. `len` after stripping a trailing newline would be 264 and is not the figure the erratum cites.

This agrees with the append-only erratum in `corpus/lessons/round-42.md`: "The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters." Neither number corrects the other.

No lane production file was modified. No network.

Report: .ufo/waves/round-43/w1/ExecBotWallBytes.md
