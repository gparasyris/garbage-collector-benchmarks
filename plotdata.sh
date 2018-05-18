# #!/bin/bash
python3 generate-plots/allocationFailures.py
./generate-plots/count-pause.sh
python3 generate-plots/durationplot.py
python3 generate-plots/pause-duration.py
python3 generate-plots/scoreplot.py
