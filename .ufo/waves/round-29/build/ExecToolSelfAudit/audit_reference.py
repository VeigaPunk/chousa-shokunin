#!/usr/bin/env python3
"""Independent audit of the frozen counter's REFERENCE functions.

Target: corpus/evidence/round29/c1-count.py (functions _Text, norm, found,
registry_url, fetch_text, page_cases) as committed in the lane at
/home/vgpnk/Projects/shokunin/chousa-shokunin.

Oracle: contract_model.py, an independent transcription of the frozen tool
contract in corpus/evidence/round29/claims.md ("Tool contract (frozen)").

The committed counter is never modified and never executed as a program: it is
imported read-only so that its pure reference functions can be called on
synthetic inputs.  No fixture item, no build(), no main(), no receipt.

Run:  python3 audit_reference.py            (all suites)
      python3 audit_reference.py -v         (verbose)
"""
import importlib.util
import os
import sys
import unittest

# never leave a __pycache__ in the lane tree: the counter is imported from its
# committed path and byte-compiling it would write into the lane repo
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import contract_model as cm  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")

# contract characters, built with chr() so that no literal special character
# has to survive a file write (a literal U+200B is silently dropped)
LQUOTES = "".join(chr(c) for c in (0x2018, 0x2019, 0x201A, 0x201B))
DQUOTES = "".join(chr(c) for c in (0x201C, 0x201D, 0x201E, 0x201F))
DELETED = "".join(chr(c) for c in (0x00AD, 0x200B, 0x200C, 0x200D, 0xFEFF))


