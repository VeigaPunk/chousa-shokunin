import importlib.util, re, sys
spec = importlib.util.spec_from_file_location("qr", "/fast/scratch/hyaku/chousa-r30/w2/ReviewKnowledge30/clone/tools/quote-reopen.py")
qr = importlib.util.module_from_spec(spec); spec.loader.exec_module(qr)
P = "/fast/scratch/hyaku/chousa-r30/w2/ReviewKnowledge30/pages/"
pages = {k: qr.norm(qr.html_to_text(open(P + f, encoding="utf-8", errors="replace").read()))
         for k, f in [("w3", "S050_S051.html"), ("sock", "S052_S053.html"), ("http", "S054.html"),
                      ("ssl", "S055.html"), ("ip", "S056.html")]}
gate = [
    ("S050", "w3", "A head element’s end tag may be omitted if the head element is not immediately followed by a space character or a comment."),
    ("S051", "w3", "Pop the current node (which will be the head element) off the stack of open elements."),
    ("S052", "sock", "In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket."),
    ("S053", "sock", "it will try to resolve it for both AF_INET and AF_INET6, and then try to connect to all possible addresses in turn"),
    ("S054", "http", "blocking operations (like connection attempts) will timeout after that many seconds"),
    ("S055", "ssl", "pass server_hostname to wrap_socket() in order to match the hostname."),
    ("S056", "ip", "True if the address is defined as globally reachable by iana-ipv4-special-registry (for IPv4) or iana-ipv6-special-registry (for IPv6)"),
]
for sid, k, q in gate:
    print("GATE", sid, "VERBATIM" if qr.found(pages[k], q) else "ABSENT", len(q.split()), "words")

def ctx(k, pat, n=1, w=420):
    t = pages[k]
    for m in list(re.finditer(pat, t))[:n]:
        print("CTX", k, repr(pat), "::", t[max(0, m.start() - 80): m.start() + w])
    if not re.search(pat, t):
        print("CTX", k, repr(pat), ":: NOT FOUND")

ctx("w3", r"8\.2\.5\.4\.4\.? The \"in head\" insertion mode", 2, 200)
ctx("w3", r"A start tag whose tag name is \"head\" Parse error", 3, 200)
ctx("w3", r"An end tag whose tag name is one of: \"body\", \"html\", \"br\"", 2, 200)
ctx("w3", r"A start tag whose tag name is \"html\" Process the token using the rules for the \"in body\"", 2, 160)
ctx("w3", r"A head element’s end tag may be omitted", 1, 200)
ctx("sock", r"Notes on socket timeouts", 2, 900)
ctx("sock", r"sendall", 3, 500)
ctx("sock", r"socket\.create_connection\(", 1, 700)
ctx("http", r"class http\.client\.HTTPConnection\(", 1, 700)
ctx("ssl", r"server_hostname", 4, 300)
ctx("ip", r"is_global", 3, 500)
