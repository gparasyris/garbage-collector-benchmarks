## Description
  The purpose of this project is to compare different Garbage Collectors using the `SpecJVM2008 benchmark Suit`.
  
### Garbage Collectors tested:
	- Serial
	- CMS
	- G1
	- Parallel

Different parameters were supplied, specified to each Garbage Collector, in order to study the actual impact of said parameters on GC's Performance.

  Inluded Workloads: 
  
  _startup.helloworld, startup.compiler.compiler, startup.compress, startup.crypto.aes, startup.crypto.rsa, startup.crypto.signverify,
   startup.mpegaudio, startup.scimark.fft, startup.scimark.lu, startup.scimark.monte\_carlo, startup.scimark.sor, 
   startup.scimark.sparse, startup.serial, startup.sunflow, startup.xml.transform, startup.xml.validation, compiler.compiler,
   compress, crypto.aes, crypto.rsa, crypto.signverify, scimark.fft.large, scimark.lu.large, scimark.sor.large,
   scimark.sparse.large, scimark.fft.small, scimark.lu.small, scimark.sor.small, scimark.sparse.small, scimark.monte\_carlo,
   serial, xml.validation_


## Requirements:
  - Unix Machine
  - SpecJVM  `curl -s -o SPECjvm2008_1_01_setup.jar http://spec.cs.miami.edu/downloads/osg/java/SPECjvm2008_1_01_setup.jar`
  - Python 3.4+

## How to run:
###	Gather Data:
	`$ ./benchmark_all.sh`

### Parse Data:
 	`$ python3 parser.py` , created files will be landed in output/ directory 

### Plot Data:
	`$ ./plotdata.sh`, inside output/ directory, each folder holds the parsed data and the images, per
	benchmark.

#### - Allocation Failures
  Displaying the sum of Allocation Failures per benchmark per GC (lower is better).

#### - Duration
  Displaying the duration per benchmark per GC (lower is better).

#### - Pause-Duration
  Displaying the part of duration that was spent on GC pauses,  per benchmark per GC.

#### - Pause-Count of GC Pauses
  Displaying amount of time GC Pauses lasted as a total, in accordance with the amount of them,  per benchmark per GC.

#### - Score
  Displaying the score, as it is delivered by SPECjvm2008, per benchmark per GC (higher is better).