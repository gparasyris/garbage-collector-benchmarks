#!/bin/bash
echo "here $1 $2"
filename=$1
high=$2
outputname=$3

sed "s/.*$high/*&/" $filename >> "plot_$filename"
echo "gnuplot -e \"filename='plot_$1'; high='$2'\" imigration.gnu"
gnuplot -e "filename='plot_$1'; high='$2'; outputname='$3'" scoreplot.gnu
# for filename in $dir;
#   if [[ $filename = *".sh"* ]]; then
#     continue
#   fi
# #1 ommit :
#   sed 's/"//g' $filename |  awk '/VALID/ {next}' | awk '
# function max(x){i=0;for(val in x){if(i<=x[val]){i=x[val];}}return i;}
# function min(x){i=max(x);for(val in x){if(i>x[val]){i=x[val];}}return i;}
# /^#/{next}
# {a[$2]=$2;next}
# END{minimum=min(a);maximum=max(a);print "Maximum = "maximum " and Minimum = "minimum}'
#   # sed 's/://g' outputs/scores/scimark.lu.large | awk '!/VALID/{print $0}'
# # sed -n -e '/Noncompliant composite result/,$p' $filename &> "${dir}__heap/${truename}.txt"
# for 
# #2 exclude lines with word VALID
# #3 get higher of $1
# #4 write .dat



#   sed 's/://g' scimark.lu.large | awk '!/VALID/{print $0}' | awk '
# function max(x){
#   i=0;
#   for(val in x){
#     if(i<=x[val]){
#       i=x[val];
#     }
#   }
#   return i;
# }
# function min(x){
#   i=max(x);
#   for(val in x){
#     if(i>x[val]){
#       i=x[val];
#     }
#   }return i;
# }
# /^#/{next}
# {a[$2]=$2;print $0;next}
# END{
#   minimum=min(a);
#   maximum=max(a);
#   print "---\nMaximum "maximum "\nMinimum "minimum
# }'


# gnuplot -e "filename='plotdata.dat'; high='100000'" imigration.gnu