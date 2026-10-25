# The search log as a working document, not a field list

source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section 6, byte offset 17383 of the committed capture — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283
verified-at: 2026-10-24
recheck: 365d
ground: the lane held no opened source for how a search log is kept. `verify-sweeps` re-runs a location set. It does not keep a log document, and it does not check recall against included references. This entry is that missing half. The filename is the package's label, not a lane round number.

#### Observation

- The method says to design the complete search strategies "in a log document, instead of directly in the database itself, to register the steps taken and to make searches accountable and reproducible" (S078, capture byte offset 17383).
- It says "Any change to the search strategy should be done in the log document" (S078, the same capture).
- It says "checking searches for their recall is advised" (S078, the same capture).

#### Inference

- A search log this lane can re-run has to be a document the searcher controls, updated in that document, and then checked for recall against the review's own included references. A location-set replay is not that document.
- The 1/2 bound used by round 43's absent-class split is not this source's rule. This source says nothing about quote overlap.

#### Unknown

- Whether the recall check can be executed on a database this lane is not approved to query. The fetch-scope ruling is open. This entry does not fetch.

#### Gate

Located quote (12 words), access 2026-10-24, no fetch: "to register the steps taken and to make searches accountable and reproducible."
Capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt` is sha256 of the URL, first 24 hex digits; the file sha256 is `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`.
The staged citation id was S118. The lane id is S078 because the URL is the evidence and S078 is the next free lane id. Staged S077 stays the PRISMA-S DOI and is not this row. Lane S077 stays the pdftotext manual.
