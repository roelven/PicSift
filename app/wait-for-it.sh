#!/bin/bash

# wait-for-it.sh

TIMEOUT=15
QUIET=0
PROTOCOL=tcp
VERBOSE=0

echoerr() {
  if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
  exitcode="$1"
  cat << USAGE >&2
Usage:
  $0 host:port [-s] [-t timeout] [-- command args]
  -h HOST | --host=HOST       Host or IP under test
  -p PORT | --port=PORT       TCP port under test
                             Alternatively, you specify the host and port as host:port
  -s | --strict               Only execute subcommand if the test succeeds
  -q | --quiet                Don't output any status messages
  -t TIMEOUT | --timeout=TIMEOUT
                             Timeout in seconds, zero for no timeout
  -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
  exit "$exitcode"
}

wait_for() {
  if [[ $TIMEOUT -gt 0 ]]; then
    echoerr "$host:$port - waiting $TIMEOUT seconds for $PROTOCOL connection"
  else
    echoerr "$host:$port - waiting for $PROTOCOL connection indefinitely"
  fi
  start_ts=$(date +%s)
  while :
  do
    set +e
    nc -z -w 1 $host $port
    result=$?
    set -e

    if [[ $result -eq 0 ]]; then
      end_ts=$(date +%s)
      echoerr "$host:$port is not available after $((end_ts - start_ts)) seconds"
      break
    fi
    sleep 1
  done
  return $result
}

while [[ $# -gt 0 ]]
do
  case "$1" in
    *:* )
    host=$(printf "%s\n" "$1"| cut -d : -f 1)
    port=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift 1
    ;;
    -q | --quiet)
    QUIET=1
    shift 1
    ;;
    -s | --strict)
    STRICT=1
    shift 1
    ;;
    -t)
    TIMEOUT="$2"
    if [[ $TIMEOUT == "" ]]; then break; fi
    shift 2
    ;;
    --timeout=*)
    TIMEOUT="${1#*=}"
    shift 1
    ;;
    --)
    shift
    COMMAND="$@"
    break
    ;;
    --help)
    usage 0
    ;;
    *)
    echoerr "Unknown argument: $1"
    usage 1
    ;;
  esac
done

if [[ "$host" == "" || "$port" == "" ]]; then
  echoerr "Error: you need to provide a host and port to test."
  usage 2
fi

wait_for
RESULT=$?

exit $RESULT
