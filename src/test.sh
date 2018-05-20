#!/usr/bin/env bash

for i in `seq 1 10` ; do
    echo "Test ${i}"
    python3 test_browser.py 3
done