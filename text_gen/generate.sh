#!/bin/sh

# k = 50, penalty = 1.3, nucleus sampling = 0.7, temperature = .6
folder='../sample_output'
for k in 20 50 100
do
    for temperature in 3 6 9 12
    do
        for penalty in 10 15 50 100
        do
            for nsample in 3 7 10 30
            do
                t=$(echo $temperature*1.0/10 | bc -l)
                p=$(echo $nsample*1.0/10 | bc -l)
                echo $k, $t, $penalty, $p
                echo $k, $t, $penalty, $p >> log.txt
                python3 generate.py --prompt $1 -t $t -k $k --penalty $penalty -p $p -n 2 >> ${folder}hyper_param_log.txt
                echo "\n#END#\n" >> ${folder}log.txt
            done
        done
    done
done

python3 tuning.py
