# Round 25 — metadata mutant fixtures

**Scope:** Writer fixture assignment only. Private clone base observed by `git -C /tmp/chousa-r25-ExecMetaMutants-3 rev-parse HEAD`: `b820e4e40ce52deedf53b191140cd7b08ddda929`.

**Behavior:** Added `corpus/fixtures/metadata-r25/README.md` with hand-derived spec-v1 expected `META` lines, finding IDs, and normal/strict exit status for every single-file run; added 18 one-defect mutants, six metadata edge fixtures (CRLF, BOM first line, value continuation, ISO-date/90d/on-release rechecks), and three clean controls. Mutants cover all six spec-v1 finding IDs. Seed entries observed at `corpus/knowledge/claim-support-states-r24.md:1-7`, `citation-chain-fidelity-r24.md:1-7`, and `contextual-source-admission-r24.md:1-6`; contract read at `corpus/evidence/round25-claims.md:20-40`. `crlf.md` identified as `UTF-8 text ... with CRLF line terminators` by `file`. Fixture `wc -l` observations: README 35 lines; each fixture 5–9 lines (all below 40).

**Retained evidence:** The table is explicitly marked hand-derived and unexecuted. No gate/selftest/build/lint/formatter was run. No installs.

**Risks:** Expected classifications and exits remain unexercised until the metadata mode is integrated. **Blockers:** None.

**Clone files written (sha256):**
- `corpus/fixtures/metadata-r25/README.md` — `e03056e7756b0d8fe43a7a57a62255a581c32af3c6f70b3c96da23477bdff48a`
- `corpus/fixtures/metadata-r25/bom-first-line.md` — `81928a700fa6756d745ca5205366ae160fd5806235ae1b0bf06d69e12aa4d6a8`
- `corpus/fixtures/metadata-r25/bom-source-first-line.md` — `34f51202c01e4b5085104869c7872794154ccd27ed3f4240a8890aaeb37073d3`
- `corpus/fixtures/metadata-r25/command-only-recheck.md` — `5dbafc78d78096b2a0629ab94e0d99fa32925c1bff4d22ae5cb4dcad90cb9374`
- `corpus/fixtures/metadata-r25/control-citation-fidelity.md` — `8c36b034891ecca901863453a493efc1d98fc9483f3382be122f29fe9fa9ce07`
- `corpus/fixtures/metadata-r25/control-claim-support.md` — `7ea4e53fecea6c49f470d6387a1bdbc2d9598353b2a977164ba4179f03030dd6`
- `corpus/fixtures/metadata-r25/control-contextual-admission.md` — `e0e059e1126f08cd2863b1b2691b63f59dafa8b955bc4aa6959600d0748b48f4`
- `corpus/fixtures/metadata-r25/crlf.md` — `aef8eb1a92c4432a303dd2bd2bce1de558a330bfe7d4126234c86d1b6da23629`
- `corpus/fixtures/metadata-r25/empty-recheck.md` — `aeb21aea6e57bd636701cf0e09536a5a1f1fb9028d867960819974f36dda6aa4`
- `corpus/fixtures/metadata-r25/fenced-recheck.md` — `0e6d2dbf1080990ec66b4de8084f018f5687b8f82d50c65b834a5678edbf493e`
- `corpus/fixtures/metadata-r25/fenced-source.md` — `715ad074d1fcebb21eb1a1f6e7d10342b6957b1790a392d8709b303170aeb266`
- `corpus/fixtures/metadata-r25/indented-source.md` — `a3a0ca69eef8ace8450b7720f9174747a3d17ddb370315d910ddf48a04e58c8d`
- `corpus/fixtures/metadata-r25/indented-verified-at.md` — `cd0fd28fb1e1468ee0baa0fc288d2c01b38925511bb666612b7d5b9b103c6ca1`
- `corpus/fixtures/metadata-r25/malformed-source-key.md` — `4b804a5af8d1389c09d8e4b6b94634038292f3debc5af82967866d5bf98d28df`
- `corpus/fixtures/metadata-r25/missing-recheck.md` — `78d06a269da4751a1bf4e1f704d4c6e257e2db85c53751938d9611a322c92c86`
- `corpus/fixtures/metadata-r25/missing-source.md` — `5874cb706b8d965d2361bbd196a88ca083ad3b8195c4491f105dc955c575b44d`
- `corpus/fixtures/metadata-r25/missing-verified-at.md` — `c55b717c88bc1237ca249de88a6594c7903750028238e8b0c95dd5c9f14d5971`
- `corpus/fixtures/metadata-r25/recheck-90d.md` — `9fd9796a09ed9a96a08cb63294ebe8329b04c0c985ebcbf4229a6da574211d7d`
- `corpus/fixtures/metadata-r25/recheck-from-no-colon.md` — `609d857ab0bfe8fd0b2e68a70d2812ac5e7ef03d16c4c0aaa7227cd5489c83f0`
- `corpus/fixtures/metadata-r25/recheck-iso-date.md` — `575d89e3a1533046d7865996c2ca4e60abd409409ea3f894d62301d4612a6aa5`
- `corpus/fixtures/metadata-r25/recheck-on-release.md` — `da2a7cc7590ec54fd6a490c880d395c26a96ba49dd61bb3373cf1809f5834b96`
- `corpus/fixtures/metadata-r25/root-parent-recheck.md` — `143e363056c85e0196f80c02b55866f5d75b2e6585a6fe805668a01a68285ab3`
- `corpus/fixtures/metadata-r25/source-below-heading.md` — `88dbe371c8150d55434afdc7f03305e6c184588295f93c0f0c7b7de5383402e1`
- `corpus/fixtures/metadata-r25/source-continuation.md` — `ee32210762fcee5e7a1f8eaf35cf38228835917a86e788b05013749e26aedb5f`
- `corpus/fixtures/metadata-r25/undated-verified-at-slash.md` — `b0f97398bbb5cfaa3c2f2ed5c9563f55a5a30d4bbcc66bca56660a029a027c8f`
- `corpus/fixtures/metadata-r25/undated-verified-at.md` — `ecc50377c9db5a999ca2106a98d431b380358cd648f226e4a2e6bac781f79e0b`
- `corpus/fixtures/metadata-r25/unrecognized-recheck.md` — `98488fab0465c85ff6fa2d5233d9a2624dd87bbaebc7fa702248a226693eb771`
- `corpus/fixtures/metadata-r25/verified-at-below-heading.md` — `273cbf271b816f8389346e96ab4cc8b79d0525a95d7b5a477a3f985b28e1592a`

**VERDICT: Delivered the 18-mutant fixture set, six edge fixtures, three clean controls, hand-derived output contract, and file digests in the assigned private clone.**