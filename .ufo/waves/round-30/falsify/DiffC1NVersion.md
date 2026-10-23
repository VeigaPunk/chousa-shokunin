# DiffC1NVersion — C1 implementation fidelity by N-version differential

VERDICT: hold — landed tool and the independent `ExecC1HeadB` implementation agree on every document the C1 counter's own generator produces (200/200 across fresh `build()` runs, seeds 0-9), and all observed disagreements are confined to HTML shapes the counter never generates; the counter's coverage score is not a measurement of a specific correct parser. Contract-v2-item-1 defects exist on both sides, but none is reachable from the counter.

## Method (ran)

- `importlib` load of `tools/quote-reopen.py` (landed, SHA-256 `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`, matches frozen) and `…/.ufo/waves/round-30/build/ExecC1HeadB/quote-reopen.py` (independent, SHA-256 `7f6d234fabe528650cefefb5818aaa526b39da0a263bc13e8bc500c0b270775c`).
- (a) 310 hand-generated documents: 80 targeted cases covering the requested shapes (no `<head>` start tag; stray `<html>`/`<head>`/`</body>`/`</html>`/`</br>` inside head; comments, incl. unclosed; CDATA; uppercase tags; attributes with `>`/`<` inside and outside quotes; `noframes`; nested `noscript`; self-closing SKIP tags; raw-text under/over-terminated; legacy/numeric charrefs) plus 230 random compositions (same token alphabet).
- (b) counter's own generator: `import c1_count; c1_count.build(random.Random(seed))` for seeds 0-9 → 200 documents.
- Comparison: `norm(html_to_text(doc))` on both modules. Script: `…/w2/DiffC1NVersion/diff_harness.py`, `probe.py`; results JSON `disagreements.json`.

## Results

- Counter-generated docs: agree 200/200 (seeds 0,1,5,9 re-run in `probe.py`: 20/20 each). **No disagreement class is reachable from the C1 counter's generator.**
- Hand-generated: 29/310 disagree. Classes (all with minimal example, `L`=landed, `I`=independent; outputs raw, then norm):

1. **End tags inside head end the head (I) vs. not (L).** `<head></body><noframes>N</noframes></head>` → L `""` (head continues, `noframes` content dropped); I `"N"`. Same for `</html>`, `</br>` inside head. Contract v2 item 1 ends the head at `</head>`, `<body>` start, other start tag, or non-whitespace character data — an end tag is none of these, so L follows the contract; I applies the HTML5 rule. (I's defect, contract-wise; not counter-reachable.)
2. **`noframes` content inside head: L drops, I emits.** `<head><noframes>NOFR</noframes><title>T</title></head><body>B</body>` → L `"B"`; I `"NOFRB"`. Contract: `noframes` is in the head start-tag list, so its content is head content and is dropped — L per contract, I diverges. (I's defect; not counter-reachable.)
3. **CDATA: L drops the whole declaration at the first `>` ; I pages content up to `>` and splits when the closing `]]>` is absent or the `>` fails.** `<body>A<![CDATA[ raw > data ]] >B</body>` → L `"A"`; I `"A data ]] >B"`. Contract silent (CDATA is not character data in the sense of the head rule; the counter never emits it). Neither side has contract grounding; the class is definitional.
4. **Block-element space leaks from inside SKIP elements in the body (L).** `<body>A<noscript><br></noscript>B</body>` → L `"A B"`; I `"AB"`. Contract item 1: content of `noscript` is dropped wherever it appears; if content is dropped, it cannot emit block spaces (`BLOCK` is defined as emitting a space at element boundaries, and a dropped element emits nothing). I per contract, L defect.
5. **Self-closing SKIP start tags: L treats them as void and emits the following text; I ignores the `/` (HTML5) and drops.** `<body>A<script/>x</script>B</body>` → L `"AxB"`; I `"AB"`. Same for `style`, `title`, `noscript`, `template`, and `<head/>` (L: `head` never opens, so content is emitted; I: head opens, content dropped). Contract: `title/script/style/noscript/template` content is dropped wherever it appears — I per contract, L defect.
6. **Mis-nested SKIP end tags: L's single counter decrements on any SKIP end tag, closing the wrong element (L).** `<template>A</noscript>B</template>` → L `"B"`; I `""`. Contract: `template` content is dropped — I per contract, L defect. Same effect in `<head><noscript><template>x</noscript>y</template>…` → L `"B"`, I `"yB"`.
7. **Unterminated raw text: L must see an exact `</script>`-style tag to leave CDATA; I's regex also accepts trailing whitespace but not a following alphanumeric.** `<body>A<script>x</script B>y</script>B</body>` → L `"AyB"`; I `"AyB"` (agree — good). Divergence only via case 5-style constructs; otherwise aligned.
8. **`&nbsp;` and numeric charrefs inside the head: L strips them as whitespace data; I unescapes then checks whitespace, so `&nbsp;X` ends the head and `X` is emitted.** `<head>&nbsp;X</head><body>B</body>` → L `"\xa0XB"` norm `"XB"`; I same norm `"XB"` — agree after norm. Not a disagreement in normalized output; noted for completeness.
9. **Unclosed comments / DTD / PI endings at EOF: L's declaration skip ends at the first `>` (CDATA class), I ends at `-->` for comments.** `"a<!--x"` → L `"a"`; I `"a<!--x"`. Contract silent; class definitional. (Counter never generates partial comments.)

Counter-reachability: none of classes 1-6 is produced by `make_doc` (head is `meta/title/link/style/script` plus optional `</head>`, `<body>`, `p/div/section/span/a/img/table/ul` blocks, inline markup without self-closing or misplaced end tags; no `noframes`, CDATA, comments, or self-closing SKIP). The counter's 106/106 does not exercise any diverging shape.

## Impact on axes

- C1 coverage: unaffected — both implementations agree on every counter-generated document; either tool scores 106/106 on the same generator. The claim's predicate is satisfied by the landed tool regardless of which parser is "correct" on out-of-distribution shapes.
- C2 operability: untouched (this seat never ran the fetch layer).
- Correctness vs contract v2 item 1: both sides have defects, but the counter cannot observe them. Item 1 fidelity is therefore not falsified by this differential; the defects are latent.

## Smallest safe correction (for the integrator, not a counter re-scale)

If contract v2 item 1 is to be exercised beyond the counter's own shapes, the landed tool needs: (i) type-balanced skip nesting (track the open element per skip level, not one counter); (ii) no `BLOCK` spaces emitted while inside a SKIP element; (iii) HTML5 self-closing semantics for non-void `script/style/title/noscript/template/head/noframes`; and the independent implementation needs: (i) not ending the head on `</body>`/`</html>`/`</br>` end tags; (ii) dropping `noframes` content while the head is open. Neither set is reachable from the counter, so no claim text needs to change.
