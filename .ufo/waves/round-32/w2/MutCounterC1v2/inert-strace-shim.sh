#!/bin/sh
# Mutation control: accept the counter's strace options but never trace or inject.
while [ "$#" -gt 0 ]; do
    case "$1" in
        -f|-qq|--seccomp-bpf) shift ;;
        -o|-P|-e) shift 2 ;;
        --) shift; break ;;
        *) break ;;
    esac
done
exec "$@"
