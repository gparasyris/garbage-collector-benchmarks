#!/bin/bash
# filename=$1
# high=$2
# outputname=$3
awk 'NR==FNR{a[NR]=$1;b[NR]=$3;next}{print a[FNR], b[FNR], $2-b[FNR]}' $1 $2 >> $3
# 
# {printf "%s\t%4.2f\n", a[FNR], b[FNR]/$2 }' $1 $2
# echo "here $1 $2"
# filename=$1
# high=$2
# outputname=$3
# low=$4

# sed "s/.*$low/*&/" $filename >> "plot_$filename"
# echo "gnuplot -e \"filename='plot_$1'; high='$2'\" imigration.gnu"
# gnuplot -e "filename='plot_$1'; high='$2'; outputname='$3'" allocationFailures.gnu
