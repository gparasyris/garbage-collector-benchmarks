import sys  
import os
import re
import subprocess
import shutil

# should be placed inside outputs/
files = ["startup.helloworld", "startup.compiler.compiler", "startup.compress", "startup.crypto.aes", "startup.crypto.rsa", "startup.crypto.signverify",
                        "startup.mpegaudio", "startup.scimark.fft", "startup.scimark.lu", "startup.scimark.monte_carlo", "startup.scimark.sor", 
                        "startup.scimark.sparse", "startup.serial", "startup.sunflow", "startup.xml.transform", "startup.xml.validation", "compiler.compiler",
                        "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "scimark.fft.large", "scimark.lu.large", "scimark.sor.large",
                        "scimark.sparse.large", "scimark.fft.small", "scimark.lu.small", "scimark.sor.small", "scimark.sparse.small", "scimark.monte_carlo",
                        "serial", "xml.validation"]


def silentremove(filename):
		try:
			shutil.rmtree(filename, ignore_errors=True, onerror=None)
		except FileExistsError as err:
			print("folder:"+filename+" not found")

def outputToFile(path,filename,value,header):

	with open(os.path.join(path, filename),'a') as f:
		# print("in open")
		# if( header != "" and os.stat(os.path.join(path, filename)).st_size == 0):
		# 	f.write(header + "\n")
		# if times == -1:
		# 	f.write(gc +":\t" + myinput + "\n")
		# else:
		if( header != "" and os.stat(os.path.join(path, filename)).st_size == 0):
			f.write(header + "\n")
		f.write(value)
	f.close()

def main():  
	# filepath = sys.argv[1]
	try:
		silentremove(os.path.dirname("pause-duration/"))
		os.makedirs(os.path.dirname("pause-duration/"))
	except FileExistsError:
		pass

	for filepath in files:

		itemList = []
		if not os.path.isfile("duration/"+filepath):
				print("File path {} does not exist. Exiting...".format(filepath))
				sys.exit()
		# reading a file
		#!!
		Process = subprocess.Popen('./pause-duration-concat.sh %s %s %s' % ( "gc/"+filepath, "duration/"+filepath, "pause-duration/"+filepath ,), shell=True)
		Process.wait()
		# print(filepath)
		with open("pause-duration/"+filepath) as fp:
				# print("here")
				cnt = 0
				for line in fp:
					# print(line)
					if re.match(".*VALID:*",line) or re.match(".*userT*",line) or re.match(".*NOT*", line):
						continue
					# removing whitespace
					# line = re.sub(r"\s+", "", line, flags=re.UNICODE)
					splitted = line.split(":")
					# print(splitted)
					# print("before open")
					outputToFile('./pause-duration/', '__'+filepath+'.dat', splitted[0]+'\t'+splitted[1],"GC\tPause\tDuration \t")
					number = re.sub(r"\s+", "", splitted[1].split(" ")[-1], flags=re.UNICODE)
					itemList.append(float(number))
					# print(number)
					# print(max(itemList))
		high = 0
		if(max(itemList)<100):
			high = max(itemList) +3
		else:
			high = 300
		# print(high)
		# print(max(itemList))
		Process2 = subprocess.Popen('./pause-duration.sh %s %s %s %s' % (("./pause-duration/__"+filepath+".dat"),str(high),"./pause-duration/__"+filepath+"_pause-duration_.png", str(min(itemList)) ,), shell=True)
		Process2.wait()
if __name__ == '__main__':  
   main()
	 