"""Independent reader of the frozen Round 29 quote contract; stdlib only."""
from html.parser import HTMLParser
import re
import unicodedata


class ContractText(HTMLParser):
    omitted = frozenset("script style noscript template head".split())
    separated = frozenset(
        "p div li ul ol table tr td th h1 h2 h3 h4 h5 h6 br section article "
        "header footer nav pre blockquote dt dd dl figure figcaption hr main aside".split()
    )

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fragments = []
        self.hidden = []

    def handle_starttag(self, tag, attrs):
        if tag in self.omitted:
            self.hidden.append(tag)
        elif not self.hidden and tag in self.separated:
            self.fragments.append(" ")

    def handle_endtag(self, tag):
        if self.hidden:
            if tag in self.omitted and tag in self.hidden:
                pos = len(self.hidden) - 1 - self.hidden[::-1].index(tag)
                del self.hidden[pos:]
        elif tag in self.separated:
            self.fragments.append(" ")

    def handle_startendtag(self, tag, attrs):
        if not self.hidden and tag in self.separated:
            self.fragments.extend((" ", " "))

    def handle_data(self, data):
        if not self.hidden:
            self.fragments.append(data)


def normalize(value):
    translated = []
    for char in unicodedata.normalize("NFKC", value):
        point = ord(char)
        if point in (0xAD, 0x200B, 0x200C, 0x200D, 0xFEFF):
            continue
        if 0x2018 <= point <= 0x201B:
            char = "'"
        elif 0x201C <= point <= 0x201F:
            char = '"'
        translated.append(char)
    return " ".join("".join(translated).split())


def extract(document, content_type):
    if content_type == "text/plain":
        return normalize(document)
    parser = ContractText()
    parser.feed(document)
    parser.close()
    return normalize("".join(parser.fragments))


def present(page, quote):
    needle = normalize(quote)
    if not needle:
        return False
    for match in re.finditer("(?=" + re.escape(needle) + ")", page):
        left = match.start()
        right = left + len(needle)
        neighbors = page[left - 1:left] if left else ""
        neighbors += page[right:right + 1]
        if not any(char.isalnum() for char in neighbors):
            return True
    return False


def verdict(page, quote, has_source=True):
    if not has_source:
        return "NO_SOURCE"
    if len(normalize(quote).split()) > 25:
        return "TOO_LONG"
    if page is None:
        return "UNREACHABLE"
    return "VERBATIM" if present(page, quote) else "ABSENT"
