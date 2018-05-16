# #!/bin/bash
dd='__'

for dir in */ ; do
    grep -B 2 -A 2 Score  ${dir}__all_totaltimes.txt  &> ${dir}__2.txt
done
