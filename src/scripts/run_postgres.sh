#!/usr/bin/env bash
# Demo script (không dùng trong MSSQL)
set -e
CONTAINER=pg-local
PORT=5432
PASS=postgres
DB=appdb

if [ "$(docker ps -aq -f name=$CONTAINER)" ]; then
  docker rm -f $CONTAINER >/dev/null 2>&1 || true
fi
docker run -d --name $CONTAINER -e POSTGRES_PASSWORD=$PASS -e POSTGRES_DB=$DB -p $PORT:5432 postgres:16
echo "Postgres is up on port $PORT (db=$DB, user=postgres, pass=$PASS)"