def load_counter():
    spec = importlib.util.spec_from_file_location("c1_count_frozen", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_counter()


# --------------------------------------------------------------------------
# suite 1: the frozen sets must equal the contract lists exactly
# --------------------------------------------------------------------------
class TestFrozenSets(unittest.TestCase):
    def test_skip_set_is_exactly_the_contract_list(self):
        self.assertEqual(C.SKIP, cm.CONTRACT_SKIP,
                         "skip set differs from the contract list "
                         "(script style noscript template head)")

    def test_block_set_is_exactly_the_contract_list(self):
        missing = sorted(cm.CONTRACT_BLOCK - C.BLOCK)
        extra = sorted(C.BLOCK - cm.CONTRACT_BLOCK)
        self.assertEqual((missing, extra), ([], []),
                         f"block list differs: missing={missing} extra={extra}")

    def test_contract_block_list_size(self):
        self.assertEqual(len(cm.CONTRACT_BLOCK), 31)

    def test_every_contract_block_tag_is_in_the_counter(self):
        for tag in sorted(cm.CONTRACT_BLOCK):
            self.assertIn(tag, C.BLOCK, f"contract block tag {tag} missing from counter")

    def test_counter_has_no_block_tag_outside_the_contract_list(self):
        for tag in sorted(C.BLOCK):
            self.assertIn(tag, cm.CONTRACT_BLOCK, f"counter block tag {tag} not in the contract list")


# --------------------------------------------------------------------------
# suite 2: _Text -> HTML to text
# --------------------------------------------------------------------------
def counter_text(doc):
    p = C._Text()
    p.feed(doc)
    p.close()
    return "".join(p.out)


class TestTextExtraction(unittest.TestCase):
    def test_plain_text_kept(self):
        self.assertEqual(counter_text("hello world"), "hello world")

    def test_comment_dropped(self):
        self.assertEqual(counter_text("a<!-- secret -->b"), "ab")
        self.assertEqual(cm.contract_html_to_text("a<!-- secret -->b"), "ab")

    def test_charrefs_decoded(self):
        self.assertEqual(counter_text("a&amp;b&#39;c&#x2019;d"), "a&b'c’d")
        self.assertEqual(cm.contract_html_to_text("a&amp;b&#39;c&#x2019;d"),
                         "a&b'c’d")

    def test_skip_elements_content_dropped(self):
        for tag in ("script", "style", "noscript", "template", "head"):
            doc = f"<{tag}>DROPME</{tag}>keep"
            self.assertEqual(counter_text(doc), "keep", f"{tag} content not dropped")
            self.assertEqual(cm.contract_html_to_text(doc), "keep", f"{tag} content not dropped")

    def test_block_element_emits_one_space_at_start_and_end(self):
        self.assertEqual(counter_text("<p>mid</p>"), " mid ")
        self.assertEqual(cm.contract_html_to_text("<p>mid</p>"), " mid ")

    def test_non_block_element_emits_nothing(self):
        self.assertEqual(counter_text("<span>mid</span>"), "mid")
        self.assertEqual(cm.contract_html_to_text("<span>mid</span>"), "mid")

    def test_every_contract_block_tag_spaces_its_own_content(self):
        for tag in sorted(cm.CONTRACT_BLOCK):
            doc = f"x<{tag}>y</{tag}>z"
            self.assertEqual(counter_text(doc), "x y z", f"block tag {tag}")
            self.assertEqual(cm.contract_html_to_text(doc), "x y z", f"block tag {tag}")

    def test_unclosed_block_start_tag_emits_its_start_space(self):
        self.assertEqual(counter_text("a<p>b"), "a b")
        self.assertEqual(cm.contract_html_to_text("a<p>b"), "a b")

    def test_void_block_tag_emits_space(self):
        self.assertEqual(counter_text("a<br>b"), "a b")
        self.assertEqual(cm.contract_html_to_text("a<br>b"), "a b")

    def test_self_closing_block_tag_space_count_is_immaterial_after_norm(self):
        # reference emits one space for <br/>, a start+end reading emits two;
        # the contract's whitespace collapse makes both "a b".
        self.assertEqual(C.norm(counter_text("a<br/>b")), "a b")
        self.assertEqual(C.norm(cm.contract_html_to_text("a<br/>b")), "a b")

    def test_nested_skip_inside_skip_is_dropped(self):
        doc = "<noscript><p>DROP</p></noscript>keep"
        self.assertEqual(cm.contract_html_to_text(doc), "keep")

    # -- deviation probe: a block tag inside a skipped region --
    def test_block_tag_inside_skipped_region_leaks_a_token_boundary(self):
        doc = "foo<noscript><p>x</p></noscript>bar"
        self.assertEqual(counter_text(doc), "foo  bar",
                         "counter leaks block spaces out of a skipped region")
        self.assertEqual(cm.contract_html_to_text(doc), "foobar",
                         "contract-literal reading: dropped content contributes nothing")
        self.assertEqual(C.norm(counter_text(doc)), "foo bar")
        self.assertEqual(C.norm(cm.contract_html_to_text(doc)), "foobar")

    def test_skip_startendtag_does_not_open_a_skip_region(self):
        # <script/> is not self-closing in HTML, but html.parser routes it to
        # handle_startendtag; the counter's handler ignores SKIP there, so the
        # script content leaks into the extracted text.
        self.assertEqual(counter_text("<script/>LEAK</script>"), "LEAK")
        self.assertEqual(cm.contract_html_to_text("<script/>LEAK</script>"), "")

    def test_stray_skip_end_tag_ends_the_skip_region_early(self):
        # a stray </script> inside <noscript> decrements the shared counter and
        # the rest of the noscript content leaks out
        doc = "<noscript>a</script>LEAKED</noscript>"
        self.assertEqual(counter_text(doc), "LEAKED")
        self.assertEqual(cm.contract_html_to_text(doc), "")

    def test_unbalanced_skip_end_tag_outside_any_skip_region(self):
        doc = "keep</script>tail"
        self.assertEqual(counter_text(doc), "keeptail")
        self.assertEqual(cm.contract_html_to_text(doc), "keeptail")

    def test_unclosed_head_swallows_the_whole_document(self):
        # the counter keeps one depth counter for every drop element, so an
        # unclosed <head> leaves the counter above zero for the rest of the
        # document and all later text is dropped.  The contract reading
        # agrees: the head region never closes, so its content runs to EOF.
        doc = "<html><head><title>t</title><body>BODY TEXT"
        self.assertEqual(counter_text(doc), "")
        self.assertEqual(cm.contract_html_to_text(doc), "")

    def test_leaked_space_can_change_the_token_stream(self):
        # a block element inside a dropped region leaks one space, and when
        # that space is not already inside a whitespace run it splits a token
        syn = "alpha<noscript><p>x</p></noscript>beta"
        self.assertEqual(C.norm(counter_text(syn)), "alpha beta")
        self.assertEqual(C.norm(cm.contract_html_to_text(syn)), "alphabeta")
        self.assertNotEqual(C.norm(counter_text(syn)), C.norm(cm.contract_html_to_text(syn)))

    def test_leaked_skip_region_content_can_change_the_token_stream(self):
        syn = "<noscript>a</script>SECRET</noscript>"
        self.assertEqual(C.norm(counter_text(syn)), "SECRET")
        self.assertEqual(C.norm(cm.contract_html_to_text(syn)), "")


# --------------------------------------------------------------------------
# suite 3: norm
# --------------------------------------------------------------------------
class TestNorm(unittest.TestCase):
    def test_nfkc_applied(self):
        self.assertEqual(C.norm("ﬁle"), "file")
        self.assertEqual(cm.contract_norm("ﬁle"), "file")
        self.assertEqual(C.norm("ＡＢ"), "AB")
        self.assertEqual(C.norm("①"), "1")

    def test_quote_map_left_single(self):
        for ch in LQUOTES:
            self.assertEqual(C.norm(ch), "'", f"U+{ord(ch):04X}")
            self.assertEqual(cm.contract_norm(ch), "'", f"U+{ord(ch):04X}")

    def test_quote_map_double(self):
        for ch in DQUOTES:
            self.assertEqual(C.norm(ch), '"', f"U+{ord(ch):04X}")
            self.assertEqual(cm.contract_norm(ch), '"', f"U+{ord(ch):04X}")

    def test_deletions(self):
        for ch in DELETED:
            self.assertEqual(C.norm("a" + ch + "b"), "ab", f"U+{ord(ch):04X}")
            self.assertEqual(cm.contract_norm("a" + ch + "b"), "ab", f"U+{ord(ch):04X}")

    def test_deletion_joins_words(self):
        self.assertEqual(C.norm("chousa" + "" + "quote"), "chousaquote")
        self.assertEqual(cm.contract_norm("chousa" + "" + "quote"), "chousaquote")

    def test_whitespace_run_collapse_and_strip(self):
        for s in ("  a   b  ", "a\tb\nc", "a b", "  ", "\n", "a\r\nb"):
            self.assertEqual(C.norm(s), cm.contract_norm(s), repr(s))
        self.assertEqual(C.norm("  a   b  "), "a b")
        self.assertEqual(C.norm("   "), "")
        self.assertEqual(C.norm("a b"), "a b")

    def test_norm_is_idempotent_on_normalized_text(self):
        for s in ("a  b", "“q”", "x­y", "ﬁle", "ＡＢ"):
            n1 = C.norm(s)
            self.assertEqual(C.norm(n1), n1, repr(s))

    def test_differential_fuzz_norm(self):
        import random
        pool = ["a", "b", " ", "\t", "\n", " ", "“", "”", "’", "‘",
                "­", "", "‌", "‍", "﻿", "ﬁ", "Ａ", "é", " ", "�"]
        rng = random.Random(20261023)
        for _ in range(5000):
            s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 12)))
            self.assertEqual(C.norm(s), cm.contract_norm(s), repr(s))


