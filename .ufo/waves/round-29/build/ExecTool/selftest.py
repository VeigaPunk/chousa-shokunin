#!/usr/bin/env python3
"""Self-test of tools/quote-reopen.py against the frozen tool contract.

Offline checks (no network) plus one live registry fetch.
Run from the lane root:  python3 ../selftest.py
"""
import importlib.util
import io
import os
import sys
import unittest
import urllib.error

LANE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(LANE, "tools", "quote-reopen.py")
spec = importlib.util.spec_from_file_location("qr", TOOL)
qr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qr)


class TestNormalization(unittest.TestCase):
    def test_nfkc_and_quote_folding(self):
        self.assertEqual(qr.norm("ﬁle"), "file")
        self.assertEqual(qr.norm("it’s"), "it's")
        self.assertEqual(qr.norm("“q”"), '"q"')
        self.assertEqual(qr.norm("‚x‛"), "'x'")
        self.assertEqual(qr.norm("„x‟"), '"x"')

    def test_soft_and_zero_width_removed(self):
        self.assertEqual(qr.norm("a­b"), "ab")
        self.assertEqual(qr.norm("ab"), "ab")
        self.assertEqual(qr.norm("a‌b"), "ab")
        self.assertEqual(qr.norm("a‍b"), "ab")
        self.assertEqual(qr.norm("a﻿b"), "ab")

    def test_whitespace_collapse_and_strip(self):
        self.assertEqual(qr.norm("  a \t\n b  "), "a b")

    def test_order_is_nfkc_first(self):
        # NFKC maps the fullwidth form to ASCII before the quote map applies.
        self.assertEqual(qr.norm("＇"), "'")


class TestHtmlToText(unittest.TestCase):
    def test_script_style_noscript_template_head_dropped(self):
        doc = ("<html><head><title>T</title><style>p{}</style></head>"
               "<body><script>var x=1;</script><noscript>ns</noscript>"
               "<template>tpl</template><p>kept</p></body></html>")
        text = qr.html_to_text(doc)
        self.assertNotIn("var x", text)
        self.assertNotIn("p{}", text)
        self.assertNotIn("ns", text)
        self.assertNotIn("tpl", text)
        self.assertNotIn("T", text)
        self.assertIn("kept", text)

    def test_block_elements_emit_spaces(self):
        self.assertEqual(qr.html_to_text("<p>a</p><p>b</p>").split(), ["a", "b"])
        self.assertEqual(qr.html_to_text("<div>x</div>").split(), ["x"])
        self.assertEqual(qr.html_to_text("<ul><li>one</li><li>two</li></ul>").split(), ["one", "two"])

    def test_inline_elements_emit_nothing(self):
        self.assertEqual(qr.html_to_text("<span>a</span><em>b</em>"), "ab")

    def test_comments_dropped(self):
        self.assertEqual(qr.html_to_text("a<!-- hidden -->b"), "ab")

    def test_charrefs_decoded(self):
        self.assertEqual(qr.html_to_text("a &amp; b &#8212; c"), "a & b — c")

    def test_self_closing_block(self):
        self.assertEqual(qr.html_to_text("a<br/>b").split(), ["a", "b"])


class TestFound(unittest.TestCase):
    def test_boundary_rule_rejects_alnum_neighbours(self):
        self.assertFalse(qr.found("xabc", "abc"))
        self.assertFalse(qr.found("abcx", "abc"))
        self.assertTrue(qr.found("x abc", "abc"))
        self.assertTrue(qr.found("abc x", "abc"))
        self.assertTrue(qr.found("(abc)", "abc"))

    def test_case_sensitive(self):
        self.assertFalse(qr.found("Hello world", "hello world"))
        self.assertTrue(qr.found("Hello world", "Hello world"))

    def test_normalizes_both_sides(self):
        # `found` takes the already-normalized page text, as the contract states.
        self.assertTrue(qr.found(qr.norm("it’s fine"), "it's fine"))
        self.assertTrue(qr.found(qr.norm("it’s fine"), "it’s fine"))
        self.assertTrue(qr.found(qr.norm("a﻿b"), "ab"))


class TestRegistry(unittest.TestCase):
    def test_url_extraction_and_stripping(self):
        self.assertEqual(qr.registry_url("Title — https://example.org/a."), "https://example.org/a")
        self.assertEqual(qr.registry_url("Title — https://example.org/a)"), "https://example.org/a")
        self.assertEqual(qr.registry_url("no url here"), None)
        self.assertEqual(qr.registry_url("ftp://example.org/x"), None)

    def test_rows_from_lane_registry(self):
        rows = qr.registry_rows(os.path.join(LANE, "corpus", "SOURCES.md"))
        self.assertIn("S002", rows)
        self.assertIn("S044", rows)
        self.assertTrue(qr.registry_url(rows["S044"]).startswith("https://docs.python.org/3/library/os.path"))
        self.assertIsNone(qr.registry_url(rows["S001"]))


