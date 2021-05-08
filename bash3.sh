#!/bin/bash
for filename in examples/*_T.txt; do
        ./from.py ${filename} 
done
