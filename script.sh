#!/bin/bash

rm missed.txt
rm timeout.txt
rm master.csv

for f in *.log ;
do
    cat $f | grep "not present" | grep -o '[0-9][0-9]*\/[0-9]*[0-9]\/[0-9]*' >> missed.txt
    cat $f | grep TIMEOUT | sed  "s/.*\(https.*\.ece\).*web\/\([0-9]*\/[0-9]*[0-9]\/[0-9]*\).*/\1 \2/" >> timeout.txt
done

for f in *.csv ;
do
    cat $f >> master.csv
done

