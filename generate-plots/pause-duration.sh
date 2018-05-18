#!/bin/bash
# echo "here $1 $2"
filename=$1
high=$2
outputname=$3
low=$4

# echo $1 $2 $3
# sed "s/.*$low/*&/" $filename >> "plot_$filename"
# echo "gnuplot -e \"filename='plot_$1'; high='$2'\" imigration.gnu"
gnuplot -e "filename='$1'; high='$2'; outputname='$3'" pause-duration.gnu
