#!/usr/bin/env bash

python3 src/static_site_gen/main.py
cd public && python3 -m http.server 8888
