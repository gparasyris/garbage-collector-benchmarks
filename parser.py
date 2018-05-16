import os
import re
import shutil
import subprocess
from datetime import datetime

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
			f.write(gc +":\t" + myinput + "\n")
		else:
			f.write(gc +":\t" + myinput + " " +str(times)+"\n")
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
			#if not in warmup
			if flag == 1:
				# G1 case
				if re.match("G1", gc):
					if re.match(".*GC pause*",line) or re.match(".*Full GC*",line):
							j = i
							while True:
								if re.match(".*\[Times: user=*",lines[j]):
									gcpause += 1
									splitted = lines[j].split("[")
									correct = splitted[len(splitted)-1]
									times = re.split('[= ,]',correct)
									# print("\t"+times[2]+"\t"+times[4]+"\t"+times[7])
									usert += float(times[2])
									syst += float(times[4])
									realt += float(times[7])
									# print("\t"+str(usert)+"\t"+str(syst)+"\t"+str(realt))
									break
								j+=1
				# CMS case
				elif re.match("CSM", gc):
					# print("in CSM now..")
					if any (re.match(regex, line) for regex in [".*CMS Initial Mark*", ".*CMS Final Remark*", ".*concurrent mode failure*"]): #re.match(".*GC pause*",line):
					# print(i)
					# if re.match(".*CMS Initial Mark*",line) or re.match(".*CMS Initial Mark*",line):
						# print("found initial mark")
						gcpause += 1
						# gcpause += 1
						splitted = line.split("[")
						correct = splitted[len(splitted)-1]
						times = re.split('[= ,]',correct)
						usert += float(times[2])
						syst += float(times[4])
						realt += float(times[7])
				# Parallel/Serial
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
	outputToFile("outputs/gc/",myfile,correct,gc,gcpause,"#\tgc\tuserT\tsysT\trealT\tgcCount")

# Get Scores
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

#parse GC Allocation Failures for count/times
def GCAllocationFailures(gc,myfile,filename,path):
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
	afCounter = 0
	with open(os.path.join(path, filename), 'r') as f:
		lines = f.readlines()
		for i,line in enumerate(lines):
			# if(skipRest):
				# break
			if flag == 1 or re.match(".*startup*", filename):
				# if score is in line get the second to last column of that line
				if re.match(".*Allocation Failure*",line):
					# splitted = line.split(" ")
					# correct += splitted[len(splitted)-2]
					# skipRest = True
					afCounter+=1
			elif re.match("Warmup \(.*\) result:",line):
				flag = 1
			if "NOT VALID" in line:
				valid = 0
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc
	# correct = "{:.2f}".format(usert)+" "+"{:.2f}".format(syst)+" "+"{:.2f}".format(realt)
	outputToFile("outputs/allocation_failures/",myfile,str(afCounter),gc,-1,"#\tAllocation Failures")

# with open(os.path.join(path, filename), 'r') as f:
# 		lines = f.readlines()
# 		for i,line in enumerate(lines):
# 			if(skipRest):
# 				break
# 			if flag == 1 or re.match(".*startup*", filename):
# 				# if score is in line get the second to last column of that line
# 				if re.match(".*Allocation Failure*",line):
# 					# splitted = line.split(" ")
# 					# correct += splitted[len(splitted)-2]
# 					# skipRest = True
# 					afCounter+=1
# 			elif re.match("Warmup \(.*\) result:",line):
# 				flag = 1
# 			if "NOT VALID" in line:
# 				valid = 0
# 	#check if valid testfile
# 	if valid == 0:
# 		gc = "NOT VALID-"+gc
# 	# correct = "{.2f}.format(afCounter)"
# 	# correct = "{:.2f}".format(usert)+" "+"{:.2f}".format(syst)+" "+"{:.2f}".format(realt)
# 	outputToFile("outputs/allocation_failures/",myfile,afCounter,gc,-1,"#\tAllocation Failures")

#	a			b	d		H:M:S
# Sun May 13 18:52:30 EEST 2018
# **** Sun May 13 00:47:19 ****
def __datetime(date_str):
	# print("****"+date_str+"****")
	return datetime.strptime(date_str, ' %a %b %d %H:%M:%S ')

# Get duration of benchmark
def parseTimes(gc,myfile,filename,path):
	flag = 0
	begins = ""
	ends = ""
	# usert = 0
	# syst = 0
	# realt = 0
	# gcpause = 0
	# cms_mark = 0
	valid = 1
	# print("GC:"+gc+":"+path+filename)
	# correct = "\t"
	# skipRest = False
	# afCounter = 0
	with open(os.path.join(path, filename), 'r') as f:
		lines = f.readlines()
		for i,line in enumerate(lines):
			if re.match(".*begins:*",line):
				splitted = line.split(":",1)
				begins = splitted[1].split("EEST",1)[0]
				# print(__datetime(begins))
			if re.match(".*ends:*",line):
				splitted = line.split(":", 1)
				ends = splitted[1].split("EEST",1)[0]
			if "NOT VALID" in line:
				valid = 0
	#check if valid testfile
	if valid == 0:
		gc = "NOT VALID-"+gc

		# start = __datetime(start_date)
		# end = __datetime(end_date)

	delta = __datetime(ends) - __datetime(begins)
		#print delta  # prints: 1 day, 7:50:05
		#print delta.total_seconds()  # prints: 114605.0
	outputToFile("outputs/duration/",myfile, str(delta.total_seconds()),gc,-1,"#\tAllocation Failures")

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

