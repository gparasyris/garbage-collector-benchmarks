# variables:
  # filename
  # high
  # title

set terminal png  enhanced font "arial,27" fontscale 1.0 size 1920, 1080 
#set term postscript enhanced eps #fontsize

set output outputname
set border 3 front lt black linewidth 1.000 dashtype solid
set boxwidth 0.8 absolute
set style fill   solid 1.00 noborder
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics nortics nomrtics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
# set grid layerdefault   lt 0 linecolor 0 linewidth 0.500,  lt 0 linecolor 0 linewidth 0.500
set key bmargin center horizontal Left reverse noenhanced autotitle columnhead nobox
set style histogram rowstacked title textcolor lt -1 offset character 2, 0.25
set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45  autojustify
set xtics  norangelimit  #font ",8"
set xtics   ()
set ytics border in scale 0,0 mirror norotate  autojustify
set ytics  norangelimit autofreq  #font ",8"
set ztics border in scale 0,0 nomirror norotate  autojustify
set cbtics border in scale 0,0 mirror norotate  autojustify
set rtics axis in scale 0,0 nomirror norotate  autojustify
# set title "Immigration from different regions\n(give each histogram a separate title)" 
# set xlabel "(Same plot using rowstacked rather than clustered histogram)" 
set xlabel  offset character 0, -2, 0 font "" textcolor lt -1 norotate
# set ylabel "Immigration by decade" 
set linetype 1 lc rgb 'green'
set yrange [ 0.00000 : high ] noreverse nowriteback
DEBUG_TERM_HTIC = 119
DEBUG_TERM_VTIC = 119
## Last datafile plotted: "immigration.dat"
#plot newhistogram "Northern Europe", 'immigration.dat' using "Sweden":xtic(1) t col, '' u "Denmark" t col, '' u "Norway" t col, newhistogram "Southern Europe", '' u "Greece":xtic(1) t col, '' u "Romania" t col, '' u "Yugoslavia" t col, newhistogram "British Isles", '' u "Ireland":xtic(1) t col, '' u "United_Kingdom" t col
plot newhistogram, filename using "Allocion_Failures":xtic(1) t col linecolor rgb "#1A5CEC"#, '' u "DIFF" t col #, '' u "Norway" t col 
#plot filename using 2:xtic(1) ti "Speedup" linecolor rgb "#1A5CEC"