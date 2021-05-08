#!/bin/bash
for filename in headers/*.h; do
        ./to.py "$filename" 
done
