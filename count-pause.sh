#!/bin/bash
# echo "here $1 $2"
#filename=$1
#high=$2
#outputname=$3
#low=$4

# echo $1 $2 $3
# sed "s/.*$low/*&/" $filename >> "plot_$filename"
# echo "gnuplot -e \"filename='plot_$1'; high='$2'\" imigration.gnu"
#gnuplot -e "filename='$1'; high='$2'; outputname='$3'" pause-duration.gnu
# rm -rf count-pause/
mkdir -p "count-pause/"
for file in "gc/"*; do
  echo $file
  filename=$(basename $file)
  awk '!/NOT/{print $1"\t"$(NF-1)"\t"$NF}' $file >>  "count-pause/$filename.dat"
  sed -i.bak 's/://' "count-pause/$filename.dat"
  passfile="count-pause/$filename.dat"
  passpng="count-pause/$filename.png"
  gnuplot -e "filename='$passfile'; outputname='$passpng'" count-pause.gnu
done