def	parseAllData(title,myfile,filename,path):
	GCparseFile(title,myfile,filename,path)
	heapParse(title,myfile,filename,path)
	ScoreParse(title,myfile,filename,path)
	GCAllocationFailures(title,myfile,filename,path)
	parseTimes(title,myfile,filename,path)

def openFile():
	#create folders if not there
	try:
		silentremove(os.path.dirname("outputs/gc/"))
		silentremove(os.path.dirname("outputs/heap/"))
		silentremove(os.path.dirname("outputs/scores/"))
		silentremove(os.path.dirname("outputs/allocation_failures/"))
		silentremove(os.path.dirname("outputs/duration/"))
		os.makedirs(os.path.dirname("outputs/heap/"))
		os.makedirs(os.path.dirname("outputs/gc/"))
		os.makedirs(os.path.dirname("outputs/scores/"))
		os.makedirs(os.path.dirname("outputs/allocation_failures/"))
		os.makedirs(os.path.dirname("outputs/duration/"))
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
								parseAllData("G1-4-1",myfile,filename,path)
								# heapParse("G1-4-1",myfile,filename,path)
								# ScoreParse("G1-4-1",myfile,filename,path)
								# GCAllocationFailures("G1-4-1",myfile,filename,path)
							elif "_8MB" in filename:
								parseAllData("G1-4-8",myfile,filename,path)
								# heapParse("G1-4-8",myfile,filename,path)
								# ScoreParse("G1-4-8",myfile,filename,path)
								# GCAllocationFailures("G1-4-8",myfile,filename,path)
							elif "_16MB" in filename:
								parseAllData("G1-4-16",myfile,filename,path)
								# heapParse("G1-4-16",myfile,filename,path)
								# ScoreParse("G1-4-16",myfile,filename,path)
								# GCAllocationFailures("G1-4-16",myfile,filename,path)
							elif "_32MB" in filename:
								parseAllData("G1-4-32",myfile,filename,path)
								# heapParse("G1-4-32",myfile,filename,path)
								# ScoreParse("G1-4-32",myfile,filename,path)
								# GCAllocationFailures("G1-4-32",myfile,filename,path)
						else:
							if "_1MB" in filename:
								parseAllData("G1-8-1",myfile,filename,path)
								# heapParse("G1-8-1",myfile,filename,path)
								# ScoreParse("G1-8-1",myfile,filename,path)
								# GCAllocationFailures("G1-8-1",myfile,filename,path)
							elif "_8MB" in filename:
								parseAllData("G1-8-8",myfile,filename,path)
								# heapParse("G1-8-8",myfile,filename,path)
								# ScoreParse("G1-8-8",myfile,filename,path)
								# GCAllocationFailures("G1-8-8",myfile,filename,path)
							elif "_16MB" in filename:
								parseAllData("G1-8-16",myfile,filename,path)
								# heapParse("G1-8-16",myfile,filename,path)
								# ScoreParse("G1-8-15",myfile,filename,path)
								# GCAllocationFailures("G1-8-16",myfile,filename,path)
							elif "_32MB" in filename:
								parseAllData("G1-8-32",myfile,filename,path)
								# heapParse("G1-8-32",myfile,filename,path)
								# ScoreParse("G1-8-32",myfile,filename,path)
								# GCAllocationFailures("G1-8-32",myfile,filename,path)
				elif re.match(".*ConcMark*",filename):
					if "4_threads" in filename:
						parseAllData("CSM-4",myfile,filename,path)
						# heapParse("CSM-4",myfile,filename,path)
						# ScoreParse("CSM-4",myfile,filename,path)
						# GCAllocationFailures("CSM-4",myfile,filename,path)
					elif "8_threads" in filename:
						parseAllData("CSM-8",myfile,filename,path)
						# heapParse("CSM-8",myfile,filename,path)
						# ScoreParse("CSM-8",myfile,filename,path)
						# GCAllocationFailures("CSM-8",myfile,filename,path)
				elif re.match(".*SerialGc*",filename):
					parseAllData("Serial",myfile,filename,path)
					# heapParse("Serial",myfile,filename,path)
					# ScoreParse("Serial",myfile,filename,path)
					# GCAllocationFailures("Serial",myfile,filename,path)
				elif re.match(".*ParallelOldGC*",filename):
					if "4_threads" in filename:
						parseAllData("Parallel-4",myfile,filename,path)
						# heapParse("Parallel-4",myfile,filename,path)
						# ScoreParse("Parallel-4",myfile,filename,path)
						# GCAllocationFailures("Parallel-4",myfile,filename,path)
					elif "8_threads" in filename:
						parseAllData("Parallel-8",myfile,filename,path)
						# heapParse("Parallel-8",myfile,filename,path)
						# ScoreParse("Parallel-8",myfile,filename,path)
						# GCAllocationFailures("Parallel-8",myfile,filename,path)
				else:
					print("couldnt handle "+filename)	
		except FileExistsError as err:
			print("folder:"+myfile+" not found")
		

openFile()