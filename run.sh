#!/usr/bin/env bash

docker run -d --name ruian-import \
  -v {$pwd}/data:/opt/ruian/data -v {$pwd}/config:/opt/ruian/config \
  --network=rest-service_ruian-net \
  sysnetcz/ruian-sync:manual-build
{$pwd}