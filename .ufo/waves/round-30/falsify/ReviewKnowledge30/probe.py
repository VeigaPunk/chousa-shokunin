"""Offline probes of the landed tool (clone at a9d3a05): watchdog timing and TLS host check.
Loopback only. `_check_address` is replaced so loopback passes; everything after it is the landed code."""
import importlib.util, json, os, socket, ssl, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("qr", os.path.join(HERE, "clone/tools/quote-reopen.py"))
qr = importlib.util.module_from_spec(spec); spec.loader.exec_module(qr)
out = {}


def drip_server(host, port_holder, stop):
    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port_holder[0])); port_holder[0] = s.getsockname()[1]; s.listen(8); s.settimeout(0.2)
    def serve(c):
        try:
            c.recv(4096); c.sendall(b"HTTP/1.1 200 OK\r\nX-A: ")
            while not stop.is_set():
                c.sendall(b"a"); time.sleep(0.2)
        except OSError:
            pass
        finally:
            c.close()
    while not stop.is_set():
        try:
            c, _ = s.accept()
        except socket.timeout:
            continue
        threading.Thread(target=serve, args=(c,), daemon=True).start()
    s.close()


def blackhole(host, port):
    """A listener whose accept queue is full, so a further connect gets no SYN-ACK."""
    l = socket.socket(); l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    l.bind((host, port)); l.listen(0)
    fill = []
    for _ in range(4):
        c = socket.socket(); c.setblocking(False)
        try:
            c.connect((host, port))
        except BlockingIOError:
            pass
        fill.append(c)
    time.sleep(0.3)
    return l, fill


def timed(url, addrs, deadline):
    qr.DEADLINE = deadline
    qr._check_address = lambda h, p: list(addrs)
    t0 = time.monotonic(); r = qr.fetch_page(url); return round(time.monotonic() - t0, 3), r[3]


stop = threading.Event(); ph = [0]
threading.Thread(target=drip_server, args=("127.0.0.1", ph, stop), daemon=True).start()
time.sleep(0.3); port = ph[0]
bh = blackhole("127.0.0.2", port)
# control: the black hole really holds a connect
c = socket.socket(); c.settimeout(1.0); t0 = time.monotonic()
try:
    c.connect(("127.0.0.2", port)); bh_ctl = "connected"
except OSError as e:
    bh_ctl = type(e).__name__
out["blackhole_control"] = [bh_ctl, round(time.monotonic() - t0, 3)]
c.close()
for D in (3.0, 4.0):
    out["drip_one_addr_D%.0f" % D] = timed("http://h.test:%d/" % port, ["127.0.0.1"], D)
    out["drip_blackhole_then_good_D%.0f" % D] = timed("http://h.test:%d/" % port, ["127.0.0.2", "127.0.0.1"], D)
stop.set()

# TLS: throwaway CA via SSL_CERT_FILE (read by create_default_context), cert for good.test only.
ca = os.path.join(HERE, "tls")
if os.path.exists(os.path.join(ca, "ca.pem")):
    os.environ["SSL_CERT_FILE"] = os.path.join(ca, "ca.pem")
    sctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sctx.load_cert_chain(os.path.join(ca, "srv.pem"), os.path.join(ca, "srv.key"))
    snis = []
    sctx.sni_callback = lambda so, name, ctx: snis.append(name)
    ls = socket.socket(); ls.bind(("127.0.0.1", 0)); ls.listen(8); tport = ls.getsockname()[1]
    def tls_serve():
        while True:
            try:
                c, _ = ls.accept()
            except OSError:
                return
            try:
                t = sctx.wrap_socket(c, server_side=True)
                t.recv(4096)
                body = b"<html><head><title>x</title></head><body><p>alpha beta gamma delta</p></body></html>"
                t.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n" % len(body) + body)
                t.close()
            except (OSError, ssl.SSLError):
                c.close()
    threading.Thread(target=tls_serve, daemon=True).start()
    qr.DEADLINE = 5.0
    qr._check_address = lambda h, p: ["127.0.0.1"]
    out["tls_good"] = list(qr.fetch_page("https://good.test:%d/" % tport))
    out["tls_bad_name"] = list(qr.fetch_page("https://bad.test:%d/" % tport))
    out["tls_sni_seen"] = snis
    ls.close()
print(json.dumps(out, indent=1))
