#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

retries=5
count=0

until [ $count -gt $retries ]
do
  status=$(curl -s "$host/_cluster/health" | jq -r '.status')
  if [ "$status" = "green" ]; then
    count=$((count+1))
    >&2 echo "Elasticsearch is green. Count: $count/$retries"
    sleep 5
  else
    count=0
    >&2 echo "⏳ Elasticsearch is $status - sleeping"
    sleep 5
  fi
done

>&2 echo "👍 Elasticsearch has been green consistently. Proceeding..."
exec $cmd
