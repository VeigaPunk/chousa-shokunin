# CriticD3Classes — Routed Defect D3 Mutant Kill Verification on Round 29 Tool

## Scoped Verdict

**ALL THREE ROUND 29 SURVIVING MUTANTS ARE KILLED BELOW 78/106 BY THE FROZEN ROUND 30 C1 COUNTER.**

- **Pristine round 29 tool (`tools/quote-reopen.py` byte copy):** `QUOTE_REOPEN_HEADLESS_MATCH=78/106` (exit `1`)
- **`MutOrder` on round 29 tool:** `QUOTE_REOPEN_HEADLESS_MATCH=76/106` (exit `1`, `-2` vs baseline; killed by `order/too-long-unreachable`)
- **`MutSkipScript` on round 29 tool:** `QUOTE_REOPEN_HEADLESS_MATCH=66/106` (exit `1`, `-12` net vs baseline; `-40` on `*/script-window` and `*/title-window`, offset by `+28` on `headless-*/body-window`)
- **`MutCasefold` on round 29 tool:** `QUOTE_REOPEN_HEADLESS_MATCH=72/106` (exit `1`, `-6` vs baseline; killed by `closed-head/case-flip` on the round 29 tool, and by all `*/case-flip` classes once headless bodies are parsed)

Impacted axes: **coverage**, **operability**.

---

## 1. Exact Mutant Changes from Round 29 (`falsify/Mut*.md`)

1. **`MutOrder` (`.ufo/waves/round-29/falsify/MutOrder.md:21-44`):**
   In `verify()`, retains the `NO_SOURCE` check first, but moves `elif len(norm(quote).split()) > MAX_WORDS: verdict = "TOO_LONG"` to run **after** `fetch_page(url)` and `if text is None: verdict = "UNREACHABLE"`.
   ```diff
   --- a/tools/quote-reopen.py
   +++ b/tools/quote-reopen.py
   @@ -393,3 +393,0 @@
   -        elif len(norm(quote).split()) > MAX_WORDS:
   -            verdict = "TOO_LONG"
   -            detail = "%d words, limit %d" % (len(norm(quote).split()), MAX_WORDS)
   @@ -403,0 +400,3 @@
   +            elif len(norm(quote).split()) > MAX_WORDS:
   +                verdict = "TOO_LONG"
   +                detail = "%d words, limit %d" % (len(norm(quote).split()), MAX_WORDS)
   ```

2. **`MutSkipScript` (`.ufo/waves/round-29/falsify/MutSkipScript.md:27-39`):**
   Replaces the suppressed-element set `SKIP` at line 58 so that `script`, `style`, and `head` are no longer suppressed:
   ```diff
   --- a/tools/quote-reopen.py
   +++ b/tools/quote-reopen.py
   @@ -58 +58 @@
   -SKIP = {"script", "style", "noscript", "template", "head"}
   +SKIP = {"noscript", "template"}
   ```

3. **`MutCasefold` (`.ufo/waves/round-29/falsify/MutCasefold.md:13-28`, `MutCasefold/mutant.diff`):**
   In `found(text, quote)`, casefolds both the normalized quote and normalized page text before boundary-aware substring matching:
   ```diff
   --- a/tools/quote-reopen.py
   +++ b/tools/quote-reopen.py
   @@ -114 +114,2 @@
   -    q = norm(quote)
   +    q = norm(quote).casefold()
   +    text = text.casefold()
   ```

---

## 2. C1 Counter Classes (`corpus/evidence/round30/c1-count.py`)

`c1-count.py` (SHA-256 `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6`) with loopback harness `qr_harness.py` (SHA-256 `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4`) generates `FROZEN_TOTAL = 106` items per run with a fresh 64-bit `os.urandom` seed and no network calls:

- **20 documents (`5` items each = `100` document items):**
  - Document classes: `headless-body` (`5` docs), `headless-nobody` (`5` docs), `headless-text` (`4` docs), `closed-head` (`6` docs).
  - Per-document item kinds (`c1-count.py:245-251`):
    - `body-window` (`2` per doc = `40` total; `12` in `closed-head`, `28` across the `14` headless docs), label `VERBATIM`.
    - `title-window` (`1` per doc = `20` total; `6` in `closed-head`, `14` in headless docs), words inside `<head><title>...</title>`, label `ABSENT`.
    - `script-window` (`1` per doc = `20` total; `6` in `closed-head`, `14` in headless docs), words inside `<script>var note = "...";</script>` placed in head or body with probability `0.5`, label `ABSENT`.
    - `case-flip` (`1` per doc = `20` total; `6` in `closed-head`, `14` in headless docs), disjoint body window with one character's case swapped via `.swapcase()`, label `ABSENT`.
