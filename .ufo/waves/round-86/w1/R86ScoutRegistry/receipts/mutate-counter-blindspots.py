#!/usr/bin/env python3
"""R86ScoutRegistry — read-only mutation battery on a SCRATCH copy of the landing tree.

Each mutation is applied to a copy of the corpus extracted from the landing revision
667a5d091dc46168ed95eda0ae7f19a9bcf139a2; the frozen counter
corpus/evidence/round86/curation-r86.py is then run against that copy.
Nothing under the lane repo is modified.
"""
import os, re, shutil, subprocess, sys

SRC = "/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry/corpus"   # landing tree, extracted
WORK = "/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry/mut"


def apply_mutation(w, mode):
    sp = os.path.join(w, "corpus/SOURCES.md")
    if mode == "M1_revert_S024_to_mined":
        t = open(sp, encoding="utf-8").read()
        t2 = t.replace("| A last-reviewed date for accuracy is a property separate from publication or modification dates | queued |",
                       "| A last-reviewed date for accuracy is a property separate from publication or modification dates | mined |")
        assert t2 != t, "M1 did not apply"
        open(sp, "w", encoding="utf-8").write(t2)
    elif mode == "M2_r85_entry_cites_S024":
        p = os.path.join(w, "corpus/knowledge/provenance-recording-r85.md")
        t = open(p, encoding="utf-8").read()
        t2 = t.replace("source: S215, S026, S031", "source: S215, S026, S024").replace("| Q7 | S031 |", "| Q7 | S024 |")
        assert t2 != t, "M2 did not apply"
        open(p, "w", encoding="utf-8").write(t2)
    elif mode == "M3_drop_supersedes_marker":
        t = open(sp, encoding="utf-8").read()
        t2 = t.replace("| supersedes S024 — lastReviewed records", "| lastReviewed records")
        assert t2 != t, "M3 did not apply"
        t2 = t2.replace("| A last-reviewed date for accuracy is a property separate from publication or modification dates | queued |",
                        "| A last-reviewed date for accuracy is a property separate from publication or modification dates | mined |")
        open(sp, "w", encoding="utf-8").write(t2)
    elif mode == "M4_reword_supersedes_marker":
        t = open(sp, encoding="utf-8").read()
        t2 = t.replace("| supersedes S024 — lastReviewed records", "| S024 is corrected here: lastReviewed records")
        assert t2 != t, "M4 did not apply"
        t2 = t2.replace("| A last-reviewed date for accuracy is a property separate from publication or modification dates | queued |",
                        "| A last-reviewed date for accuracy is a property separate from publication or modification dates | mined |")
        open(sp, "w", encoding="utf-8").write(t2)
    elif mode == "M5_drop_Q13_modified_definition":
        p = os.path.join(w, "corpus/knowledge/search-transparency-reporting-r84.md")
        t = open(p, encoding="utf-8").read()
        t2 = t.replace('| Q13 | S023 | "Date on which the resource was changed." |\n', "")
        assert t2 != t, "M5 did not apply"
        open(p, "w", encoding="utf-8").write(t2)
    elif mode == "M6_unentailed_modification_term":
        p = os.path.join(w, "corpus/knowledge/provenance-recording-r85.md")
        t = open(p, encoding="utf-8").read()
        t2 = t.replace("| record a review date for content that was not reviewed for accuracy or completeness |",
                        "| record a modification date for content that was not reviewed at all |")
        assert t2 != t, "M6 did not apply"
        open(p, "w", encoding="utf-8").write(t2)
    elif mode == "M7_r85_inversion_restored":
        t = open(sp, encoding="utf-8").read()
        t2 = t.replace("no comparison to other date properties claimed | mined |",
                       "no comparison to other date properties claimed | queued |")
        assert t2 != t, "M7 did not apply"
        t2 = t2.replace("| A last-reviewed date for accuracy is a property separate from publication or modification dates | queued |",
                        "| A last-reviewed date for accuracy is a property separate from publication or modification dates | mined |")
        open(sp, "w", encoding="utf-8").write(t2)
    else:
        raise SystemExit("unknown mode " + mode)


MODES = ["M1_revert_S024_to_mined", "M2_r85_entry_cites_S024", "M3_drop_supersedes_marker",
         "M4_reword_supersedes_marker", "M5_drop_Q13_modified_definition",
         "M6_unentailed_modification_term", "M7_r85_inversion_restored"]

if __name__ == "__main__":
    for mode in MODES:
        w = os.path.join(WORK, mode)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        shutil.copytree(SRC, os.path.join(w, "corpus"))
        apply_mutation(w, mode)
        counter = os.path.join(w, "corpus/evidence/round86/curation-r86.py")
        r = subprocess.run([sys.executable, "-B", counter, "--root", w], capture_output=True, text=True)
        print("=" * 78)
        print(mode)
        print("  stdout:", r.stdout.strip().replace("\n", " | "))
        print("  exit  :", r.returncode, "(0 = CURATION_R86=PASS, 1 = FAIL)")
