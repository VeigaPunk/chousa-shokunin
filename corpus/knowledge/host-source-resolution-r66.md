source: S158 — git.git Documentation/git-cat-file.adoc at 50fe5cc63f9cd6e89b87a2c9ccf96a444f4cfdb7, OUTPUT section; S159 — corpus/evidence/round66/controls/before-host-pins.txt at 8c2a0a2add04d0e74222d58a3f695aab95a13cf9
verified-at: 2026-10-31 (host pins measured on Windows/11, git 2.55.0.windows.3; upstream adoc fetched and pinned, quote re-opened VERBATIM by tools/quote-reopen.py)
recheck: on a host change or a Git/Python upgrade re-run `python corpus/evidence/round66/host-pins.py` from the lane root; on the next git.git tip change, re-fetch S158 at the then-current commit and re-open the quote

# A citation anchored to an installed-local path is host-scoped; re-anchor by hopping to a pinned canonical upstream

## Claims

1. S159's receipt measures both round-65 installed-local pins on this host: `PINS_PRESENT=0/2` — S154's `/usr/share/man/man1/git-cat-file.1.gz` and S155's `/usr/lib/python3.14/hashlib.py` are both absent on Windows/11 — and the host git is 2.55.0.windows.3, so `GIT_PIN_MATCH=no` against the 2.56.0 manual pinned in S154's anchor. Observation: a registry anchor that names an installed-local path resolves only on the host class where that path exists.
2. S158 restates S154's located sentence in the upstream documentation source at a pinned commit: the OUTPUT section of `git-cat-file.adoc` at git.git tip `50fe5cc63f9cd6e89b87a2c9ccf96a444f4cfdb7` carries "If `<type>` is specified, the raw (though uncompressed) contents of the `<object>` will be returned.", byte-identical to the capture (`sha256 3a8971e70ef50cc4b8c7b06c5696b382b30b4765303ab4dd986b140cd75cc847`, committed under `corpus/evidence/round66/captures/`) and re-opened `VERBATIM` by `tools/quote-reopen.py` on 2026-10-31. Inference: the citation chain hops from the absent local surface to the canonical upstream; the hop is honest only when the upstream is pinned to a revision and the fetched bytes are committed.
3. S160 records the tested alternative: the versioned `git-scm.com/docs/git-cat-file` page (HTTP 200, 79,360 bytes, capture committed) contains the sentence but pins no revision — its content moves with releases. Inference: for a web anchor, a URL that serves whatever the latest release renders is a lead (tier C), not an anchor; the anchor must name a commit, tag, or immutable permalink.

## Limits

One host and one point in time are measured: Windows/11 with git 2.55.0.windows.3 on 2026-10-31; the drift receipt says nothing about other hosts, and the pinned upstream commit is itself a moving tip whose recheck is `on-release`.

The committed capture and the `VERBATIM` verdict are byte evidence of access and of the quote's location; they are not truth of the claim (support state 3 only, QUALITY criterion 8). The r65 rows S154–S156 stay as committed — their facts were verified on the old host and are not rewritten; this entry adds the host-scoped reading and the re-anchor, not a correction of those rows.

## Use in research

When a citation's local surface is absent on the current host, resolve the hop in this order: find the canonical upstream source of the same document, pin it to a revision (commit, tag, or permalink), fetch once, commit the capture bytes with their sha256, re-open the located quote with `tools/quote-reopen.py`, and register the re-anchor as a new row that names the row it re-anchors. Record the drift itself as an own-work receipt row so the next reader can see which pins are host-scoped. Never quietly relabel the old row's anchor as if it still resolved.
