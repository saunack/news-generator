#!/bin/bash

python3 scrape.py

folder='../raw_scrape/'
rm ${folder}missed.txt
rm ${folder}timeout.txt
rm ${folder}master.csv

for f in ${folder}*.log ;
do
    cat $f | grep "not present" | grep -o '[0-9][0-9]*\/[0-9]*[0-9]\/[0-9]*' >> missed.txt
    cat $f | grep TIMEOUT | sed  "s/.*\(https.*\.ece\).*web\/\([0-9]*\/[0-9]*[0-9]\/[0-9]*\).*/\1 \2/" >> timeout.txt
done

for f in ${folder}*.csv ;
do
    cat $f >> master.csv
done

