#!/usr/bin/env python3
"""freeze-check.py - pre-ready check of a wave's frozen claims, spec and dispatch payload.

    freeze-check.py --claims <claims.md> --dispatch <wN-dispatch.json> --spec <wN-spec.json> --ready <wN.ready>
    freeze-check.py --selftest [--lane-root DIR] [--work DIR]

Exit 0 only when every check below passes; exit 1 when any fails; exit 2 on a usage error.
Output: one `CHECK <ID> PASS|FAIL <detail>` line per check, `WARN ...` lines (never change
the exit code), then `FAILED_CHECKS=<ids|none>` and `FREEZE_CHECK=PASS|FAIL`.

Checks (the first two are QUALITY 116, the rest QUALITY 118; round 60 / round 59 lessons):
  CLAIMS_NONEMPTY  claims file exists, is a regular file and has > 0 bytes; its sha256 is the reference digest.
  CONTEXT_DIGEST   the reference digest occurs in dispatch taskCall.context as a whole 64-hex token
                   (not a prefix like `65721569...`, not a longer hex run).
  DIGEST_STRAY     no OTHER 64-hex token occurs in any item prompt (spec bodies, dispatch task bodies) or in the
                   spec/dispatch context. Round 60: claims 65721569... vs prompts 09d8053f...
                   Deliberate foreign digests (e.g. a cited capture hash) need `--allow-digest <hex64>`.
  CONTEXT_SPEC_EQ  spec.context == dispatch.taskCall.context.
  NAMES            spec item names are unique and equal, in order, the dispatch task names; task.agent == item.role.
  BODY_RENDER      every dispatch task body equals the spec item rendered by the validator's rules (RENDER below);
                   a spec edited after rendering (round 59: 0/66 equal) fails here.
  READY_DISPATCH   ready is JSON, names an existing dispatch file, and that file is the --dispatch file.
  READY_IDENT      ready lane/round/wave match dispatch.wave (`<lane>-r<round>-<wave>`), spec.wave, and the
                   dispatch location `round-<round>/<wave>-dispatch.json`.
  WARN ORDER       (advisory, mtimes are not preserved by checkouts) spec or dispatch newer than ready.

RENDER, inferred from the real spec/dispatch pairs of rounds 32-61 (42 of 44 pairs reproduce byte for byte; the 2
that do not are round-57/w2, whose tasks are the bare bodies with no wrapper, and round-59, whose spec was rewritten): task =
    ('/skill:godspeed\\n\\n' unless the body already starts with '/skill:') + body
    + '\\n\\nLane bounds: leaf member - no subagent dispatch' + (' except your single labrat.' if role == 'executor' else '.')   [dash is U+2014]
    + '\\nJudged on: ' + ', '.join(item.axes or spec.axes)
    + ('\\nMilestone: ' + spec.milestone if spec.milestone)
    + '\\n\\nReport: write your scoped findings to ' + spec.reportDir + '/' + name + '.md'
body = item.prompt, else item.item; when spec.template exists, body = template.replace('{{item}}', body).
"""
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HEX64 = re.compile(r'(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])')
LANE_ROOT_DEFAULT = '/home/vgpnk/Projects/shokunin/chousa-shokunin'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def body_of(item):
    return item.get('prompt', item.get('item'))


def render(spec, item):
    body = body_of(item)
    if isinstance(spec.get('template'), str):
        body = spec['template'].replace('{{item}}', body)
    pre = '' if body.startswith('/skill:') else '/skill:godspeed\n\n'
    lb = 'leaf member \u2014 no subagent dispatch' + (' except your single labrat.' if item.get('role') == 'executor' else '.')
    axes = item.get('axes') or spec.get('axes') or []
    out = pre + body + '\n\nLane bounds: ' + lb + '\nJudged on: ' + ', '.join(axes)
    if spec.get('milestone'):
        out += '\nMilestone: ' + spec['milestone']
    out += '\n\nReport: write your scoped findings to ' + spec['reportDir'] + '/' + item['name'] + '.md'
    return out


def load_json(path):
    with open(path, 'rb') as f:
        return json.loads(f.read().decode('utf-8'))


