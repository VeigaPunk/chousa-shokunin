# ExecFormProbe — round 49 w1 report

Seat: ExecFormProbe (executor, leaf). Assignment: per-capture form metrics for nine theme captures, odd-aligned UTF-16LE probe against `build-spans.py`, plus keyword offsets in the two `.doc` captures.

## Method and code rule

- Read `corpus/evidence/round49/build-spans.py` lines 55–65 and 101–125. `form_texts()` returns `.txt` first (UTF-8 with replacement), then `.raw` decoded as UTF-16LE from byte zero with replacement. `build()` accepts a quote only when it occurs exactly once in at least one returned form; it selects the first matching form. It never tries decoding `.raw` from byte offset 1.
- Ran Python stdlib scripts against only the nine specified qcache keys; no network, installs, scratch artifacts, or external campaign tools. CJK count here means code points in U+3400–U+4DBF or U+4E00–U+9FFF; FFFD means U+FFFD code points. For `.raw`, offsets 0 and 1 are decoded with `errors='replace'` exactly as requested.
- URL-to-key check: SHA-256 first-24 mappings from staged IDs S087,S088,S089,S091,S092,S100,S101,S102,S103 respectively matched the nine requested keys in order (Python `hashlib.sha256(url.encode()).hexdigest()[:24]`).

## Per-key measurements

Bytes are file sizes; CJK / FFFD are decoded-character counts. `odd-only CJK` is literal CJK code points in offset-1 decoding which are not CJK at the same character position in the offset-0 decoding; this detects decoding-dependent characters, not proof that every such character is meaningful source text. The last column assesses the requested span-builder miss risk.

| key (staged id) | .txt bytes; CJK; FFFD | .raw bytes | raw UTF-16LE @0 CJK; FFFD | raw UTF-16LE @1 CJK; FFFD | odd-only CJK | Would exactly-once builder miss odd-aligned text? |
|---|---:|---:|---:|---:|---:|---|
| `09fc63de41f293d43d631c46` (S087) | 12,901; 1,387; 0 | 41,404 | 11,852; 0 | 11,852; 1 | 3,376 | **Potentially yes** if desired quote occurs only in the odd decode; builder searches .txt then aligned raw only. This `.txt` exists, so odd-only text is not searched. |
| `167e9db7dde3c998838e3469` (S088) | 15,656; 1,452; 0 | 52,944 | 16,275; 0 | 16,145; 1 | 4,667 | **Potentially yes**, same rule; nonzero odd-only CJK. |
| `fea98dc5a5a486c988dd415c` (S089) | 95,733; 10,486; 0 | 178,654 | 43,579; 0 | 43,505; 1 | 18,301 | **Potentially yes**, same rule; nonzero odd-only CJK. |
| `76914d78c20094f677dea77d` (S091) | 15,270; 2,677; 0 | 197,752 | 45,570; 0 | 45,731; 1 | 10,682 | **Potentially yes**, same rule; nonzero odd-only CJK. |
| `32d1d24b24fce96d2a078ec0` (S092) | 2,796; 0; 0 | 14,258 | 5,553; 0 | 5,524; 1 | 993 | **Potentially yes**, same rule; `.txt` has no CJK, and raw decode contains odd-only CJK. |
| `b539a80218080da56a75b624` (S100, `.doc`) | 1,406,840; 1,104; 308,430 | 801,280 | 157,853; 11,154 | 158,294; 11,347 | 81,199 | **Yes, demonstrated for a staged quote**: the self-citation quote occurs once at aligned raw and zero times at offset 1; however the .txt is an invalidly decoded binary `.doc` and does not preserve it. Other odd-only text can be missed. |
| `6dc68fd6b32ce9c8dfcebce8` (S101, `.doc`) | 157,816; 15; 14,486 | 129,024 | 15,515; 263 | 20,234; 211 | 10,730 | **Yes, demonstrated for staged quotes**: `文献类型及载体类型标志` occurs once aligned and zero times odd; `GB/T 7714` occurs four times aligned and zero times odd. `.txt` does not contain those terms. |
| `7809d5114330a60527436b07` (S102) | 30,277; 2,965; 0 | 5,066,141 | 1,043,633; 79,329 | 1,056,466; 78,936 | 542,811 | **Potentially yes**, large binary/raw-vs-text content difference and nonzero odd-only characters; no assertion that those raw characters are coherent text. |
| `02aefcf570a7108e699d0990` (S103) | 22,631; 6,258; 0 | 6,550,066 | 1,324,146; 93,229 | 1,328,675; 93,823 | 703,599 | **Potentially yes**, same caution; nonzero odd-only characters, but binary PDF raw is not necessarily text. |

Observed additional fact: the `.pdf` files for S102 and S103 each have exactly the same size and bytes as their `.raw` files (5,066,141 and 6,550,066 bytes respectively). The `.raw` metrics for those PDFs are therefore decodes of binary PDF bytes, not clean text transcriptions. For S100 and S101, `.txt` is also binary-garbage extraction (large U+FFFD counts); relevant document text was recoverable by aligned UTF-16LE raw decoding.

