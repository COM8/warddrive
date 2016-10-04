import pickle
import sys
if __name__=="__main__":
	try:
		with open("logFile" + '.pkl', 'rb') as f:
			loggedData = pickle.load(f)
		if len(sys.argv)>=2:
			Thelist=sys.argv
			Thelist.remove("filter.py")			
			for key, value in loggedData.items():
				for output in Thelist:
					try:							
						print(value["essid"]+": "+str(value["position"])+"; Encrytion: "+str(value["encryption"]))
					except KeyError:
						print("unnamed : "+str(value["position"])+"; Encrytion: "+str(value["encryption"]))
			exit(0)
			
		else:
			print("no output info given")
			options=""
			line=list(loggedData.keys())[0]
			print(line)
			for key,value in loggedData[line].items():
				options+=", "+str(key)
			print("options are: "+options)
			exit(-1)
	except FileNotFoundError:
			exit(-1)