def run_checks(claims, dispatch_path, spec_path, ready_path, allow):
    res = []   # (id, ok, detail)
    warns = []

    def add(cid, ok, detail):
        res.append((cid, bool(ok), detail))

    # --- claims
    ref = None
    try:
        st = os.stat(claims)
        if not os.path.isfile(claims):
            add('CLAIMS_NONEMPTY', False, 'not a regular file: %s' % claims)
        elif st.st_size == 0:
            add('CLAIMS_NONEMPTY', False, 'empty file: %s' % claims)
        else:
            ref = sha256_file(claims)
            add('CLAIMS_NONEMPTY', True, '%d bytes sha256=%s' % (st.st_size, ref))
    except OSError as e:
        add('CLAIMS_NONEMPTY', False, 'cannot stat %s: %s' % (claims, e.strerror))

    # --- load dispatch + spec
    disp = spec = None
    ctx_d = ctx_s = ''
    tasks, items = [], []
    try:
        disp = load_json(dispatch_path)
        tc = disp['taskCall']
        ctx_d, tasks = tc['context'], tc['tasks']
        if not isinstance(ctx_d, str) or not isinstance(tasks, list):
            raise ValueError('taskCall.context/tasks have wrong types')
    except (OSError, ValueError, KeyError, TypeError) as e:
        disp = None
        for cid in ('CONTEXT_DIGEST', 'DIGEST_STRAY', 'CONTEXT_SPEC_EQ', 'NAMES', 'BODY_RENDER'):
            add(cid, False, 'dispatch unreadable (%s): %s' % (type(e).__name__, dispatch_path))
    try:
        spec = load_json(spec_path)
        ctx_s, items = spec['context'], spec['items']
        if not isinstance(items, list):
            raise ValueError('items is not a list')
    except (OSError, ValueError, KeyError, TypeError) as e:
        spec = None
        for cid in ('CONTEXT_SPEC_EQ', 'NAMES', 'BODY_RENDER', 'DIGEST_STRAY'):
            if not any(r[0] == cid for r in res):
                add(cid, False, 'spec unreadable (%s): %s' % (type(e).__name__, spec_path))

    if disp is not None:
        toks = [t.lower() for t in HEX64.findall(ctx_d)]
        if ref is None:
            add('CONTEXT_DIGEST', False, 'no reference digest (claims missing or empty)')
        elif ref in toks:
            add('CONTEXT_DIGEST', True, 'context carries %s' % ref)
        else:
            near = ref[:8] in ctx_d.lower()
            add('CONTEXT_DIGEST', False, 'context lacks whole-token %s%s' % (
                ref, ' (only a prefix/longer run of it appears)' if near else ''))

        if spec is not None:
            add('CONTEXT_SPEC_EQ', ctx_s == ctx_d,
                'identical (%d chars)' % len(ctx_d) if ctx_s == ctx_d else
                'spec.context (%d chars) != dispatch context (%d chars)' % (len(ctx_s), len(ctx_d)))

    # --- digest strays
    if disp is not None and spec is not None:
        stray = []
        def scan(where, text):
            for m in HEX64.finditer(text):
                t = m.group().lower()
                if t != ref and t not in allow:
                    stray.append('%s:%s...' % (where, t[:8]))
        scan('dispatch.context', ctx_d)
        scan('spec.context', ctx_s)
        for it in items:
            if isinstance(it, dict) and isinstance(body_of(it), str):
                scan('spec:' + str(it.get('name')), body_of(it))
        for t in tasks:
            if isinstance(t, dict) and isinstance(t.get('task'), str):
                scan('dispatch:' + str(t.get('name')), t['task'])
        if ref is None:
            add('DIGEST_STRAY', False, 'no reference digest to compare against')
        elif stray:
            add('DIGEST_STRAY', False, '%d foreign 64-hex tokens vs claims %s...: %s' % (
                len(stray), ref[:8], ', '.join(stray[:6]) + (' ...' if len(stray) > 6 else '')))
        else:
            add('DIGEST_STRAY', True, 'no 64-hex token other than the claims digest')

        # --- names / render
        names_s = [it.get('name') for it in items if isinstance(it, dict)]
        names_t = [t.get('name') for t in tasks if isinstance(t, dict)]
        probs = []
        if len(names_s) != len(items) or len(names_t) != len(tasks):
            probs.append('non-object entries')
        if len(set(names_s)) != len(names_s):
            probs.append('duplicate spec names')
        if names_s != names_t:
            probs.append('spec names (%d) != dispatch names (%d) in order; first diff %s' % (
                len(names_s), len(names_t), next(((a, b) for a, b in zip(names_s, names_t) if a != b),
                                                 (set(names_s) ^ set(names_t)))))
        else:
            bad = [t.get('name') for it, t in zip(items, tasks) if it.get('role') != t.get('agent')]
            if bad:
                probs.append('role != agent for %d tasks, first %s' % (len(bad), bad[0]))
        add('NAMES', not probs, '; '.join(probs) or '%d names match in order, roles match agents' % len(names_s))

        by_task = {t.get('name'): t.get('task') for t in tasks if isinstance(t, dict)}
        eq, bad = 0, []
        for it in items:
            try:
                want = render(spec, it)
            except (KeyError, TypeError) as e:
                bad.append('%s(unrenderable:%s)' % (it.get('name'), e))
                continue
            if by_task.get(it['name']) == want:
                eq += 1
            else:
                bad.append(it['name'])
        extra = [n for n in by_task if n not in set(names_s)]
        ok = not bad and not extra
        add('BODY_RENDER', ok, '%d/%d dispatch tasks equal the rendered spec items%s%s' % (
            eq, len(items), '' if not bad else '; first mismatch %s' % bad[0],
            '' if not extra else '; %d tasks without spec item (first %s)' % (len(extra), extra[0])))

    # --- ready
    ready = None
    try:
        ready = load_json(ready_path)
        if not isinstance(ready, dict):
            raise ValueError('ready JSON is not an object')
    except (OSError, ValueError) as e:
        for cid in ('READY_DISPATCH', 'READY_IDENT'):
            add(cid, False, 'ready unreadable (%s): %s' % (type(e).__name__, ready_path))
    if ready is not None:
        rd = ready.get('dispatch')
        if not isinstance(rd, str) or not rd:
            add('READY_DISPATCH', False, 'ready has no dispatch path')
        else:
            p = rd if os.path.isabs(rd) else os.path.join(os.path.dirname(os.path.abspath(ready_path)), rd)
            if not os.path.isfile(p):
                add('READY_DISPATCH', False, 'ready names a dispatch file that does not exist: %s' % p)
            elif os.path.realpath(p) != os.path.realpath(dispatch_path):
                add('READY_DISPATCH', False, 'ready names %s, not the checked dispatch %s' % (p, dispatch_path))
            else:
                add('READY_DISPATCH', True, 'ready -> %s' % p)
        lane, rnd, wave = ready.get('lane'), ready.get('round'), ready.get('wave')
        probs = []
        if not (isinstance(lane, str) and lane and isinstance(wave, str) and wave
                and isinstance(rnd, int) and not isinstance(rnd, bool)):
            probs.append('ready lane/round/wave missing or mistyped (%r/%r/%r)' % (lane, rnd, wave))
        else:
            want = '%s-r%d-%s' % (lane, rnd, wave)
            if disp is None or not isinstance(disp.get('wave'), str):
                probs.append('dispatch wave unavailable')
            elif disp['wave'] != want:
                probs.append('dispatch.wave %r != ready %r' % (disp['wave'], want))
            if spec is not None and spec.get('wave') != want:
                probs.append('spec.wave %r != ready %r' % (spec.get('wave'), want))
            dp = os.path.abspath(dispatch_path)
            if os.path.basename(dp) != '%s-dispatch.json' % wave or os.path.basename(os.path.dirname(dp)) != 'round-%d' % rnd:
                probs.append('dispatch file location %s is not round-%d/%s-dispatch.json' % (dp, rnd, wave))
        add('READY_IDENT', not probs, '; '.join(probs) or 'lane=%s round=%d wave=%s agree with dispatch, spec and location' % (lane, rnd, wave))

    # --- advisory ordering
    try:
        ms, md, mr = (os.stat(p).st_mtime for p in (spec_path, dispatch_path, ready_path))
        if ms > mr or md > mr:
            warns.append('ORDER spec/dispatch newer than ready (spec %+.0fs, dispatch %+.0fs vs ready): rewrite after ready?' % (ms - mr, md - mr))
    except OSError:
        pass
    return res, warns


