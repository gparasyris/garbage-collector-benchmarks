#!/bin/bash
# initial script to gather heap-data
for dir in */ ; do
    echo "******: $dir"
    for filename in $dir*.txt; do
        if [[ $filename = *"__"* ]]; then
            continue
        fi
        # echo $filename
        #  grep "SPECjvm2008" < $filename
        name2=${filename%.txt}
        name=${name2// /_}
        truename=$(basename "${filename%.*}")
        mkdir -p "${dir}__heap"
        # get gc-pause time lines
        # awk '/GC pause|Full GC|Parallel Time:|Eden:|Times:/{ print $0 }' $filename  &> "__${name}/3_gc-pause.txt"
        # get everything arround garbage-first heap annotation
        sed -n -e '/Noncompliant composite result/,$p' $filename &> "${dir}__heap/${truename}.txt"
        # get all the begins ends in file
        # awk '/begins:|ends:|Score on/{ print $0 }' $filename  &> "${dir}__heap/${truename}.txt"
    done
    # awk 'FNR==1{print "--------------------------"}1' $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
    # cat $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
    # echo "######: ${dir}0_${dir::-1}_all.txt"
    # echo $(ls ${dir})
    rm "${dir}__all_heap.txt"


    for filename in ${dir}__heap/*.txt; do
        # each time through the loop, ${filename} will hold the name
        # of the next *.txt file.  You can then arbitrarily process
        # each file
        var="$(cat ${filename})" 
        echo "
${filename}

${var}"

    # You can add redirection after the done (which ends the
    # for loop).  Any output within the for loop will be sent to
    # the redirection specified here
    done >> ${dir}__all_heap.txt
done
