# Validation log

Record each validation run here (see `validation-protocol.md`). Keep client names out if
the client has not agreed to be named; a site label such as "Site A (plumbing, UK)" is
enough.

## Status

**No validation run yet.** The skill was built and unit-tested in an environment whose
network policy blocked general web hosts, so it has not been run against real pages, and
the approval step needs a human reviewer in any case.

## Run template

```
### Run <n>: <date>

Rulebook version: 0.1.0
Agent and model: <agent, model>
Reviewer: <role, not necessarily name>
Pages: <count> (<types>), control page: <which>

Tally:
<paste tally.py table>

Rejected findings and why:
- <file> F<n> <pattern>: <reviewer note>

Missed tells the reviewer noticed:
- <page>: <passage> (<which pattern, or "not in batch">)

Regression cases: <passed>/<total>; failures: <ids>

Decision: <continue / tighten patterns X, Y / stop and fix>
```