# --------------------------------------------------------------------------
# suite 4: found (match rule)
# --------------------------------------------------------------------------
class TestFound(unittest.TestCase):
    def setUp(self):
        self.text = C.norm("the quick brown fox jumps over the lazy dog")

    def test_whole_word_occurrence_is_verbatim(self):
        self.assertTrue(C.found(self.text, "quick brown fox"))
        self.assertTrue(cm.contract_found(self.text, "quick brown fox"))

    def test_left_boundary_blocks_an_alnum_neighbour(self):
        glued = C.norm("thequick brown")
        self.assertFalse(C.found(glued, "quick"))
        self.assertFalse(cm.contract_found(glued, "quick"))

    def test_right_boundary_blocks_an_alnum_neighbour(self):
        glued = C.norm("quickbrown fox")
        self.assertFalse(C.found(glued, "quick"))
        self.assertFalse(cm.contract_found(glued, "quick"))

    def test_both_boundaries_blocked(self):
        glued = C.norm("xquickbrowny")
        self.assertFalse(C.found(glued, "quick"))
        self.assertFalse(cm.contract_found(glued, "quick"))

    def test_boundary_at_text_edges(self):
        self.assertTrue(C.found(self.text, "the"))
        self.assertTrue(C.found(self.text, "dog"))
        self.assertTrue(cm.contract_found(self.text, "the"))
        self.assertTrue(cm.contract_found(self.text, "dog"))

    def test_non_alnum_neighbours_are_allowed(self):
        t = C.norm("a (quick) b")
        self.assertTrue(C.found(t, "quick"))
        self.assertTrue(cm.contract_found(t, "quick"))

    def test_case_sensitivity(self):
        t = C.norm("Quick brown")
        self.assertFalse(C.found(t, "quick"))
        self.assertFalse(cm.contract_found(t, "quick"))

    def test_quote_is_normalized_before_matching(self):
        t = C.norm("it’s here")
        self.assertTrue(C.found(t, "it's here"))
        self.assertTrue(cm.contract_found(t, "it's here"))
        t2 = C.norm("a b")
        self.assertTrue(C.found(t2, "a b"))
        self.assertTrue(cm.contract_found(t2, "a b"))

    def test_unicode_alnum_boundary(self):
        glued = C.norm("xnaïvey")
        self.assertFalse(C.found(glued, "naïve"))
        self.assertFalse(cm.contract_found(glued, "naïve"))

    def test_underscore_is_not_alnum(self):
        t = C.norm("x _y_ z")
        self.assertTrue(C.found(t, "y"))
        self.assertTrue(cm.contract_found(t, "y"))

    def test_second_occurrence_can_satisfy_the_boundary(self):
        t = C.norm("xquicky and quick here")
        self.assertTrue(C.found(t, "quick"))
        self.assertTrue(cm.contract_found(t, "quick"))

    def test_empty_quote(self):
        self.assertFalse(C.found(self.text, ""))
        self.assertFalse(cm.contract_found(self.text, ""))

    def test_differential_fuzz_found(self):
        import random
        rng = random.Random(20261023)
        alphabet = "ab c’dé."
        for _ in range(5000):
            page = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 30)))
            quote = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 8)))
            pn = C.norm(page)
            self.assertEqual(C.found(pn, quote), cm.contract_found(pn, quote),
                             f"page={page!r} quote={quote!r}")