class TestFetch(unittest.TestCase):
    def test_gzip_decoded(self):
        import gzip as gz
        chunks = [gz.compress(b"hello gzip body")]
        data, over = qr._inflate_stream(chunks, "gzip")
        self.assertEqual(data, b"hello gzip body")
        self.assertFalse(over)

    def test_plain_body(self):
        data, over = qr._inflate_stream([b"plain"], None)
        self.assertEqual(data, b"plain")
        self.assertFalse(over)

    def test_inflated_cap_is_bounded(self):
        import gzip as gz
        bomb = gz.compress(b"A" * (64 * 1024 * 1024))
        data, over = qr._inflate_stream([bomb], "gzip")
        self.assertTrue(over)
        self.assertLessEqual(len(data), qr.MAX_BODY + 1)

    def test_wire_cap_is_bounded(self):
        class _Resp:
            def __init__(self):
                self.sent = 0

            def read(self, n):
                self.sent += n
                return b"A" * n

        chunks, over = qr._read_response(_Resp(), float("inf"))
        self.assertTrue(over)
        self.assertLessEqual(sum(len(c) for c in chunks), qr.MAX_BODY + qr.CHUNK)


class TestFetchBounds(unittest.TestCase):
    """Sentinel findings T1, T2, T6."""

    def test_non_http_scheme_refused(self):
        for url in ("ftp://example.org/x", "file:///etc/hostname", "data:text/plain,hello"):
            with self.assertRaises(qr._Refuse):
                qr._check_url(url)

    def test_userinfo_refused(self):
        with self.assertRaises(qr._Refuse):
            qr._check_url("https://alice:s3cr3t@example.invalid/x")

    def test_loopback_and_private_addresses_refused(self):
        for host in ("127.0.0.1", "10.0.0.1", "192.168.1.1", "169.254.169.254", "::1"):
            with self.assertRaises(qr._Refuse):
                qr._check_address(host, 80)

    def test_global_address_accepted(self):
        qr._check_address("8.8.8.8", 443)

    def test_refusal_reason_holds_no_url(self):
        try:
            qr._check_url("https://alice:s3cr3t@example.invalid/x")
        except qr._Refuse as e:
            self.assertNotIn("s3cr3t", e.reason)
            self.assertNotIn("alice", e.reason)
        else:
            self.fail("expected a refusal")


class TestNoEcho(unittest.TestCase):
    """T6: a failure detail must not carry the URL or credential material."""

    def test_detail_is_a_reason_class_only(self):
        status, ctype, text, detail = qr.fetch_page("https://alice:s3cr3t@example.invalid/x")
        self.assertIsNone(text)
        self.assertEqual(status, None)
        self.assertNotIn("s3cr3t", detail)
        self.assertNotIn("example.invalid", detail)


class TestVerdictOrder(unittest.TestCase):
    """NO_SOURCE outranks TOO_LONG, which outranks the page verdicts."""

    def setUp(self):
        self.tmp = os.path.join(LANE, ".selftest-tmp")
        os.makedirs(self.tmp, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.tmp):
            os.remove(os.path.join(self.tmp, f))
        os.rmdir(self.tmp)

    def test_no_source_beats_too_long(self):
        p = os.path.join(self.tmp, "items.tsv")
        long_quote = " ".join(["word"] * 40)
        with open(p, "w", encoding="utf-8") as f:
            f.write("id\tsource_id\tquote\n")
            f.write("x1\tS999\t%s\n" % long_quote)
            f.write("x2\tS001\t%s\n" % long_quote)
        rc = qr.main(["verify", "--items", p])
        self.assertEqual(rc, 1)

    def test_bad_header_is_usage_error(self):
        p = os.path.join(self.tmp, "bad.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("wrong\theader\n")
        self.assertEqual(qr.main(["verify", "--items", p]), 2)

    def test_missing_items_file_is_io_error(self):
        self.assertEqual(qr.main(["verify", "--items", os.path.join(self.tmp, "nope.tsv")]), 2)

    def test_no_subcommand_is_usage_error(self):
        self.assertEqual(qr.main([]), 2)


class TestLive(unittest.TestCase):
    """One live fetch through the registry, if the network allows it."""

    def test_registry_url_fetches(self):
        rows = qr.registry_rows(os.path.join(LANE, "corpus", "SOURCES.md"))
        url = qr.registry_url(rows["S044"])
        status, ctype, text, detail = qr.fetch_page(url)
        if text is None:
            self.skipTest("network unavailable: %s" % detail)
        self.assertEqual(status, 200)
        self.assertEqual(ctype, "text/html")
        self.assertIn("commonpath", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
