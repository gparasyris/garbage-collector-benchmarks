# #!/bin/bash
# should be copied inside per-test

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
        testfile=$(echo "$dir" | cut -d "/" -f1)
        mkdir -p "${dir}__totaltimes"
        # get gc-pause time lines
        # awk '/GC pause|Full GC|Parallel Time:|Eden:|Times:/{ print $0 }' $filename  &> "__${name}/3_gc-pause.txt"
        # get everything arround garbage-first heap annotation
        # sed -n -e '/Noncompliant composite result/,$p' $filename &> "__${name}/1_heap.txt"
        # get all the begins ends in file
        awk '/begins:|ends:|Score on/{ print $0 }' $filename  &> "${dir}__totaltimes/${truename}.txt"
    done
    # awk 'FNR==1{print "--------------------------"}1' $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
    # cat $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
    # echo "######: ${dir}0_${dir::-1}_all.txt"
    # echo $(ls ${dir})
    rm "${dir}__all_totaltimes.txt"


    for filename in ${dir}__totaltimes/*.txt; do
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
    done >> ${dir}__all_totaltimes.txt
done


# trying to gather only related data (2 rows before 2 rows after)

for dir in */ ; do
    grep -B 2 -A 2 Score  ${dir}__all_totaltimes.txt  &> ${dir}__all_totaltimes.txt
done



# re-structuring data
mkdir -p "__all_times"


for dir in */ ; do
    echo ${dir}
    testfile=$(echo "$dir" | cut -d "/" -f1)
    echo $testfile
    mv "${testfile}/${testfile}_all_total_times.txt" "__all_times/${testfile}_all_total_times.txt"
done