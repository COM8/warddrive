import pickle

if __name__=="__main__":
	try:
		with open("logFile" + '.pkl', 'rb') as f:
			loggedData = pickle.load(f)
			for key, value in loggedData.items():
				try:
					print(value["essid"]+": "+str(value["position"])+"; Encrytion: "+str(value["encryption"]))
				except KeyError:
					print("unnamed : "+str(value["position"])+"; Encrytion: "+str(value["encryption"]))
				#print(item["essid"])
			#print(loggedData)
			exit(0)
	except FileNotFoundError:
		exit(-1)