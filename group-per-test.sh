# #!/bin/bash
# declare -a samples=("startup.helloworld" "startup.compiler.compiler" "startup.compress" "startup.crypto.aes" "startup.crypto.rsa" "startup.crypto.signverify"
# 			"startup.mpegaudio" "startup.scimark.fft" "startup.scimark.lu" "startup.scimark.monte_carlo" "startup.scimark.sor" 
# 			"startup.scimark.sparse" "startup.serial" "startup.sunflow" "startup.xml.transform" "startup.xml.validation" "compiler.compiler"
# 			"compress" "crypto.aes" "crypto.rsa" "crypto.signverify" "scimark.fft.large" "scimark.lu.large" "scimark.sor.large"
# 			"scimark.sparse.large" "scimark.fft.small" "scimark.lu.small" "scimark.sor.small" "scimark.sparse.small" "scimark.monte_carlo"
# 			"serial" "xml.validation"
# 			)
declare -a samples=("compiler.compiler")
declare -a datafiles=("data4th" "data8th" "dataG1")

mkdir -p per-test

for s in "${samples[@]}"
do
mkdir -p "per-test/${s}"
  for df in "${datafiles[@]}"
  do
    for file in data/$df/$s/* 
      do
      echo $file
      filename=$(basename $file)
      echo $filename
      cp $file per-test/$s/$filename
    done
  done
done