# #!/bin/bash
python3 allocationFailures.py
./count-pause.sh
python3 durationplot.py
python3 pause-duration.py
python3 scoreplot.py