def cli(argv):
    ap = argparse.ArgumentParser(prog='freeze-check.py', description=__doc__.split('\n')[1])
    ap.add_argument('--claims'); ap.add_argument('--dispatch'); ap.add_argument('--spec'); ap.add_argument('--ready')
    ap.add_argument('--allow-digest', action='append', default=[], metavar='HEX64',
                    help='a deliberately cited foreign 64-hex digest (repeatable)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--lane-root', default=LANE_ROOT_DEFAULT, help='selftest: lane holding the real round-59/60/61 files')
    ap.add_argument('--work', help='selftest: scratch directory (default: a fresh dir under $TMPDIR)')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.lane_root, a.work)
    if not (a.claims and a.dispatch and a.spec and a.ready):
        ap.error('--claims, --dispatch, --spec and --ready are all required (or --selftest)')
    allow = set()
    for h in a.allow_digest:
        if not re.fullmatch(r'[0-9A-Fa-f]{64}', h):
            ap.error('--allow-digest needs 64 hex chars: %r' % h)
        allow.add(h.lower())
    res, warns = run_checks(a.claims, a.dispatch, a.spec, a.ready, allow)
    for cid, ok, detail in res:
        print('CHECK %s %s %s' % (cid, 'PASS' if ok else 'FAIL', detail))
    for w in warns:
        print('WARN ' + w)
    failed = [c for c, ok, _ in res if not ok]
    print('FAILED_CHECKS=' + (','.join(failed) or 'none'))
    print('FREEZE_CHECK=' + ('FAIL' if failed else 'PASS'))
    return 1 if failed else 0


