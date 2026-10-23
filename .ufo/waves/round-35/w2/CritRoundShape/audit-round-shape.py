#!/usr/bin/env python3
"""Read-only round-shape census; never invokes the validator or a judge."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
WAVE = LANE / '.ufo/waves/round-35'
FLEET = LANE.parent
SOURCES = {
    'spec': WAVE / 'w2-spec.json',
    'dispatch_payload': WAVE / 'w2-plan.json',
    'taskcall_copy': WAVE / 'w2-taskcall.json',
    'registry': WAVE / 'w2/swarm-registry.json',
    'policy': FLEET / 'scripts/hyaku/ufo-wave-policy-v2.json',
    'addendum': FLEET / 'scripts/hyaku/lane-addendum.md',
    'validator_source': Path('/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs'),
    'generator': WAVE / 'gen-w2-spec.py',
    'landed_gate': LANE / 'tools/research-gate.sh',
    'base_gate': WAVE / 'repairs/base-gate.sh',
}


def role_mix(rows, field):
    return dict(sorted(Counter(row[field] for row in rows).items()))


def line_containing(text, literal):
    return next((i for i, line in enumerate(text.splitlines(), 1) if literal in line), None)


def count_key(value, key):
    if isinstance(value, dict):
        return int(key in value) + sum(count_key(v, key) for v in value.values())
    if isinstance(value, list):
        return sum(count_key(v, key) for v in value)
    return 0


ap = argparse.ArgumentParser()
ap.add_argument('--output', type=Path, required=True)
args = ap.parse_args()
raw = {name: path.read_bytes() for name, path in SOURCES.items()}
texts = {name: value.decode() for name, value in raw.items()}
docs = {name: json.loads(texts[name]) for name in
        ('spec', 'dispatch_payload', 'taskcall_copy', 'registry', 'policy')}
spec, payload, call, registry, policy = (docs[name] for name in
    ('spec', 'dispatch_payload', 'taskcall_copy', 'registry', 'policy'))
items, tasks, members = spec['items'], call['tasks'], registry['members']
item_roles = {item['name']: item['role'] for item in items}
task_roles = {task['name']: task['agent'] for task in tasks}
member_roles = {name: member['role'] for name, member in members.items()}
lane_re = re.compile(re.escape(str(LANE)) + r'(?=/|\s|[\x60\x22\x27<>)]|$)')
missing = []
for item, task in zip(items, tasks):
    if not lane_re.search(item['prompt']):
        spec_name = line_containing(texts['spec'], '"name": ' + json.dumps(item['name']))
        call_name = line_containing(texts['taskcall_copy'], '"name": ' + json.dumps(task['name']))
        missing.append({'name': item['name'], 'role': item['role'],
                        'spec_prompt_line': spec_name + 2,
                        'task_text_line': call_name + 2})
attack_roles = {'reviewer', 'critic', 'mutation-tester'}
attack = sum(item['role'] in attack_roles for item in items)
planner_counts = {
    'spec': sum(i['role'] == 'planner' for i in items),
    'dispatch_tasks': sum(t['agent'] == 'planner' for t in payload['taskCall']['tasks']),
    'taskcall_copy': sum(t['agent'] == 'planner' for t in tasks),
    'payload_registry': sum(m['role'] == 'planner' for m in payload['registry']['members'].values()),
    'persisted_registry': sum(m['role'] == 'planner' for m in members.values()),
}
policy_swarm = policy['sighting']['dispatch']['swarm']
policy_fields = ('maxLanes', 'minLanes', 'waveMinLanes', 'waveMaxLanes', 'rampBatchSize', 'rampIntervalMs')
report_paths = []
for task in tasks:
    m = re.search(r'\nReport: write your scoped findings to (.+)\Z', task['task'])
    expected = spec['reportDir'] + '/' + task['name'] + '.md'
    report_paths.append(m is not None and m.group(1) == expected and not Path(m.group(1)).is_absolute())
result = {
    'access_date': '2026-10-23',
    'scope': 'static artifact audit only; no validator, judge, gate or dispatch invocation',
    'axes': spec['axes'],
    'wave': spec['wave'],
    'sources': {name: {'path': str(path), 'sha256': hashlib.sha256(raw[name]).hexdigest(),
                      'bytes': len(raw[name])} for name, path in SOURCES.items()},
    'populations': {'spec_items': len(items), 'validator_counts': payload['counts'],
                    'validator_tasks': len(payload['taskCall']['tasks']), 'taskcall_copy': len(tasks),
                    'payload_registry_members': len(payload['registry']['members']),
                    'persisted_registry_members': len(members)},
    'roles': {'spec': role_mix(items, 'role'), 'tasks': role_mix(tasks, 'agent'),
              'registry': role_mix(list(members.values()), 'role')},
    'attack': {'roles': sorted(attack_roles), 'count': attack, 'denominator': len(items),
               'percent': 100 * attack / len(items), 'minimum_count_at_25_percent': (len(items) + 3) // 4,
               'at_least_25_percent': attack * 4 >= len(items)},
    'identity': {'spec_names_unique': len(item_roles) == len(items),
                 'task_names_unique': len(task_roles) == len(tasks),
                 'name_role_maps_equal': item_roles == task_roles == member_roles,
                 'item_task_order_equal': [i['name'] for i in items] == [t['name'] for t in tasks],
                 'distinct_spec_prompts': len({i['prompt'] for i in items}),
                 'distinct_task_bodies': len({t['task'] for t in tasks}),
                 'payload_registry_matches_persisted': payload['registry']['members'] == members,
                 'registry_spawn_members': sum(m['kind'] == 'spawn' for m in members.values()),
                 'unrecorded_agent_ids': sum(m['agentId'] is None for m in members.values())},
    'policy': {'declared_band': [policy_swarm['waveMinLanes'], policy_swarm['waveMaxLanes']],
               'declared_max_lanes': policy_swarm['maxLanes'],
               'payload_values_match_policy': all(payload['policy'][f] == policy_swarm[f] for f in policy_fields),
               'population_in_band': policy_swarm['waveMinLanes'] <= len(items) <= policy_swarm['waveMaxLanes'],
               'population_below_cap': len(items) <= policy_swarm['maxLanes'],
               'policy_profile_planner_declarations': [name for name, profile in policy['nativeProfiles'].items()
                                                        if profile.get('planner', {}).get('role') == 'planner']},
    'one_call': {'taskCall_key_count_in_payload': count_key(payload, 'taskCall'),
                 'taskcall_copy_equals_emitted': call == payload['taskCall'],
                 'shared_context_equals_spec': call['context'] == spec['context'],
                 'resume_sends': len(payload['resumeSends']),
                 'literal_dispatch_field_present': 'dispatch' in payload,
                 'source_invariant_line': line_containing(texts['validator_source'], 'calls: spawns.length > 0 ? 1 : 0'),
                 'source_payload_emission_line': line_containing(texts['validator_source'], 'spawns.length > 0 ? { context: plan.context, tasks: spawns } : null'),
                 'dispatch_calls_implied_by_source': 1 if payload['counts']['spawn'] else 0,
                 'actual_task_invocation_count': None},
    'planner_seats': planner_counts,
    'paths': {'shared_context_has_absolute_lane': bool(lane_re.search(call['context'])),
              'spec_items_with_absolute_lane': sum(bool(lane_re.search(i['prompt'])) for i in items),
              'tasks_with_absolute_lane': sum(bool(lane_re.search(t['task'])) for t in tasks),
              'tasks_bound_when_shared_context_included': sum(bool(lane_re.search(call['context'] + '\n' + t['task'])) for t in tasks),
              'all_report_trailers_expected_and_lane_relative': all(report_paths),
              'missing_item_lane_paths': missing},
    'stale_64_seat_mentions': {
        'generator_docstring_line': line_containing(texts['generator'], 'one v2 wave (64 seats'),
        'generator_audit_assignment_line': line_containing(texts['generator'], 'ONE v2 wave of 64 seats'),
        'spec_audit_assignment_line': line_containing(texts['spec'], 'ONE v2 wave of 64 seats'),
        'taskcall_audit_assignment_line': line_containing(texts['taskcall_copy'], 'ONE v2 wave of 64 seats')},
}
encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
args.output.write_text(encoded)
print(encoded, end='')
