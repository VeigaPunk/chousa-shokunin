"""Contract-literal model of corpus/evidence/round29/claims.md (design v2, tool contract).

Every rule here is transcribed from the frozen contract text in
corpus/evidence/round29/claims.md, section "Tool contract (frozen)".
This module is an INDEPENDENT implementation used only as the oracle of a
differential audit against the counter's reference functions. It never reads
or writes lane state.

All special characters are written as explicit escapes: a literal U+200B or
U+FEFF can be silently lost when a source file is written, which would
fabricate a divergence.

Contract clauses implemented (quoted from claims.md):

  "HTML to text: Python `html.parser` semantics with character references
   decoded. The content of `script`, `style`, `noscript`, `template` and `head`
   is dropped, and comments are dropped. Exactly these block-level elements
   emit one space at start and end (v2 fixes this list; v1 said "at least"):
   `p div li ul ol table tr td th h1 h2 h3 h4 h5 h6 br section article header
   footer nav pre blockquote dt dd dl figure figcaption hr main aside`. Every
   other element emits nothing."

  "Normalization, applied to page text and quote alike: Unicode NFKC; U+2018,
   U+2019, U+201A and U+201B become `'`; U+201C, U+201D, U+201E and U+201F
   become `"`; U+00AD, U+200B, U+200C, U+200D and U+FEFF are deleted; every
   whitespace run (Python `str.split()`) becomes one space; ends are stripped."

  "Match: `VERBATIM` iff the normalized quote occurs in the normalized page text
   at an offset where the character before it (if any) and the character after
   it (if any) are not alphanumeric (`str.isalnum`). Matching is case-sensitive."

  "1. `NO_SOURCE`: the id is not a registry row, or the row's `source` cell has
      no `http://` or `https://` URL. The tool uses the first URL in the cell and
      strips trailing `.,;)` characters."

  "3. `UNREACHABLE`: the fetch failed, the final status is not 2xx, the content
      type is not `text/html`, `application/xhtml+xml` or `text/plain`, or the
      body is over 8 MiB."

  "- Fetch bounds: the tool fetches only registry URLs, with GET only, the
      fragment removed, http and https only (redirects too), a 30 s timeout, one
      retry, no cookies or credentials, and each URL at most once per run."
"""
import re
import unicodedata
import zlib
from html.parser import HTMLParser

# Contract: "Exactly these block-level elements emit one space at start and end"
CONTRACT_BLOCK = {
    "p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
    "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
    "figure", "figcaption", "hr", "main", "aside",
}

# Contract: "The content of `script`, `style`, `noscript`, `template` and `head` is dropped"
CONTRACT_SKIP = {"script", "style", "noscript", "template", "head"}

# Contract quote map: U+2018/2019/201A/201B -> "'", U+201C/201D/201E/201F -> '"'
CONTRACT_QUOTE_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
}
# Contract deletions: U+00AD, U+200B, U+200C, U+200D, U+FEFF
# built with chr() so that no literal special character has to survive a
# file write (a literal U+200B is silently dropped by the write path)
CONTRACT_DELETED = {chr(c) for c in (0x00AD, 0x200B, 0x200C, 0x200D, 0xFEFF)}

MAX_BODY = 8 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"text/html", "application/xhtml+xml", "text/plain"}
FETCH_TIMEOUT_S = 30


def contract_norm(s):
    """Normalization applied to page text and quote alike (contract order)."""
    s = unicodedata.normalize("NFKC", s)
    s = "".join(CONTRACT_QUOTE_MAP.get(ch, ch) for ch in s)
    s = "".join(ch for ch in s if ch not in CONTRACT_DELETED)
    return " ".join(s.split())


class ContractText(HTMLParser):
    """Contract-literal HTML to text.

    Reading of the contract: the content of a skipped element is dropped, so
    nothing at all is emitted for it, including the one space a nested
    block-level element would otherwise contribute.

    Skip regions are tracked on a stack: an end tag closes only the element it
    matches, and a raw-text element such as `script` does not self-close, so
    `<script/>` still opens a region that runs to `</script>`.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []

    @property
    def skip(self):
        return len(self.stack)

    def handle_starttag(self, tag, attrs):
        if tag in CONTRACT_SKIP:
            self.stack.append(tag)
            return
        if self.skip:
            return
        if tag in CONTRACT_BLOCK:
            self.out.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag in CONTRACT_SKIP:
            # script/style are raw-text elements: `<script/>` does not close
            # them, the region runs to the matching end tag
            self.stack.append(tag)
            return
        if self.skip:
            return
        if tag in CONTRACT_BLOCK:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in CONTRACT_SKIP:
            if tag in self.stack:
                # close the matching region and any regions opened inside it
                while self.stack:
                    top = self.stack.pop()
                    if top == tag:
                        break
            return
        if self.skip:
            return
        if tag in CONTRACT_BLOCK:
            self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_comment(self, data):
        pass  # contract: "comments are dropped"


def contract_html_to_text(doc):
    p = ContractText()
    p.feed(doc)
    p.close()
    return "".join(p.out)


def contract_found(page_text, quote):
    """Contract match rule; page_text is expected already normalized."""
    q = contract_norm(quote)
    if not q:
        return False
    i = 0
    while True:
        i = page_text.find(q, i)
        if i < 0:
            return False
        j = i + len(q)
        before_ok = i == 0 or not page_text[i - 1].isalnum()
        after_ok = j == len(page_text) or not page_text[j].isalnum()
        if before_ok and after_ok:
            return True
        i += 1


def contract_registry_url(line):
    """Contract NO_SOURCE rule for one registry line.

    "the id is not a registry row, or the row's `source` cell has no `http://`
    or `https://` URL. The tool uses the first URL in the cell and strips
    trailing `.,;)` characters."
    """
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 2:
        return None
    source_cell = cells[1]
    m = re.search(r"https?://\S+", source_cell)
    if not m:
        return None
    return m.group(0).rstrip(".,;)")


def contract_body_decoding(enc, body):
    """Contract does not name compression; a conformant reader must still read
    what a server sends.  Raw DEFLATE (no zlib header) is accepted here."""
    enc = (enc or "").lower().strip()
    if enc == "gzip":
        import gzip
        return gzip.decompress(body)
    if enc == "deflate":
        try:
            return zlib.decompress(body)
        except zlib.error:
            return zlib.decompress(body, -zlib.MAX_WBITS)
    return body
