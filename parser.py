import os
import re

files = ["startup.helloworld", "startup.compiler.compiler", "startup.compress", "startup.crypto.aes", "startup.crypto.rsa", "startup.crypto.signverify",
                        "startup.mpegaudio", "startup.scimark.fft", "startup.scimark.lu", "startup.scimark.monte_carlo", "startup.scimark.sor", 
                        "startup.scimark.sparse", "startup.serial", "startup.sunflow", "startup.xml.transform", "startup.xml.validation", "compiler.compiler",
                        "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "scimark.fft.large", "scimark.lu.large", "scimark.sor.large",
                        "scimark.sparse.large", "scimark.fft.small", "scimark.lu.small", "scimark.sor.small", "scimark.sparse.small", "scimark.monte_carlo",
                        "serial", "xml.validation"]

def outputToFile(path,filename,myinput,gc,times):
	with open(os.path.join(path, filename),'a') as f:
		f.write(gc +": [" + myinput + "] in seconds with " +str(times)+" invokations \n")
	f.close()

def parseFile(gc,myfile,filename,path):
	flag = 0
	usert = 0
	syst = 0
	realt = 0
	gcpause = 0
	cms_mark = 0
	valid = 1
	print(gc+":"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			if re.match(".*\[Times: user=*",line) and flag == 1:
				gcpause += 1
				splitted = line.split("[")
				correct = splitted[len(splitted)-1]
				times = re.split('[= ,]',correct)
				usert += float(times[2])
				syst += float(times[4])
				realt += float(times[7])
			if re.match("Warmup \(.*\) result:",line):
				flag = 1
			if "NOT VALID" in line:
				valid = 0
	if valid == 0:
		gc = "NOT VALID-"+gc
	correct = "user:"+"{:.2f}".format(usert)+" system:"+"{:.2f}".format(syst)+" real:"+"{:.2f}".format(realt)
	outputToFile("outputs/",myfile,correct,gc,gcpause)

def G1read(myfile,filename,path):
	flag = 0
	print("G1:"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			pass

def CSMread(myfile,filename,path):
	print("CSM:"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			pass

def Parallelread(myfile,filename,path):
	print("Parallel:"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			pass


def openFile():
	for myfile in files:
		path = myfile+"/"
		try:
			for filename in os.listdir(path):
				if re.match(".*G1GC*", filename):
					G1read(myfile,filename,path)
				elif re.match(".*ConcMark*",filename):
					CSMread(myfile,filename,path)
				elif re.match(".*SerialGc*",filename):
					parseFile("Serial",myfile,filename,path)
				elif re.match(".*ParallelOldGC*",filename):
					if "4_threads" in filename:
						parseFile("Parallel-4",myfile,filename,path)
					elif "8_threads" in filename:
						parseFile("Parallel-8",myfile,filename,path)
				else:
					print("couldnt handle "+filename)	
		except FileNotFoundError:
			print("file:"+myfile+" not found")
		

openFile()