# ----------------------------------------------------------------------------- selftest
def selftest(lane_root, work):
    me = os.path.abspath(__file__)
    waves = os.path.join(lane_root, '.ufo', 'waves')
    own = work is None
    base = tempfile.mkdtemp(prefix='freeze-selftest-') if own else work
    os.makedirs(base, exist_ok=True)
    cases = []   # (name, argv, expect_exit, expect_failed set)
    try:
        def real(r):
            rdy = load_json(os.path.join(waves, 'round-%d' % r, 'w1.ready'))
            rdy['dispatch'] = '@DISPATCH@'   # replaced by the fixture's own dispatch path
            return (load_json(os.path.join(waves, 'round-%d' % r, 'w1-spec.json')),
                    load_json(os.path.join(waves, 'round-%d' % r, 'w1-dispatch.json')), rdy)

        def mk(name, rnd, spec, disp, ready, claims_bytes):
            d = os.path.join(base, name)
            rd = os.path.join(d, 'round-%d' % rnd)
            os.makedirs(rd)
            sp, dp, rp, cp = (os.path.join(rd, 'w1-spec.json'), os.path.join(rd, 'w1-dispatch.json'),
                              os.path.join(rd, 'w1.ready'), os.path.join(d, 'claims.md'))
            for p, o in ((sp, spec), (dp, disp)):
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(o, f, ensure_ascii=False, indent=1)
            ready = dict(ready)
            ready['dispatch'] = ready['dispatch'].replace('@DISPATCH@', dp)
            with open(rp, 'w', encoding='utf-8') as f:
                json.dump(ready, f)
            if claims_bytes is not None:
                with open(cp, 'wb') as f:
                    f.write(claims_bytes)
            return ['--claims', cp, '--dispatch', dp, '--spec', sp, '--ready', rp], d

        def case(name, expect_exit, expect_failed, argv):
            cases.append((name, argv, expect_exit, set(expect_failed)))

        # ---- green base: the real round-61 triple (claims file read-only from the lane)
        s61, d61, r61 = real(61)
        claims61 = open(os.path.join(lane_root, 'corpus', 'evidence', 'round61', 'claims.md'), 'rb').read()
        ref61 = hashlib.sha256(claims61).hexdigest()

        def g61():
            return copy.deepcopy(s61), copy.deepcopy(d61), dict(r61)

        a, _ = mk('G1_real_r61', 61, *g61(), claims61)
        case('G1 green: real round-61 triple', 0, [], a)

        # ---- real round-60 pair (claim digest 65721569.. vs prompt 09d8053f..)
        s60, d60, r60 = real(60)
        claims60 = open(os.path.join(lane_root, 'corpus', 'evidence', 'round60-claims.md'), 'rb').read()
        ref60 = hashlib.sha256(claims60).hexdigest()
        wrong60 = '09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440'
        assert ref60.startswith('65721569') and wrong60 in s60['items'][0]['prompt'], 'round-60 inputs are not the expected pair'
        a, _ = mk('R1_real_r60', 60, s60, d60, r60, claims60)
        case('R1 red: real round-60 pair (claims 65721569.. vs prompts 09d8053f..)', 1, ['CONTEXT_DIGEST', 'DIGEST_STRAY'], a)

        # repaired round-60: digest corrected in every prompt and carried in the context -> green
        def fix60():
            s, d = copy.deepcopy(s60), copy.deepcopy(d60)
            for it in s['items']:
                it['prompt'] = it['prompt'].replace(wrong60, ref60)
            for t in d['taskCall']['tasks']:
                t['task'] = t['task'].replace(wrong60, ref60)
            s['context'] += ' Claims sha256 ' + ref60 + '.'
            d['taskCall']['context'] += ' Claims sha256 ' + ref60 + '.'
            return s, d
        s, d = fix60()
        a, _ = mk('G2_fixed_r60', 60, s, d, r60, claims60)
        case('G2 green: round-60 pair with digest repaired in prompts and context', 0, [], a)
        s, d = fix60()   # repaired prompts but context never carried the digest
        s['context'] = s60['context']; d['taskCall']['context'] = d60['taskCall']['context']
        a, _ = mk('R2_r60_ctx_only_missing', 60, s, d, r60, claims60)
        case('R2 red: round-60 prompts repaired but context lacks the digest', 1, ['CONTEXT_DIGEST'], a)
        s, d = copy.deepcopy(s60), copy.deepcopy(d60)
        s['context'] += ' sha256 ' + ref60; d['taskCall']['context'] += ' sha256 ' + ref60
        a, _ = mk('R3_r60_ctx_only_prompts_wrong', 60, s, d, r60, claims60)
        case('R3 red: round-60 context fixed but prompts still 09d8053f..', 1, ['DIGEST_STRAY'], a)

        # ---- real round-59 pair (spec rewritten after dispatch); claims file never existed
        s59, d59, r59 = real(59)
        a, _ = mk('R4_real_r59_noclaims', 59, s59, d59, r59, None)
        a[1] = os.path.join(lane_root, 'corpus', 'evidence', 'round59', 'claims.md')   # the path round 59's context named
        case('R4 red: real round-59 pair, claims path named by its context (absent)', 1,
             ['CLAIMS_NONEMPTY', 'CONTEXT_DIGEST', 'DIGEST_STRAY', 'BODY_RENDER'], a)
        fake59 = b'round 59 reconstructed claims (stand-in bytes)\n'
        r59d = hashlib.sha256(fake59).hexdigest()
        s, d = copy.deepcopy(s59), copy.deepcopy(d59)
        s['context'] += ' sha256 ' + r59d; d['taskCall']['context'] += ' sha256 ' + r59d
        a, _ = mk('R5_real_r59_spec_rewrite', 59, s, d, r59, fake59)
        case('R5 red: real round-59 spec/dispatch (66/66 bodies differ), claims + digest otherwise fine', 1, ['BODY_RENDER'], a)

        # ---- mutants of the green round-61 triple
        MISSING = object()

        def mut(name, expect, fn, claims=claims61, ready_fn=None, rnd=61):
            s, d, r = g61()
            c = fn(s, d, r)
            a, _ = mk(name, rnd, s, d, r, None if c is MISSING else (claims if c is None else c))
            if ready_fn:
                ready_fn(a)
            case(name, 1, expect, a)
            return a

        def empty(s, d, r): return b''
        mut('M01 red: claims file empty', ['CLAIMS_NONEMPTY', 'CONTEXT_DIGEST', 'DIGEST_STRAY'], empty)
        def edited(s, d, r): return claims61 + b'\n'
        mut('M02 red: claims edited by one byte after dispatch', ['CONTEXT_DIGEST', 'DIGEST_STRAY'], edited)
        def absent_claims(s, d, r): return MISSING
        a = mut('M03 red: claims file absent', ['CLAIMS_NONEMPTY', 'CONTEXT_DIGEST', 'DIGEST_STRAY'], absent_claims)
        def stray(s, d, r):
            x = '0' * 64
            s['items'][3]['prompt'] += ' The exact immutable claim SHA is %s.' % x
            d['taskCall']['tasks'][3]['task'] = render(s, s['items'][3])
        mut('M04 red: one prompt (spec and dispatch alike) carries a different 64-hex digest', ['DIGEST_STRAY'], stray)
        def upper(s, d, r):
            x = ref61.upper()[:63] + ('0' if ref61[-1] != '0' else '1')
            s['items'][0]['prompt'] += ' sha ' + x
            d['taskCall']['tasks'][0]['task'] = render(s, s['items'][0])
        mut('M05 red: one prompt carries a one-nibble-off uppercase copy of the digest', ['DIGEST_STRAY'], upper)
        def prefix_only(s, d, r):
            for o in (s, d['taskCall']):
                o['context'] = o['context'].replace(ref61, ref61[:16] + '...')
        mut('M06 red: context carries only the digest prefix', ['CONTEXT_DIGEST'], prefix_only)
        def longer(s, d, r):
            for o in (s, d['taskCall']):
                o['context'] = o['context'].replace(ref61, ref61 + 'a')
        mut('M07 red: context digest run is 65 hex (not a token)', ['CONTEXT_DIGEST'], longer)
        def spec_one(s, d, r):
            s['items'][5]['prompt'] = s['items'][5]['prompt'].replace('Attack', 'Inspect', 1) if 'Attack' in s['items'][5]['prompt'] else s['items'][5]['prompt'] + ' reworded'
        mut('M08 red: spec item reworded after dispatch (1 item)', ['BODY_RENDER'], spec_one)
        def spec_all(s, d, r):
            for it in s['items']:
                it['prompt'] = 'For round 61, ' + it['prompt']
        mut('M09 red: every spec item rewritten after dispatch (round-59 shape)', ['BODY_RENDER'], spec_all)
        def task_tail(s, d, r):
            d['taskCall']['tasks'][7]['task'] += '\nExtra instruction.'
        mut('M10 red: dispatch task body carries extra text', ['BODY_RENDER'], task_tail)
        def lane_bounds(s, d, r):
            t = d['taskCall']['tasks'][2]; t['task'] = t['task'].replace(' except your single labrat.', '.').replace('subagent dispatch.', 'subagent dispatch, anything allowed.')
            if t['task'] == render(s, s['items'][2]):
                t['task'] += ' '
        mut('M11 red: task lane-bounds line altered', ['BODY_RENDER'], lane_bounds)
        def drop(s, d, r):
            d['taskCall']['tasks'].pop(10)
        mut('M12 red: one dispatch task missing', ['NAMES', 'BODY_RENDER'], drop)
        def extra(s, d, r):
            t = copy.deepcopy(d['taskCall']['tasks'][0]); t['name'] = 'Smuggled'
            d['taskCall']['tasks'].append(t)
        mut('M13 red: one extra dispatch task', ['NAMES', 'BODY_RENDER'], extra)
        def swap(s, d, r):
            d['taskCall']['tasks'][0], d['taskCall']['tasks'][1] = d['taskCall']['tasks'][1], d['taskCall']['tasks'][0]
        mut('M14 red: dispatch task order swapped', ['NAMES'], swap)
        def agent(s, d, r):
            t = d['taskCall']['tasks'][4]; t['agent'] = 'executor' if t['agent'] != 'executor' else 'critic'
        mut('M15 red: task agent differs from item role', ['NAMES'], agent)
        def ctx(s, d, r):
            d['taskCall']['context'] += ' (late addendum)'
        mut('M16 red: dispatch context differs from spec context', ['CONTEXT_SPEC_EQ'], ctx)
        def axes(s, d, r):
            s['axes'] = list(s['axes']) + ['freshness']
        mut('M17 red: spec axes changed after render', ['BODY_RENDER'], axes)
        def rd_missing(s, d, r):
            r['dispatch'] = r['dispatch'] + '.gone'
        mut('M18 red: ready names a nonexistent dispatch file', ['READY_DISPATCH'], rd_missing)
        def other_file(a):
            rp = a[a.index('--ready') + 1]; dp = a[a.index('--dispatch') + 1]
            alt = os.path.join(os.path.dirname(dp), 'other-dispatch.json'); shutil.copyfile(dp, alt)
            j = load_json(rp); j['dispatch'] = alt
            json.dump(j, open(rp, 'w'))
        mut('M19 red: ready names a different existing file (a copy)', ['READY_DISPATCH'], lambda s, d, r: None, ready_fn=other_file)
        def r_round(s, d, r): r['round'] = 62
        mut('M20 red: ready round 62 vs dispatch round 61', ['READY_IDENT'], r_round)
        def r_wave(s, d, r): r['wave'] = 'w2'
        mut('M21 red: ready wave w2 vs dispatch w1', ['READY_IDENT'], r_wave)
        def r_lane(s, d, r): r['lane'] = 'other'
        mut('M22 red: ready lane other vs dispatch chousa', ['READY_IDENT'], r_lane)
        def r_nodisp(s, d, r): r['dispatch'] = ''
        mut('M23 red: ready has an empty dispatch path', ['READY_DISPATCH'], r_nodisp)
        def r_junk(a):
            open(a[a.index('--ready') + 1], 'w').write('not json')
        mut('M24 red: ready is not JSON', ['READY_DISPATCH', 'READY_IDENT'], lambda s, d, r: None, ready_fn=r_junk)
        def r_strround(s, d, r): r['round'] = '61'
        mut('M25 red: ready round is a string', ['READY_IDENT'], r_strround)

        # ---- the foreign-digest allowance is deliberate and exact
        s, d, r = g61()
        x = 'ab' * 32
        s['items'][3]['prompt'] += ' capture sha256 ' + x
        d['taskCall']['tasks'][3]['task'] = render(s, s['items'][3])
        a, _ = mk('G3_allow', 61, s, d, r, claims61)
        case('G3 green: foreign digest in a prompt with --allow-digest', 0, [], a + ['--allow-digest', x])
        a2 = list(a) + ['--allow-digest', 'cd' * 32]
        case('M26 red: foreign digest in a prompt, wrong --allow-digest', 1, ['DIGEST_STRAY'], a2)

        # ---- run
        ok_n = 0
        red_exit = None
        for name, argv, want_exit, want_failed in cases:
            p = subprocess.run([sys.executable, '-B', me] + argv, capture_output=True, text=True, timeout=120)
            m = re.search(r'^FAILED_CHECKS=(.*)$', p.stdout, re.M)
            got = set() if (m and m.group(1) == 'none') else set((m.group(1) if m else '?').split(','))
            ok = p.returncode == want_exit and got == want_failed
            ok_n += ok
            if name.startswith('R1 ') and red_exit is None:
                red_exit = p.returncode
            print('%s  [%s] exit=%d want=%d failed=%s want=%s' % (
                'PASS' if ok else 'FAIL', name, p.returncode, want_exit,
                ','.join(sorted(got)) or 'none', ','.join(sorted(want_failed)) or 'none'))
            if not ok:
                print(p.stdout + p.stderr)
        n = len(cases)
        print('SELFTEST %d/%d pass' % (ok_n, n))
        print('VERDICT: FREEZE_CHECK=%d/%d red_before_exit=%s' % (ok_n, n, red_exit))
        return 0 if ok_n == n else 1
    finally:
        if own:
            shutil.rmtree(base, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
