#!/usr/bin/env bash
set -e

# Chạy Postgres local bằng Docker
# DB: booksysdb | user: postgres | pass: postgres
container_name="podbook-pg"

if [ "$(docker ps -aq -f name=$container_name)" ]; then
  echo "Container $container_name đã tồn tại. Khởi động lại..."
  docker start $container_name || true
else
  echo "Tạo container $container_name ..."
  docker run --name $container_name \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booksysdb \
    -p 5432:5432 \
    -d postgres:15
fi

echo "Postgres started at localhost:5432 (db=booksysdb, user=postgres, pass=postgres)"
echo "Đặt DB_DIALECT=postgres trong .env để dùng Postgres."
