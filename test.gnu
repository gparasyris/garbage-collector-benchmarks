set terminal postscript       # (These commented lines would be used to )
set output  "d1_plot2.ps" #   (generate a postscript file.            )
set title "Energy vs. Time for Sample Data"
set xlabel "Time"
set ylabel "Energy"
plot "d1.dat" with lines
pause -1 "Hit any key to continue"