- **6 verdict-order items (`c1-count.py:252-270`):**
  - `order/too-long-unreachable` (`2` items): `26` to `30` words on `gone_sid`, whose loopback path is unregistered and returns HTTP `404`, label `TOO_LONG`.
  - `order/no-source-unregistered` (`1` item): `26` to `30` words on an unregistered `source_id`, label `NO_SOURCE`.
  - `order/no-source-urlless` (`1` item): `26` to `30` words on a registry row with no URL, label `NO_SOURCE`.
  - `order/unreachable` (`1` item): `8` words on `gone_sid` (HTTP `404`), label `UNREACHABLE`.
  - `order/too-long-reachable` (`1` item): `26` to `30` visible words on a reachable document, label `TOO_LONG`.

---

## 3. Scratch Execution and Receipts

Byte copies of `tools/quote-reopen.py` were created in `/fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/` and verified by `sha256sum`:

```sh
timeout 60 sha256sum /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-pristine.py /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutOrder.py /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutSkipScript.py /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutCasefold.py
```

Exit `0`. Each mutant's SHA-256 matches the exact mutant hash recorded in its round 29 falsify report:

| Variant in `/fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/` | SHA-256 | Matches round 29 hash |
|---|---|---|
| `quote-reopen-r29-pristine.py` | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` | `tools/quote-reopen.py` |
| `quote-reopen-r29-MutOrder.py` | `9049f2a3c660bc4b4d5076a28ffba0f7e345e4a0ef1f399a5811d6ad841d02d3` | `MutOrder.md:143` |
| `quote-reopen-r29-MutSkipScript.py` | `92b404eb0813cf109414c9b1ef26bcbb91c2a51020a761e9d44dc1d3913a5550` | `MutSkipScript.md:131` |
| `quote-reopen-r29-MutCasefold.py` | `c19f927aeee2dd1ec68b074049886dc810cfc6597869b9881716f8d4fc1527e1` | `MutCasefold.md:109` |

Commands run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```sh
timeout 120 python3 corpus/evidence/round30/c1-count.py --tool /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-pristine.py --receipt .ufo/waves/round-30/build/CriticD3Classes/receipt-r29-pristine.json
timeout 120 python3 corpus/evidence/round30/c1-count.py --tool /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutOrder.py --receipt .ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutOrder.json
timeout 120 python3 corpus/evidence/round30/c1-count.py --tool /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutSkipScript.py --receipt .ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutSkipScript.json
timeout 120 python3 corpus/evidence/round30/c1-count.py --tool /fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/quote-reopen-r29-MutCasefold.py --receipt .ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutCasefold.json
```

Summary of scored runs (all loopback; `net_connect_events: 21`, no external network traffic):

| Variant | Counter exit | Output | Seed | Wall (s) | Receipt |
|---|---:|---|---:|---:|---|
| Pristine round 29 | `1` | `QUOTE_REOPEN_HEADLESS_MATCH=78/106` | `16161065494100355937` | `0.049` | `.ufo/waves/round-30/build/CriticD3Classes/receipt-r29-pristine.json` |
| `MutOrder` | `1` | `QUOTE_REOPEN_HEADLESS_MATCH=76/106` | `7153732623931931967` | `0.053` | `.ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutOrder.json` |
| `MutSkipScript` | `1` | `QUOTE_REOPEN_HEADLESS_MATCH=66/106` | `152045468405045178` | `0.051` | `.ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutSkipScript.json` |
| `MutCasefold` | `1` | `QUOTE_REOPEN_HEADLESS_MATCH=72/106` | `1854963167695277012` | `0.053` | `.ufo/waves/round-30/build/CriticD3Classes/receipt-r29-MutCasefold.json` |

---

## 4. Per-Mutant Killing Classes and Interaction Analysis

### A. `MutOrder` (`76/106` vs `78/106` baseline)
- **Killing C1 item class:** `order/too-long-unreachable` (`0/2` in `MutOrder` vs `2/2` in baseline; both items have `label: "TOO_LONG"` and `got: "UNREACHABLE"`).
- **Mechanism:** `c1-count.py` builds two `26` to `30` word quotes against `gone_sid` (whose loopback URL returns HTTP `404`). Because `MutOrder` fetches and checks `text is None` before checking `len(norm(quote).split()) > MAX_WORDS`, it emits `UNREACHABLE` instead of `TOO_LONG` on both items, reducing the score by `2` (`78 -> 76` on the round 29 tool; `[INFERENCE]` `106 -> 104` on the landed round 30 tool).

### B. `MutSkipScript` (`66/106` vs `78/106` baseline)
- **Killing C1 item classes:**
  - `closed-head/script-window` (`0/6`), `headless-body/script-window` (`0/5`), `headless-nobody/script-window` (`0/5`), `headless-text/script-window` (`0/4`) — `0/20` total (`got: "VERBATIM"`, `label: "ABSENT"`).
  - `closed-head/title-window` (`0/6`), `headless-body/title-window` (`0/5`), `headless-nobody/title-window` (`0/5`), `headless-text/title-window` (`0/4`) — `0/20` total (`got: "VERBATIM"`, `label: "ABSENT"`).
- **Counteracting interaction on the round 29 base tool:**
  Because the round 29 `MutSkipScript` diff removes `"head"` as well as `"script"` and `"style"` from `SKIP`, applying it to the round 29 tool accidentally fixes the `28` headless `body-window` misses (`headless-body/body-window` `10/10`, `headless-nobody/body-window` `10/10`, `headless-text/body-window` `8/8`, `+28` items). However, because the `20` `script-window` items and `20` `title-window` items across all `20` documents now leak into extracted text (`-40` items), the net score drops by `12` points from `78/106` to `66/106`.
- **[INFERENCE] Wave 2 note on the landed tool:** On a landed round 30 tool that implements contract version 2 item 1 (dropping `title`, `script`, `style`, `noscript`, and `template` content wherever it appears and ending `<head>` at the first non-head element or non-whitespace character data), removing `"script"` and `"style"` from the dropped-element set will not gain any `body-window` items and will lose all `20` `*/script-window` items (`106 -> 86`), or `40` items (`106 -> 66`) if `"title"` / head suppression is also removed.

### C. `MutCasefold` (`72/106` vs `78/106` baseline)
- **Killing C1 item class on the round 29 tool:** `closed-head/case-flip` (`0/6` in `MutCasefold` vs `6/6` in baseline; `got: "VERBATIM"`, `label: "ABSENT"`).
- **Why `headless-*/case-flip` stays `14/14` on the round 29 tool:** On the `14` headless documents, the round 29 tool never exits `<head>`, so `html_to_text(doc)` returns `""`. Casefolding `""` still yields `False` (`ABSENT`), matching the `ABSENT` label on `headless-body/case-flip` (`5/5`), `headless-nobody/case-flip` (`5/5`), and `headless-text/case-flip` (`4/4`). On the `6` `closed-head` documents, body text is extracted, so casefolding causes all `6` `closed-head/case-flip` items to match (`VERBATIM`), dropping the score from `78/106` to `72/106`.
- **[INFERENCE] Wave 2 note on the landed tool:** Once the landed tool extracts body text on the `14` headless documents as well, `MutCasefold` will fail all `20` `case-flip` items (`closed-head/case-flip` `0/6`, `headless-body/case-flip` `0/5`, `headless-nobody/case-flip` `0/5`, `headless-text/case-flip` `0/4`), scoring `86/106`.

---

## 5. Limits and Isolation

- All four runs used independent random seeds drawn from `os.urandom` inside the loopback harness; however, the killing classes (`order/too-long-unreachable`, `*/script-window` + `*/title-window`, and `*/case-flip`) are constructed deterministically with fixed item counts (`2`, `20 + 20`, and `6` on round 29 / `20` on landed) on every seed.
- No lane production files, frozen counters, or git/jj state were modified. Scratch files reside in `/fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/`, and receipts reside in `.ufo/waves/round-30/build/CriticD3Classes/`. No tools were installed or updated.
