#!/bin/bash

cd /tmp/src
echo "db_user=${db_user}" > .env
echo "db_password=${db_password}" > .env
echo "db_host=${db_host}" > .env
echo "db_port=${db_port}" > .env
npm run create