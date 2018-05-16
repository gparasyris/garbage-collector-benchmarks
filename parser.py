import os
import re
import shutil
import subprocess

#input folders/tests
files = ["startup.helloworld", "startup.compiler.compiler", "startup.compress", "startup.crypto.aes", "startup.crypto.rsa", "startup.crypto.signverify",
                        "startup.mpegaudio", "startup.scimark.fft", "startup.scimark.lu", "startup.scimark.monte_carlo", "startup.scimark.sor", 
                        "startup.scimark.sparse", "startup.serial", "startup.sunflow", "startup.xml.transform", "startup.xml.validation", "compiler.compiler",
                        "compress", "crypto.aes", "crypto.rsa", "crypto.signverify", "scimark.fft.large", "scimark.lu.large", "scimark.sor.large",
                        "scimark.sparse.large", "scimark.fft.small", "scimark.lu.small", "scimark.sor.small", "scimark.sparse.small", "scimark.monte_carlo",
                        "serial", "xml.validation"]

# deletes a directory if exists
def silentremove(filename):
		try:
			shutil.rmtree(filename, ignore_errors=True, onerror=None)
		except FileExistsError as err:
			print("folder:"+filename+" not found")

#outpus heap/gc results
def outputToFile(path,filename,myinput,gc,times=-1, header=""):

	with open(os.path.join(path, filename),'a') as f:
		if( header != "" and os.stat(os.path.join(path, filename)).st_size == 0):
			f.write(header + "\n")
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
		correct = hused +"/"+htotal+ " | " +eused + " " +etotal
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc
	outputToFile("outputs/heap/",myfile,correct,gc,-1,"#\tHused\tHtotal\tEused\tEtotal")

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
		lines = f.readlines()
		for i,line in enumerate(lines):
			if flag == 1:
				if re.match("G1", gc):
					if re.match(".*GC pause*",line):
							j = i
							while True:
								if re.match(".*\[Times: user=*",lines[j]):
									gcpause += 1
									splitted = lines[j].split("[")
									correct = splitted[len(splitted)-1]
									times = re.split('[= ,]',correct)
									usert += float(times[2])
									syst += float(times[4])
									realt += float(times[7])
									break
								j+=1
			elif re.match(".*\[Times: user=*",line):
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
	outputToFile("outputs/gc/",myfile,correct,gc,gcpause,"#\tgc\tuserT\tsysT\tealT\tgcCount")

def ScoreParse(gc,myfile,filename,path):
	flag = 0
	usert = 0
	syst = 0
	realt = 0
	gcpause = 0
	cms_mark = 0
	valid = 1
	print("GC:"+gc+":"+path+filename)
	correct = "\t"
	skipRest = False
	with open(os.path.join(path, filename), 'r') as f:
		lines = f.readlines()
		for i,line in enumerate(lines):
			if(skipRest):
				break
			if flag == 1 or re.match(".*startup*", filename):
				# if score is in line get the second to last column of that line
				if re.match(".*Score*",line):
					splitted = line.split(" ")
					correct += splitted[len(splitted)-2]
					skipRest = True
			elif re.match("Warmup \(.*\) result:",line):
				flag = 1
			if "NOT VALID" in line:
				valid = 0
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc
	# correct = "{:.2f}".format(usert)+" "+"{:.2f}".format(syst)+" "+"{:.2f}".format(realt)
	outputToFile("outputs/scores/",myfile,correct,gc,-1,"#\tscore (higher is better)")




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
		silentremove(os.path.dirname("outputs/gc/"))
		silentremove(os.path.dirname("outputs/heap/"))
		silentremove(os.path.dirname("outputs/scores/"))
		os.makedirs(os.path.dirname("outputs/heap/"))
		os.makedirs(os.path.dirname("outputs/gc/"))
		os.makedirs(os.path.dirname("outputs/scores/"))
	except FileExistsError:
		pass
	#iterate over folders/tests
	for myfile in files:
		path = myfile+"/"
		try:
			#iterate over testfiles
			for filename in os.listdir(path):
				if re.match(".*G1GC*", filename):
					with open(os.path.join(os.path.dirname("outputs/gc/"), "temp_g1"), 'wb')	as	tf:
						subprocess.call(["awk", '/GC pause/{nr[NR]; nr[NR+25]; nr[NR+26]}; NR in nr', os.path.join(path, filename)], stdout=tf)
						if "TH=4" in filename:
							if "_1MB" in filename:
								# GCparseFile("G1-4-1","temp_g1","temp_g1",os.path.dirname("outputs/gc/"))
								GCparseFile("G1-4-1",myfile,filename,path)
								heapParse("G1-4-1",myfile,filename,path)
								ScoreParse("G1-4-1",myfile,filename,path)
							elif "_8MB" in filename:
								GCparseFile("G1-4-8",myfile,filename,path)
								heapParse("G1-4-8",myfile,filename,path)
								ScoreParse("G1-4-8",myfile,filename,path)
							elif "_16MB" in filename:
								GCparseFile("G1-4-16",myfile,filename,path)
								heapParse("G1-4-16",myfile,filename,path)
								ScoreParse("G1-4-16",myfile,filename,path)
							elif "_32MB" in filename:
								GCparseFile("G1-4-32",myfile,filename,path)
								heapParse("G1-4-32",myfile,filename,path)
								ScoreParse("G1-4-32",myfile,filename,path)
						else:
							if "_1MB" in filename:
								GCparseFile("G1-8-1",myfile,filename,path)
								heapParse("G1-8-1",myfile,filename,path)
								ScoreParse("G1-8-1",myfile,filename,path)
							elif "_8MB" in filename:
								GCparseFile("G1-8-8",myfile,filename,path)
								heapParse("G1-8-8",myfile,filename,path)
								ScoreParse("G1-8-8",myfile,filename,path)
							elif "_16MB" in filename:
								GCparseFile("G1-8-16",myfile,filename,path)
								heapParse("G1-8-16",myfile,filename,path)
								ScoreParse("G1-8-15",myfile,filename,path)
							elif "_32MB" in filename:
								GCparseFile("G1-8-32",myfile,filename,path)
								heapParse("G1-8-32",myfile,filename,path)
								ScoreParse("G1-8-32",myfile,filename,path)
				elif re.match(".*ConcMark*",filename):
					if "4_threads" in filename:
						# GCparseFile("CSM-4",myfile,filename,path)
						heapParse("CSM-4",myfile,filename,path)
						ScoreParse("CSM-4",myfile,filename,path)
					elif "8_threads" in filename:
						# GCparseFile("CSM-8",myfile,filename,path)
						heapParse("CSM-8",myfile,filename,path)
						ScoreParse("CSM-8",myfile,filename,path)
				elif re.match(".*SerialGc*",filename):
					GCparseFile("Serial",myfile,filename,path)
					heapParse("Serial",myfile,filename,path)
					ScoreParse("Serial",myfile,filename,path)
				elif re.match(".*ParallelOldGC*",filename):
					if "4_threads" in filename:
						GCparseFile("Parallel-4",myfile,filename,path)
						heapParse("Parallel-4",myfile,filename,path)
						ScoreParse("Parallel-4",myfile,filename,path)
					elif "8_threads" in filename:
						GCparseFile("Parallel-8",myfile,filename,path)
						heapParse("Parallel-8",myfile,filename,path)
						ScoreParse("Parallel-8",myfile,filename,path)
				else:
					print("couldnt handle "+filename)	
		except FileExistsError as err:
			print("folder:"+myfile+" not found")
		

openFile()