#!/usr/bin/env python3
"""Execute unchanged CLI bytes; allow GET to exact registry URLs only.

HTTP responses are retained as diagnostic evidence, without changing reads.
The parent removes proxy variables and disables bytecode writes.
"""
import hashlib
import http.client
import json
import pathlib
import re
import runpy
import sys
import time
import urllib.parse

ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
trace_path = pathlib.Path(sys.argv[1])
target = sys.argv[2]
target_args = sys.argv[3:]
allowed = set()
for line in (ROOT / 'corpus/SOURCES.md').read_text(encoding='utf-8').splitlines():
    if line.startswith('| S'):
        cell = line.split('|')[2]
        match = re.search(r'https?://\S+', cell)
        if match:
            allowed.add(urllib.parse.urldefrag(match.group().rstrip('.,;)')).url)

events = []
responses = []
original_request = http.client.HTTPConnection.request
original_getresponse = http.client.HTTPConnection.getresponse
original_read = http.client.HTTPResponse.read


def guarded_request(connection, method, url, *args, **kwargs):
    scheme = 'https' if isinstance(connection, http.client.HTTPSConnection) else 'http'
    host = connection.host
    if ':' in host and not host.startswith('['):
        host = '[' + host + ']'
    default_port = 443 if scheme == 'https' else 80
    authority = host if connection.port == default_port else host + ':' + str(connection.port)
    full_url = url if url.startswith(('http://', 'https://')) else scheme + '://' + authority + url
    full_url = urllib.parse.urldefrag(full_url).url
    event = {'kind': 'request', 'method': method, 'url': full_url,
             'allowed': method == 'GET' and full_url in allowed, 'time': time.time()}
    events.append(event)
    if not event['allowed']:
        raise OSError('DiffToolB network guard refused non-registry request')
    connection._diff_request_url = full_url
    return original_request(connection, method, url, *args, **kwargs)


def traced_getresponse(connection, *args, **kwargs):
    response = original_getresponse(connection, *args, **kwargs)
    record = {'url': getattr(connection, '_diff_request_url', None),
              'status': response.status, 'headers': list(response.getheaders()),
              'body': bytearray(), 'bytes_seen': 0}
    response._diff_record = record
    responses.append(record)
    return response


def traced_read(response, *args, **kwargs):
    data = original_read(response, *args, **kwargs)
    record = getattr(response, '_diff_record', None)
    if record is not None:
        record['bytes_seen'] += len(data)
        room = max(0, 8 * 1024 * 1024 + 1 - len(record['body']))
        record['body'].extend(data[:room])
    return data


http.client.HTTPConnection.request = guarded_request
http.client.HTTPConnection.getresponse = traced_getresponse
http.client.HTTPResponse.read = traced_read
sys.argv = [target] + target_args
try:
    runpy.run_path(target, run_name='__main__')
finally:
    for index, record in enumerate(responses, 1):
        body = bytes(record.pop('body'))
        body_path = trace_path.with_name(trace_path.stem + '.body-' + str(index) + '.bin')
        body_path.write_bytes(body)
        record.update(body_path=str(body_path), sha256=hashlib.sha256(body).hexdigest())
    trace_path.write_text(json.dumps({'events': events, 'responses': responses}, indent=2) + '\n', encoding='utf-8')
