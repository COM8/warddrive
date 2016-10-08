import subprocess

def parse(scanresult):
	iwlistinput=scanresult.split('\n')
	Theresult = list()
	first=True
	wifi=dict()
	for line in iwlistinput:
		worker=line.lstrip()
		if "Address" in worker:
			if not first:
				Theresult.append(wifi)
				wifi=dict()
			worker=worker.lstrip("Cell ")
			phase=0
			mac=""
			for char in worker:
				if phase==0 and char ==":":
					phase+=1
				elif phase==1:
					phase+=1
				elif phase==2:
					mac+=char
			wifi["mac"]=mac
			first=False
		elif "ESSID" in worker:
			phase=0
			essid=""
			for char in worker:
				if phase==0 and char == '"':
					phase=1
				elif phase==1:
					if char !='"':
						essid+=char
					else:
						break
			wifi["ESSID"]=essid
		elif "Frequency" in worker:
			phase=0
			frequency=""
			channel=""
			for char in worker:
				if char==":" and phase==0:
					phase+=1
				elif phase==1:
					if char!="z":
						frequency+=char
					else:
						frequency+="z"
						phase+=1
				elif phase==2 and char=="l":
					phase+=1
				elif phase==3:
					phase+=1
				elif phase==4 and char !=")":
					channel+=char
			wifi["channel"]=int(channel)
			wifi["frequency"]=frequency
		elif "Encryption" in worker:
			out=""
			phase=0
			for char in worker:
				if phase==0 and char==":":
					phase+=1
				elif phase==1:
					out+=char
			if out == "on":
				wifi["Encryption"]=True
			else:
				wifi["Encryption"]=False
		elif "Bit Rates" in worker:
			phase=0
			rates=""
			for char in worker:
				if phase==0 and char==":":
					phase+=1
				elif phase==1:
					rates+=char
			wifi["Bit Rates"]=rates
		elif "Quality" in worker:
			phase=0
			quality=""
			signallevel=""
			for char in worker:
				if phase==0 and char=="=":
					phase+=1
				elif phase==1:
					if char != " ":
						quality+=char
					else:
						phase+=1
				elif phase==2 and char =="=":
					phase+=1
				elif phase==3:
					if char!=" ":
						signallevel+=char
				wifi["signallevel"]=signallevel
				wifi["quality"]=quality
def scan(interface='wlan0'):
    cmd = ["iwlist", interface, "scan"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    points = proc.stdout.read().decode('utf-8')
    return points

if __name__=="__main__":
	query=""
	with open("file.txt") as f:
		query = f.read()
	parse(query)
	#parse(scan(interface='wlp7s0'))