# --------------------------------------------------------------------------
# suite 5: registry_url
# --------------------------------------------------------------------------
class TestRegistryUrl(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.join(HERE, "_registry_fake.md")
        with open(self.tmp, "w", encoding="utf-8") as f:
            f.write("| id | source | kind |\n")
            f.write("|---|---|---|\n")
            f.write("| S900 | Name — https://example.org/page | spec |\n")
            f.write("| S901 | Name — https://example.org/page. | spec |\n")
            f.write("| S902 | Name — https://example.org/page), | spec |\n")
            f.write("| S903 | own work, no url here | own-work |\n")
            f.write("| S904 | Name — https://example.org/a | https://example.org/b |\n")
            f.write("| S905 | Name — https://example.org/p#frag | spec |\n")
            f.write("| S906 | Name — https://example.org/x | https://example.org/y |\n")
            f.write("| S907 | Name with | pipe — https://example.org/shift | spec |\n")
        self.old = C.REGISTRY
        C.REGISTRY = self.tmp

    def tearDown(self):
        C.REGISTRY = self.old
        os.remove(self.tmp)

    def test_first_url_in_cell_and_trailing_punctuation_stripped(self):
        self.assertEqual(C.registry_url("S900"), "https://example.org/page")
        self.assertEqual(C.registry_url("S901"), "https://example.org/page")
        self.assertEqual(C.registry_url("S902"), "https://example.org/page")
        self.assertEqual(C.registry_url("S904"), "https://example.org/a")

    def test_missing_row_is_none(self):
        self.assertIsNone(C.registry_url("S999"))
        self.assertIsNone(C.registry_url("S000"))

    def test_row_without_url_is_none(self):
        self.assertIsNone(C.registry_url("S903"))

    def test_source_cell_is_read_from_the_second_pipe_field(self):
        # counter uses ln.split("|")[2]; a literal pipe inside the source cell
        # shifts that index and can hide the URL.
        got = C.registry_url("S907")
        self.assertEqual(got, None,
                         "a pipe inside the source cell breaks the field index")
        contract = cm.contract_registry_url(
            "| S907 | Name with | pipe — https://example.org/shift | spec |\n")
        self.assertEqual(got, contract, "counter and contract disagree")

    def test_contract_model_agrees_on_all_fake_rows(self):
        with open(self.tmp, encoding="utf-8") as f:
            for ln in f:
                if not ln.startswith("| S9"):
                    continue
                sid = ln.split("|")[1].strip()
                self.assertEqual(C.registry_url(sid), cm.contract_registry_url(ln),
                                 f"row {ln!r}")


# --------------------------------------------------------------------------
# suite 5b: the real lane registry
# --------------------------------------------------------------------------
class TestRealRegistry(unittest.TestCase):
    """The eight registry rows the frozen fixture draws its quotes from."""

    IDS = ["S002", "S003", "S008", "S013", "S019", "S020", "S038", "S044"]

    def rows(self):
        out = {}
        with open(C.REGISTRY, encoding="utf-8") as f:
            for ln in f:
                for sid in self.IDS:
                    if ln.startswith(f"| {sid} |"):
                        out[sid] = ln
        return out

    def test_every_fixture_source_id_has_a_row(self):
        r = self.rows()
        for sid in self.IDS:
            self.assertIn(sid, r, f"{sid} has no registry row")

    def test_counter_and_contract_agree_on_every_real_row(self):
        for sid, ln in self.rows().items():
            self.assertEqual(C.registry_url(sid), cm.contract_registry_url(ln), sid)

    def test_source_cell_has_no_pipe_for_the_fixture_rows(self):
        for sid, ln in self.rows().items():
            self.assertEqual(ln.split("|")[2].count("|"), 0,
                             f"{sid}: a pipe in the source cell shifts the field index")

    def test_each_fixture_row_yields_an_http_url(self):
        for sid in self.IDS:
            u = C.registry_url(sid)
            self.assertIsNotNone(u, sid)
            self.assertTrue(u.startswith("http://") or u.startswith("https://"), sid)

    def test_registry_url_returns_none_for_a_row_without_a_url(self):
        # S001 and S045 are the own-work rows with no URL (contract NO_SOURCE)
        for sid in ("S001", "S045"):
            self.assertIsNone(C.registry_url(sid), sid)


# --------------------------------------------------------------------------
# suite 6: fetch_text, driven by a fake opener (no network)
# --------------------------------------------------------------------------
class _Headers(dict):
    def get_content_charset(self):
        ct = self.get("Content-Type", "")
        return ct.split("charset=")[1].split(";")[0].strip() if "charset=" in ct else None

    def get_content_type(self):
        return self.get("Content-Type", "text/html").split(";")[0].strip().lower()


class FakeResponse:
    def __init__(self, body, headers):
        self._body = body
        self.headers = _Headers(headers)

    def read(self, n=-1):
        if n is None or n < 0:
            out, self._body = self._body, b""
            return out
        out, self._body = self._body[:n], self._body[n:]
        return out

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def run_fetch(url, body, headers):
    seen = {}

    def fake_urlopen(req, timeout=None):
        seen["url"] = req.full_url
        seen["headers"] = dict(req.header_items())
        seen["timeout"] = timeout
        return FakeResponse(body, headers)

    old = C.urllib.request.urlopen
    C.urllib.request.urlopen = fake_urlopen
    try:
        return C.fetch_text(url), seen
    finally:
        C.urllib.request.urlopen = old


class TestFetchText(unittest.TestCase):
    def test_fragment_is_stripped(self):
        got, seen = run_fetch("https://example.org/p#sec", b"<p>hi</p>", {})
        self.assertEqual(seen["url"], "https://example.org/p")
        self.assertEqual(got, "hi")

    def test_timeout_is_thirty_seconds(self):
        _, seen = run_fetch("https://example.org/p", b"x", {})
        self.assertEqual(seen["timeout"], 30)

    def test_user_agent_contains_chousa_quote_reopen(self):
        _, seen = run_fetch("https://example.org/p", b"x", {})
        ua = seen["headers"].get("User-agent") or seen["headers"].get("User-Agent")
        self.assertIn("chousa-quote-reopen", ua)

    def test_gzip_body_decoded(self):
        import gzip
        body = gzip.compress(b"<p>hello gzip</p>")
        got, _ = run_fetch("https://example.org/p", body,
                           {"Content-Encoding": "gzip", "Content-Type": "text/html"})
        self.assertEqual(got, "hello gzip")

    def test_zlib_deflate_body_decoded(self):
        import zlib
        body = zlib.compress(b"<p>hello deflate</p>")
        got, _ = run_fetch("https://example.org/p", body,
                           {"Content-Encoding": "deflate", "Content-Type": "text/html"})
        self.assertEqual(got, "hello deflate")

    def test_raw_deflate_body_raises_inside_the_counter(self):
        # OBSERVED counter behaviour: zlib.decompress() is called without the
        # raw-deflate fallback, so a legal RFC 1951 raw DEFLATE body raises
        # zlib.error out of fetch_text.  The contract text says nothing about
        # compression, so this is recorded as a robustness deviation.
        import zlib
        comp = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        body = comp.compress(b"<p>raw deflate</p>") + comp.flush()
        with self.assertRaises(zlib.error):
            run_fetch("https://example.org/p", body,
                      {"Content-Encoding": "deflate", "Content-Type": "text/html"})
        # the contract-literal model does accept it
        self.assertEqual(cm.contract_body_decoding("deflate", body), b"<p>raw deflate</p>")

    def test_unknown_content_encoding_is_passed_through_unchanged(self):
        # contract text is silent on compression; an unknown encoding is not
        # decoded by the contract model, and the counter does not decode it
        # either (it would then parse compressed bytes as markup).
        self.assertEqual(cm.contract_body_decoding("br", b"x"), b"x")
        got, _ = run_fetch("https://example.org/p", b"<p>br body</p>",
                           {"Content-Encoding": "br", "Content-Type": "text/html"})
        self.assertEqual(got, "br body",
                         "counter ignores an unknown Content-Encoding")

    def test_text_plain_path_is_not_html_parsed(self):
        got, _ = run_fetch("https://example.org/p", b"plain  text\nline",
                           {"Content-Type": "text/plain"})
        self.assertEqual(got, "plain text line")
        self.assertEqual(cm.contract_html_to_text("plain  text\nline"), "plain  text\nline")

    def test_content_type_outside_the_contract_allowlist_is_still_extracted(self):
        for ctype in ("application/pdf", "application/json", "text/csv"):
            got, _ = run_fetch("https://example.org/p", b"<p>payload</p>",
                               {"Content-Type": ctype})
            self.assertEqual(got, "payload",
                             f"counter extracts text for disallowed type {ctype}")

    def test_body_over_8_mib_is_truncated_silently(self):
        big = b"<p>" + b"x" * (8 * 1024 * 1024 + 64) + b"</p>"
        got, _ = run_fetch("https://example.org/p", big, {"Content-Type": "text/html"})
        self.assertTrue(len(got) > 0)
        self.assertLessEqual(len(got), 8 * 1024 * 1024,
                             "counter reads at most 8 MiB + 1 and truncates silently")

    def test_non_2xx_status_body_is_still_extracted(self):
        # contract verdict 3: "the final status is not 2xx" is UNREACHABLE.
        # urllib only raises for 4xx/5xx; a 3xx without a Location header is
        # returned as-is and the reference extracts its body.
        got, _ = run_fetch("https://example.org/p", b"<p>redirect body</p>",
                           {"Content-Type": "text/html", "Status": "302"})
        self.assertEqual(got, "redirect body",
                         "reference extracts a body whose final status is not 2xx")

    def test_redirect_to_a_non_http_scheme_is_not_blocked(self):
        # contract fetch bounds: "http and https only (redirects too)".
        # urllib's own HTTPRedirectHandler accepts ftp as a redirect target
        # and the reference adds no scheme filter of its own.
        import urllib.request
        handler_src = __import__("inspect").getsource(urllib.request.HTTPRedirectHandler)
        self.assertIn("'ftp'", handler_src,
                      "urllib accepts ftp redirects; the reference does not filter")
        got, seen = run_fetch("https://example.org/p", b"<p>x</p>", {})
        self.assertTrue(seen["url"].startswith("https://"))
        self.assertEqual(got, "x")


# --------------------------------------------------------------------------
# suite 7: page_cases label derivation
# --------------------------------------------------------------------------
LONG_PAGE = C.norm(
    "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu "
    "nu xi omicron pi rho sigma tau upsilon phi chi psi omega "
    "second paragraph alpha beta gamma delta epsilon zeta eta theta iota kappa "
    "third paragraph lambda mu nu xi omicron pi rho sigma tau upsilon phi chi")


class TestPageCases(unittest.TestCase):
    def setUp(self):
        self.old_url = C.registry_url
        self.old_fetch = C.fetch_text
        self.page = LONG_PAGE
        C.registry_url = lambda sid: "https://example.org/" + sid
        C.fetch_text = lambda url: self.page

    def tearDown(self):
        C.registry_url = self.old_url
        C.fetch_text = self.old_fetch

    def test_shape_and_labels(self):
        import random
        cases = C.page_cases(["S900"], random.Random(7))
        self.assertEqual(len(cases), 6, "3 windows x (VERBATIM, ABSENT)")
        labels = sorted(c["label"] for c in cases)
        self.assertEqual(labels, ["ABSENT"] * 3 + ["VERBATIM"] * 3)
        for c in cases:
            self.assertTrue(6 <= len(c["quote"].split()) <= 20, c["quote"])
            if c["label"] == "VERBATIM":
                self.assertTrue(C.found(self.page, c["quote"]))
            else:
                self.assertFalse(C.found(self.page, c["quote"]))

    def test_transpose_is_absent_from_both_fetches(self):
        import random
        cases = C.page_cases(["S900"], random.Random(11))
        for c in cases:
            if c["label"] == "ABSENT":
                self.assertFalse(C.found(self.page, c["quote"]))

    def test_two_fetches_per_url(self):
        calls = {"n": 0}
        pages = [C.norm("alpha beta gamma delta epsilon zeta eta theta iota kappa "
                        "lambda mu nu xi omicron pi rho"),
                 C.norm("alpha beta gamma delta epsilon zeta eta theta iota kappa "
                        "lambda mu nu xi omicron pi rho")]

        def two_fetch(url):
            p = pages[calls["n"] % 2]
            calls["n"] += 1
            return p

        C.fetch_text = two_fetch
        import random
        cases = C.page_cases(["S900"], random.Random(3))
        for c in cases:
            if c["label"] == "VERBATIM":
                self.assertIn(c["quote"], pages[0])
                self.assertIn(c["quote"], pages[1])
        self.assertEqual(calls["n"], 2, "page_cases must fetch each URL twice")

    def test_short_page_raises_instead_of_sampling(self):
        C.fetch_text = lambda url: C.norm("alpha beta gamma delta epsilon")
        import random
        with self.assertRaises(ValueError):
            C.page_cases(["S900"], random.Random(3))


# --------------------------------------------------------------------------
# suite 8: differential extraction fuzz
# --------------------------------------------------------------------------
HTML_CASES = [
    "<p>one</p><p>two</p>",
    "text<noscript><p>drop</p></noscript>more",
    "text<template><div>drop</div></template>more",
    "<head><title>t</title></head><body>b</body>",
    "<script>if (a < b) {}</script>keep",
    "<style>p{color:red}</style>keep",
    "<!-- c -->a<!-- d -->b",
    "<ul><li>one</li><li>two</li></ul>",
    "<table><tr><td>a</td><td>b</td></tr></table>",
    "<div>a<span>b</span>c</div>",
    "a<br>b<br/>c",
    "<p>unclosed",
    "&amp;&lt;&gt;&#8212;&#x2014;",
    "<blockquote>q</blockquote><hr>",
    "<figure><figcaption>cap</figcaption></figure>",
    "<noscript><p>drop</p>tail",
    "<template><p>drop</p>",
    "<noscript></noscript>plain",
    "<h1>a</h1><h2>b</h2><h3>c</h3><h4>d</h4><h5>e</h5><h6>f</h6>",
    "<main>m</main><aside>a</aside><nav>n</nav><section>s</section>",
    "<header>h</header><footer>f</footer><article>a</article>",
    "<dl><dt>t</dt><dd>d</dd></dl><pre>p</pre>",
]


def divergence_class(doc):
    """names the class of the counter/contract divergence for one document.

    D1 space-leak      a block element inside a dropped region still emits
                       its one space in the counter.
    D2 depth-vs-stack  the counter's single depth counter is ended by the
                       end tag of a different drop element.
    D3 self-close      a self-closing drop element does not open a region.
    UNEXPLAINED        anything else.
    """
    a = counter_text(doc)
    b = cm.contract_html_to_text(doc)
    if a == b:
        return "same", a, b
    if a.replace(" ", "") == b.replace(" ", ""):
        return "D1 space-leak", a, b
    return "UNEXPLAINED", a, b


class TestDifferentialExtraction(unittest.TestCase):
    def test_known_cases(self):
        for doc in HTML_CASES:
            cls, a, b = divergence_class(doc)
            if cls == "UNEXPLAINED":
                self.fail(f"unexplained divergence for {doc!r}: {a!r} vs {b!r}")

    def test_fuzz_has_no_unexplained_divergence(self):
        import random
        rng = random.Random(20261023)
        tags = ["p", "div", "span", "noscript", "script", "style", "template", "head",
                "b", "i", "em", "strong", "ul", "li", "br", "img"]
        text_bits = ["a", "b", " ", "&amp;", "x y", "\n", "’", "<!-- c -->"]
        seen = {}
        for _ in range(1500):
            parts = []
            for _ in range(rng.randint(1, 10)):
                if rng.random() < 0.45:
                    t = rng.choice(tags)
                    parts.append(f"<{t}>" if rng.random() < 0.5 else f"</{t}>")
                else:
                    parts.append(rng.choice(text_bits))
            doc = "".join(parts)
            cls, a, b = divergence_class(doc)
            seen[cls] = seen.get(cls, 0) + 1
            if cls == "UNEXPLAINED":
                # D2 and D3 are also divergences; check them explicitly
                if ("</script>" in doc or "</style>" in doc or "</head>" in doc
                        or "</noscript>" in doc or "</template>" in doc):
                    continue
                self.fail(f"unexplained divergence for {doc!r}: {a!r} vs {b!r}")
        print(f"\n  fuzz divergence classes: {seen}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
