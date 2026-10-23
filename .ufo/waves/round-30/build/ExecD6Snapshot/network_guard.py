#!/usr/bin/env python3
"""Run an offline negative control with socket events refused and counted."""
import runpy
import sys

attempts = []
def guard(event, args):
    if event.startswith('socket.'):
        attempts.append(event)
        raise RuntimeError('offline negative control may not use sockets')

sys.addaudithook(guard)
sys.argv = sys.argv[1:]
try:
    runpy.run_path(sys.argv[0], run_name='__main__')
finally:
    print('CANDIDATE_SOCKET_EVENTS=' + str(len(attempts)), file=sys.stderr)
