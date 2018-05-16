# #!/bin/bash
dd='__'

mkdir -p "__all_times"


for dir in */ ; do
    echo ${dir}
    testfile=$(echo "$dir" | cut -d "/" -f1)
    echo $testfile
    mv "${testfile}/${testfile}_all_total_times.txt" "__all_times/${testfile}_all_total_times.txt"
done
