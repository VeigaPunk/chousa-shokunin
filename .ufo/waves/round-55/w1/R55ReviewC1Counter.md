# R55ReviewC1Counter — same-sentence audit

Scope: compare the frozen C1 sentence in `corpus/evidence/round55/claims.md:49-81`, the identical counter docstring (`c1-count.py:4-36`), with enforcement in that counter. This is a code/receipt review, not a run of the builder or counter. Commands below are observations; no new behavior is inferred from a check not run. No lane production file changed.

## Predicate clauses

| Clause | Assessment | Counter evidence |
|---|---|---|
| Ordinary builder command with `--quotes Q --out DIR --cache C` | Enforced as CLI invocation | `:188-196` creates TSV and invokes hook + tool with all three flags, cwd run directory. The full command text in claims uses `--quotes Q --out DIR --cache C`; argparse contract of the builder itself was not independently inspected in this seat. |
| Hook terminates on spawn/exec/fork/socket/connect/bind/ctypes library load, exit 97 | Partially enforced | Hook `:84-86` enumerates subprocess.Popen, os.system/exec/posix_spawn/spawn/fork/forkpty, pty.spawn, socket connect/bind, ctypes.dlopen/dlsym/cdata; `:88-90,101-105` writes denial and `_exit(97)`. This is a concrete list, not a proof every operation colloquially described as spawn/exec/fork is covered. |
| File open/listing/scan outside run, hook, tool dir, lane tools, Python installation denied | Partially enforced | Allow roots assembled `:191-196,407-413`; hook checks only audit event names `open`, `os.listdir`, `os.scandir` at `:87,104`, resolved path-prefix check `:91-100`. The hook itself/tool dir/tools/Python prefix roots correspond to sentence, but `sys.prefix`, `sys.base_prefix`, `sys.exec_prefix` can overlap/broaden roots; prefix matching is path-separator bounded. This audit does not establish coverage of every possible file access/scan operation. |
| Manifest header and one ordered row per quote row | Enforced by judge | `:243-250` requires exact header and expected row count; `:254-259` checks rows in zipped order and echoed values. |
| Span files exact slice of defined form, longer than quote, quote char position correct | Partially enforced | `:267-273` compares slice, length, and computed char. It only requires `span.find(quote) >= 0` and expected char; it does not require quote occurs exactly once in span. Predicate says the quote held at the computed position, not uniqueness within span. |
| Capture digest is digest of bytes read | Enforced for tested cases | `:260-261` compares manifest digest to SHA-256 of expected capture bytes held by counter; expectation sources are generated/pinned inputs. |
| Defined form: OLE/zip raw via capture-text; otherwise `.txt` universal newlines; never OLE sidecar | Partially enforced | Oracle form uses pinned capture-text subprocess `:141-145`; pinned case forms obtained there `:224-235`; expected checks use those forms (`:238-279`). Refusal tests exercise distinctions `:337-359`. Counter itself does not directly assert universal-newline semantics for non-OLE `.txt` input in the shown logic; tested main legs are OLE. |
| Print one `QUOTE <id> char <N> <span_file>` per row and exit 0 | Partially enforced | Judge checks each expected line is present `:274-275`, and successful builder rc `:241-242`; does not require stdout to contain exactly one such line per row or forbid additional lines. |
| Held-out generated OLE `.doc` from fresh random text, copied alone to keyed cache; generation tree deleted before run | Enforced for GENOLE construction | `:199-221` builds HTML source, LibreOffice docs and defined forms, deletes generation tree; `:282-297` places raw docs in run cache under random URL keys then invokes builder. |
| Four distinct pinned OLE captures, copied with sidecars under random URLs | Enforced | Pin validation `:224-235`; leg copies raw + optional sidecar under random URL key `:299-315`. Four pin constants are listed `:71-77`. |
| Expected offsets only in counter memory while builder runs | Enforced for expected offsets; not a claim that counter has no writes | `:238-240,269-273` expected tuples/char values are in process memory and used after subprocess returns. Writes in the counter (`:170-171,176,183-185,190,203,208-210,220,288,304-306,362-365,370,376-381,405-406,446,474`) create hook/run data, generated inputs, cache copies, and cleanup; no code writes expected offset values to a file. `:89` is hook diagnostic stderr, not an expected value. |
| REFUSE no-form raw whose quote only occurs UTF-16LE decode, no sidecar | Enforced case construction and refusal | `:337-344`, then common check `:373-387`; `refused_ok :318-328` checks rc=1/refusal/no outputs. |
| REFUSE quote absent from defined form, present exactly once in `.txt` sidecar | Enforced if qualifying window found | `:345-353` selects sidecar-only window; overall exact case list required `:371-372`. |
| REFUSE quote absent from defined form, present exactly once in raw UTF-16LE decode | Enforced if qualifying window found | `:354-359`; exact case list check `:371-372`. |
| REFUSE OLE file capture-text refuses (spreadsheet) | Enforced | CSV→OLE spreadsheet via private soffice profile (`:175-179,360-370`), then exact refusal case list and per-case result `:371-387`. |
| REFUSE emits `build-spans: refused <that id>`, rc=1, writes no manifest/span | Partially enforced | `:320-328` checks rc=1 and a stderr line with required prefix, checks no manifest and no nonempty spans directory. Prefix allows suffix text after id; empty spans directory allowed, consistent with no span file. |
| REGRESS reads round-54 quotes and spans at BASE and compares byte for byte | Enforced | `:391-398` uses `git show BASE_REV`; `:399-426` copies matching cache files, runs builder under hook, compares manifest and each named span bytes to BASE. |
| `--per-leg` default 3, minimum 2; reject smaller | Enforced | argparse/default and guard `:432-438`; default and minimum also documented `:43-46`. |
| ENV_CHANGED on oracle digest / pinned capture digest mismatch | Enforced | Oracle existence/hash check `:441-442`, `env_fail` exit 2 `:114-116`; each pin checks raw existence/hash prefix `:224-230`; generated and spreadsheet environmental failures likewise route through `env_fail` (`:213-218,366-372`). |

