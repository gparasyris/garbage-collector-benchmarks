import os
import re

#input folders/tests
files = ["startup.helloworld", "startup.compiler.compiler", "startup.compress", "startup.crypto.aes", "startup.crypto.rsa", "startup.crypto.signverify",
                        "startup.mpegaudio", "startup.scimark.fft", "startup.scimark.lu", "startup.scimark.monte_carlo", "startup.scimark.sor", 
                        "startup.scimark.sparse", "startup.serial", "startup.sunflow", "startup.xml.transform", "startup.xml.validation", "compiler.compiler",
                        "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "scimark.fft.large", "scimark.lu.large", "scimark.sor.large",
                        "scimark.sparse.large", "scimark.fft.small", "scimark.lu.small", "scimark.sor.small", "scimark.sparse.small", "scimark.monte_carlo",
                        "serial", "xml.validation"]

#outpus heap/gc results
def outputToFile(path,filename,myinput,gc,times=-1):

	with open(os.path.join(path, filename),'a') as f:
		if times == -1:
			f.write(gc +":" + myinput + "\n")
		else:
			f.write(gc +":" + myinput + " " +str(times)+"\n")
	f.close()

#parses heap values
def heapParse(gc,myfile,filename,path):
	flag = 0
	valid = 1
	htotal = "" #heap
	hused = ""
	etotal = "" #extra values
	eused = ""
	print("Heap:"+gc+":"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			#found heap sizes
			if flag == 1 and "total" in line:
				splitted = line.split(",")
				etotal = splitted[0].split(" ")
				etotal = etotal[len(etotal)-1]
				eused = splitted[1].split(" ")
				eused = eused[2]
				if htotal == "":
					htotal = etotal
					hused = eused
			#G1 case to capture number of young/survivors spaces
			elif flag == 1 and "survivors" in line:
				splitted = line.split(",")
				etotal = splitted[1].split(" ")
				etotal = etotal[1]
				eused = splitted[2].split(" ")
				eused = eused[1]
			#find correct start of parsing
			elif re.match("Noncompliant",line):
				flag = 1
			if "NOT VALID" in line:
				valid = 0
	#format per Garbage collector
	if gc == "Serial":
		correct = "new: "+hused +"/"+htotal+" | tenured: "+ eused +"/"+etotal
	elif "Parallel" in gc:
		correct = "Young: "+hused +"/"+htotal+" | Old: "+ eused +"/"+etotal
	elif "CSM" in gc:
		correct = "new: "+hused +"/"+htotal+" | mark-sweep: "+ eused +"/"+etotal
	elif "G1" in gc:
		correct = hused +"/"+htotal+ " | " +etotal + " " +eused
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc
	outputToFile("outputs/heap/",myfile,correct,gc)

#parse GCs for count/times
def GCparseFile(gc,myfile,filename,path):
	flag = 0
	usert = 0
	syst = 0
	realt = 0
	gcpause = 0
	cms_mark = 0
	valid = 1
	print("GC:"+gc+":"+path+filename)
	with open(os.path.join(path, filename), 'r') as f:
		for line in f:
			if flag == 1 and re.match(".*\[Times: user=*",line):
				gcpause += 1
				splitted = line.split("[")
				correct = splitted[len(splitted)-1]
				times = re.split('[= ,]',correct)
				usert += float(times[2])
				syst += float(times[4])
				realt += float(times[7])
			elif re.match("Warmup \(.*\) result:",line):
				flag = 1
			if "NOT VALID" in line:
				valid = 0
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc
	correct = "{:.2f}".format(usert)+" "+"{:.2f}".format(syst)+" "+"{:.2f}".format(realt)
	outputToFile("outputs/gc/",myfile,correct,gc,gcpause)

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

def openFile():
	#create folders if not there
	try:
		os.makedirs(os.path.dirname("outputs/heap/"))
		os.makedirs(os.path.dirname("outputs/gc/"))
	except FileExistsError:
		pass
	#iterate over folders/tests
	for myfile in files:
		path = myfile+"/"
		try:
			#iterate over testfiles
			for filename in os.listdir(path):
				if re.match(".*G1GC*", filename):
					if "TH=4" in filename:
						if "_1MB" in filename:
							heapParse("G1-4-1",myfile,filename,path)
						elif "_8MB" in filename:
							heapParse("G1-4-8",myfile,filename,path)
						elif "_16MB" in filename:
							heapParse("G1-4-16",myfile,filename,path)
						elif "_32MB" in filename:
							heapParse("G1-4-32",myfile,filename,path)
					else:
						if "_1MB" in filename:
							heapParse("G1-8-1",myfile,filename,path)
						elif "_8MB" in filename:
							heapParse("G1-8-8",myfile,filename,path)
						elif "_16MB" in filename:
							heapParse("G1-8-16",myfile,filename,path)
						elif "_32MB" in filename:
							heapParse("G1-8-32",myfile,filename,path)
				elif re.match(".*ConcMark*",filename):
					if "4_threads" in filename:
						heapParse("CSM-4",myfile,filename,path)
					elif "8_threads" in filename:
						heapParse("CSM-8",myfile,filename,path)
				elif re.match(".*SerialGc*",filename):
					GCparseFile("Serial",myfile,filename,path)
					heapParse("Serial",myfile,filename,path)
				elif re.match(".*ParallelOldGC*",filename):
					if "4_threads" in filename:
						GCparseFile("Parallel-4",myfile,filename,path)
						heapParse("Parallel-4",myfile,filename,path)
					elif "8_threads" in filename:
						GCparseFile("Parallel-8",myfile,filename,path)
						heapParse("Parallel-8",myfile,filename,path)
				else:
					print("couldnt handle "+filename)	
		except FileNotFoundError:
			print("folder:"+myfile+" not found")
		

openFile()