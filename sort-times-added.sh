# #!/bin/bash

# used inside a per-test subdirectory to 
# gather all the total times and scores into one sorted list

mkdir -p "sorted"

for filename in *.txt; do
    awk '$1 ~/__totaltimes/ {printf "%s ",$1} $0 ~/[0-9]{2}:[0-9]{2}:[0-9]{2}/ {printf "%s ",$(NF-2);} $1 ~/Score/  {print $4;}' $filename |  grep -o '+.*' | sort | sed -e '1i\
    GCname  begin end score
    '>> sorted/${filename%.txt}_sorted.txt
done

# awk -F1 '/May/ { for (x=1;x<=NF;x++) if ($x~"May") print $(x+2) }' sorted