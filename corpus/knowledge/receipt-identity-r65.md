source: S154 — installed git-cat-file(1), Git 2.56.0, OUTPUT; S155 — /usr/lib/python3.14/hashlib.py:27–34, Python 3.14.8; S156 — corpus/evidence/round64/controls/c1v3-before-full.txt:1,44
verified-at: 2026-10-30
recheck: re-open the three pinned sources and run python3 corpus/evidence/round65/c2-count.py; recheck semantics on Git or Python upgrade

# Receipt identity is not execution authenticity

## Claims

1. S154's installed manual says under OUTPUT: “If <type> is specified, the raw (though uncompressed) contents of the object will be returned.” The receipt validator requests type `blob` at the caller's full revision plus repository-relative path. Inference: this selects committed contents, not the current working tree. The supplied repository and revision remain caller choices.
2. S155's hashlib module documentation says `digest()` returns the digest of bytes passed to `update()`; `hexdigest()` represents that digest as hexadecimal. Located quote, lines31–32: “Return the digest of the bytes passed to the update() method”. Inference: a matching SHA256 value binds a reported digest to the selected blob bytes under the hash assumption; it does not establish who ran a command.
3. S156 begins “LEG CLEAN clean ok ok” and ends with a BATTERY=FAIL summary, without a self-contained revision/exit/digest header. The round64 claims file supplies surrounding provenance; the observation here is missing in-file headers, not that the historical receipt has no provenance anywhere.
4. Inference from these sources: revision identity, blob-content digest and an asserted process exit answer different questions. In the round65 format, `EXIT=1` can be a consistent report of a failed command. The validator's own exit0 means header/blob consistency, not that the measured command passed.

## Limits

This format does not prove execution authenticity. A person can write an arbitrary body and EXIT alongside a genuine blob digest. There is no command/body binding, signature, trusted timestamp or process attestation. Replaying a valid header with fabricated output can pass. No receipt identity debt from round1 is resolved by this local consistency checker.

The frozen twenty-case counter checks named interface examples, not arbitrary malformed-input completeness or semantic entailment. Git object replacement/configuration and caller-selected repositories are trust assumptions, not a sandbox. Working tree modifications do not change the committed blob selected by the receipt.

## Use in research

Keep the declared observation and its provenance separate: quote the measured output, retain the reported child exit, and pin the instrument blob. Never turn structural consistency into a claim that a source was truly fetched or a command truly ran. An outside reviewer must still re-open the source and check the claim against it.
