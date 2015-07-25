#!/usr/bin/env bash
for i in {0..50}; do (curl -u $1:$2 -Is https://staging.hacklaunch.com/projects/list/ | head -n1 &) 2>/dev/null; done
