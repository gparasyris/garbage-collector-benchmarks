1. awk script 
  - paused time / duration
    - a: ouputpus/gc/testfile col0 col3
    - b: ouputpus/duration/testfile col0 col1
    - if !"Valid" print col0 col3/col1
  - paused time / realtime
    - a: ouputpus/gc/testfile col0 col3
    - b: ouputpus/duration/testfile col0 col1
    - if !"Valid" print col0 col3/col1


General Plots:

  - Scores per output/scores/testfile (2 cols only)
  - Allocation Failures per output/allocation_failures/testfile (2 cols only)

G1 Specific
  -  young + survivor


CMS/Parallel/Serial
  eden & from space 



  |
  |
  |
  |
  |
  |
  |
  | _____||______||_____||____||___________________________
      G1/4/8    


python3 scoreplot.py inside scores folder
rm -rf *__* *.png