#!/bin/bash


FAIL () {
    local frame=0 LINE SUB FILE
    set +v
    while read LINE SUB FILE < <(caller "$frame"); do
	printf '  %s@ %s :%s' "${SUB}" "${FILE}" "${LINE}" >&2
	((frame++))
    done
    echo
    echo
    set -v
}

export -f FAIL

FAIL=FAIL TRAP_ERRORS=FAIL bash -Ev "${@}"
