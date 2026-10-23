#!/usr/bin/env python3
"""Print the normalized reader-visible text of one HTML file.

Usage:
    python3 difftext.py FILE.html

Loads the sibling quote-reopen.py (this seat's independent implementation of
tool contract v2 item 1) and prints norm(html_to_text(file contents)) on one
logical line, so wave 2 can diff it against the landed tool's rendering of the
same document.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_tool():
    path = os.path.join(HERE, "quote-reopen.py")
    spec = importlib.util.spec_from_file_location("execb_quote_reopen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: difftext.py FILE.html\n")
        return 2
    with open(argv[1], encoding="utf-8", errors="replace") as f:
        doc = f.read()
    tool = _load_tool()
    print(tool.norm(tool.html_to_text(doc)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