## Controls provenance

The receipts and driver are present in the freeze commit, checked directly with `git show <freeze>:<path> | sha256sum`:

```text
4d10dc029d1b1fca6db38b1bb9b29d4f6509abf496d7d0448ace247e0f03cc0f  controls/c1-before.txt
69f35b084e4a9026a2abe0eeabc2830c71794f107f4ecbdc358d14bfe2508c3f  controls/c1-controls.txt
a0df7c980cae749acaba2fda5468fe5a843724519ccf1f552ea801702865255f  controls/build-c1-controls.py
5506f240c53ff83c7c17b7252c7627871b4b1af7c1ca739b461fdbcc32048906  corpus/evidence/round55/c1-count.py
```

Receipt content: `controls/c1-before.txt:1-40` records BASE absence (`:2-4`) and seed 7 plus three unseeded failure receipts (`:5-40`). `controls/c1-controls.txt:1-28` records seed 55: r54shim 1/4, txtonly 1/4, delegate 0/4 and `AUDIT_FORBIDDEN ctypes.dlopen`. Driver `controls/build-c1-controls.py:2-12,23-43` describes/builds those three controls and their common CLI/output; `:74-86` contains txtonly/delegate implementations. Freeze-blob checks establish these exact receipt and driver bytes are in the specified freeze commit; they do not independently prove the historical commands were run exactly as labeled, beyond receipt contents.

## Residual risk / verification gaps

No LSP device/server was available among the provided devices, so caller/reference/definition/diagnostics requests could not be made; this review used the assigned frozen claim and targeted source reads. No counter or builder execution was performed, and no independent reproduction of historical control commands was attempted. The strongest actionable counter limitations are the hook's bounded audit-event list and the judge's non-exact stdout-line cardinality; noted partials are audit limitations, not changes proposed to the frozen predicate.

VERDICT: attacked the same-sentence C1 counter contract and frozen control provenance; core leg checks and byte-for-byte REGRESS are implemented, with hook-coverage and stdout-cardinality gaps recorded.