## Odd alignment and interpretation

A low-cost literal probe compared decoded strings character-by-character and counted offset-1 CJK code points not CJK at the corresponding offset-0 position; all nine forms yielded positive counts (table). The probe confirms that the two decodings differ and that the builder's sole raw decode is specifically aligned at byte 0. It does **not** establish that the many offset-1 “CJK” characters are semantic text: binary DOC/PDF/XML-like bytes also decode to CJK-range code points. For the two DOCs, the stronger direct test is the exact staged quotation: the useful Chinese strings are present in aligned decoding, not in odd decoding or `.txt`. Thus these observations do not demonstrate that the frozen C2 quotes are lost by the builder; they show that odd-offset-only quote searches are unsupported, and that applying CJK counts to binary `.raw` is a noisy text-quality proxy.

## Requested terms in the two `.doc` captures

Offsets below are Python Unicode code-point offsets in the offset-0 UTF-16LE decoded string, not byte offsets. Search in `.txt` returned no requested terms; offset-1 decode also returned none.

- S100 / `b539a80218080da56a75b624.raw`: `自引` at 1425 (first occurrence; 2 total). Context: `...18601173042\r\r关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定...`. Its staged co-author self-citation quote occurs once in raw@0 and zero times raw@1 / `.txt`.
- S101 / `6dc68fd6b32ce9c8dfcebce8.raw`: `文献标志码` at 10922 (14 total); context begins `11中图分类号(CLC number)与文献标志码(Document code)\r11.1...`. `GB/T 7714` at 12000 (4 total); context includes `...本规范推荐采用GB/T 7714中规定的顺序编码制格式著录...`. Both terms occur zero times in `.txt` and raw@1. Another requested S101 staged quotation, `文献类型及载体类型标志`, occurs once raw@0 and zero times in other searched forms.
- The third requested term `自引` does not occur in S101; `文献标志码` and `GB/T 7714` do not occur in S100 in any searched form.

## Evidence commands and observed output

Commands were run through the Python evaluation kernel using stdlib `pathlib`, `hashlib`, `re`; commands are summarized here with exact observed results (the table reproduces the complete metric output). The first file listing command was `ls -la <qcache>/{nine keys}*` and showed all requested `.txt`/`.raw` files, plus `.pdf` for the final two keys. Relevant excerpt:

```text
-rw-r--r-- ... 41404 .../09fc63de41f293d43d631c46.raw
-rw-r--r-- ... 12901 .../09fc63de41f293d43d631c46.txt
-rw-r--r-- ... 197752 .../76914d78c20094f677dea77d.raw
-rw-r--r-- ... 15270 .../76914d78c20094f677dea77d.txt
-rw-r--r-- ... 801280 .../b539a80218080da56a75b624.raw
-rw-r--r-- ... 1406840 .../b539a80218080da56a75b624.txt
-rw-r--r-- ... 129024 .../6dc68fd6b32ce9c8dfcebce8.raw
-rw-r--r-- ... 157816 .../6dc68fd6b32ce9c8dfcebce8.txt
-rw-r--r-- ... 5066141 .../7809d5114330a60527436b07.raw
-rw-r--r-- ... 30277 .../7809d5114330a60527436b07.txt
-rw-r--r-- ... 6550066 .../02aefcf570a7108e699d0990.raw
-rw-r--r-- ... 22631 .../02aefcf570a7108e699d0990.txt
```

The per-key metric program read each `.txt` using UTF-8 `errors='replace'`, each `.raw` as bytes, then `decode('utf-16le', errors='replace')` and `bytes[1:].decode('utf-16le', errors='replace')`; exact metric output is the table above. Offset probe emitted:

```text
S100 '对于合作发文的参考文献中，如果引文出现了任一': txt=0 raw@0=1 raw@1=0
S100 '他引频次': txt=0 raw@0=7 raw@1=0
S101 '文献类型及载体类型标志': txt=0 raw@0=1 raw@1=0
S101 '以单字母方式标识以下各种参考文献类型': txt=0 raw@0=2 raw@1=0
S101 'GB/T 7714': txt=0 raw@0=4 raw@1=0
```

Keyword scan output: S100 raw@0 `自引` code-point offset 1425; S101 raw@0 `文献标志码` offset 10922 and `GB/T 7714` offset 12000. All had no hit at offset 1 or in `.txt`.

No tools installed or updated (`~/.omp/agent/RULES.md` read; no install was needed). No tests/build/lint/formatters run. No scratch directory was created.

VERDICT: Attacked the nine-capture form/odd-alignment falsifier — all keys have offset-1-vs-offset-0 CJK differences, but raw CJK counts are noisy for binary forms; the two DOC captures’ staged Chinese quotations and requested terms are recoverable in offset-0 UTF-16LE and missed by `.txt`/offset-1, so this does not falsify C2's frozen quote rule but documents its form-selection limitation.
