## Description


## Requirements:
  - Unix Machine
  - SpecJVM  `curl -s -o SPECjvm2008_1_01_setup.jar http://spec.cs.miami.edu/downloads/osg/java/SPECjvm2008_1_01_setup.jar`
  - Python 3.4+

## How to run:
  ###	Gather Data:
	`$ ./benchmark_G1.sh && ./benchmark_Serial && ./benchmark_rest.sh`

  ### Parse Data:
 	`$ python3 parser.py` , created files will be landed in output/ directory 

### Plot Data:
	`$ ./plotdata.sh`, inside output/ directory, each folder holds the parsed data and the images, per
	benchmark.