import sys  
import os
import re
import subprocess

files = ["startup.helloworld", "startup.compiler.compiler", "startup.compress", "startup.crypto.aes", "startup.crypto.rsa", "startup.crypto.signverify",
                        "startup.mpegaudio", "startup.scimark.fft", "startup.scimark.lu", "startup.scimark.monte_carlo", "startup.scimark.sor", 
                        "startup.scimark.sparse", "startup.serial", "startup.sunflow", "startup.xml.transform", "startup.xml.validation", "compiler.compiler",
                        "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "scimark.fft.large", "scimark.lu.large", "scimark.sor.large",
                        "scimark.sparse.large", "scimark.fft.small", "scimark.lu.small", "scimark.sor.small", "scimark.sparse.small", "scimark.monte_carlo",
                        "serial", "xml.validation"]


def outputToFile(path,filename,value,header):

	with open(os.path.join(path, filename),'a') as f:
		# if( header != "" and os.stat(os.path.join(path, filename)).st_size == 0):
		# 	f.write(header + "\n")
		# if times == -1:
		# 	f.write(gc +":\t" + myinput + "\n")
		# else:
		if( header != "" and os.stat(os.path.join(path, filename)).st_size == 0):
			f.write(header + "\n")
		f.write(value+"\n")
	f.close()

def main():  
	# filepath = sys.argv[1]

	for filepath in files:

		itemList = []
		if not os.path.isfile(filepath):
				print("File path {} does not exist. Exiting...".format(filepath))
				sys.exit()
		# reading a file
		with open(filepath) as fp:
				cnt = 0
				for line in fp:
					if re.match(".*VALID:*",line) or re.match(".*higher*",line):
						continue
					# removing whitespace
					line = re.sub(r"\s+", "", line, flags=re.UNICODE)
					splitted = line.split(":")
					print(splitted)
					outputToFile('./', '__'+filepath+'.dat', splitted[0]+'\t'+splitted[1],"GC\tScore")
					itemList.append(float(splitted[1]))

		print(max(itemList))
		print(min(itemList))
		name="\"filename=\'__startup.xml.transform.dat\'; high=\'"+str(max(itemList))+"\'\""
		a="gnuplot -e {0} scoreplot.gnu".format(name)
		print(a)
		Process = subprocess.Popen('./scoreplot.sh %s %s %s' % (("__"+filepath+".dat"),str(max(itemList)),filepath+"_score.png" ,), shell=True)

if __name__ == '__main__':  
   main()