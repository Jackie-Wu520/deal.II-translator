#!/bin/bash
for filename in headers/*.h; do
        ./to2.py "$filename" 
done
