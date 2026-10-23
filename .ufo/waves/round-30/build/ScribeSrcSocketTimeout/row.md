| S0NN | Python socket documentation — https://docs.python.org/3/library/socket.html#socket-timeouts | docs | A | Python timeout-mode semantics for blocking socket operations; not a total fetch-deadline guarantee | Python 3.15.1 documentation, section “Notes on socket timeouts”, opened 2026-10-23 | [INFERENCE] A socket timeout bounds an individual blocking operation; a separate elapsed-time deadline is needed to bound a sequence of operations | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |

Located quote (17 words), section “Notes on socket timeouts”: “In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket.”

Supports C2, tool contract v2 item 2 (total deadline), as the per-operation timeout semantics behind the slow-drip T4 finding. The quoted passage does not itself specify the tool’s total-deadline policy.
