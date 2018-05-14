# #!/bin/bash

# # find . -name "*.txt" -print0 | while read -d $'\0' file
# # do
# #     grep "SPECjvm2008" "$file" &> aaareader$file.txt
# #     # echo "$file"
# # done

# for filename in *.txt; do
#     # echo $filename
#     #  grep "SPECjvm2008" < $filename
#     name2=${filename%.txt}
#     name=${name2// /_}
#     mkdir -p "__${name}"
#     # get gc-pause time lines
#     awk '/GC pause|Full GC|Parallel Time:|Eden:|Times:/{ print $0 }' $filename  &> "__${name}/3_gc-pause.txt"
#     # get everything arround garbage-first heap annotation
#     sed -n -e '/Noncompliant composite result/,$p' $filename &> "__${name}/1_heap.txt"
#     # get all the begins ends in file
#     awk '/begins:|ends:|Score on/{ print $0 }' $filename  &> "__${name}/2_totaltimes.txt"

# done

# for dir in */ ; do
#     echo "******: $dir"
#     awk 'FNR==1{print "--------------------------"}1' $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
#     # cat $dir/*.txt > "${dir}0_${dir::-1}_all.txt"
#     # echo "######: ${dir}0_${dir::-1}_all.txt"
#     # echo $(ls ${dir})
# done


# # for dir 
#     #mkdir heap/
#     #for .txt
#     # get heap, add inside heap



#!/bin/bash

# # find . -name "*.txt" -print0 | while read -d $'\0' file
# # do
# #     grep "SPECjvm2008" "$file" &> aaareader$file.txt
# #     # echo "$file"
# # done

# for filename in *.txt; do
#     # echo $filename
#     #  grep "SPECjvm2008" < $filename
#     name2=${filename%.txt}
#     name=${name2// /_}
#     mkdir -p "__${name}"
#     # get gc-pause time lines
#     awk '/GC pause|Full GC|Parallel Time:|Eden:|Times:/{ print $0 }' $filename  &> "__${name}/3_gc-pause.txt"
#     # get everything arround garbage-first heap annotation
#     sed -n -e '/Noncompliant composite result/,$p' $filename &> "__${name}/1_heap.txt"
#     # get all the begins ends in file
#     awk '/begins:|ends:|Score on/{ print $0 }' $filename  &> "__${name}/2_totaltimes.txt"
# done
dd='__'

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
