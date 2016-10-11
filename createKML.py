import pickle

def check(string):
	newstring=""
	for char in string:
		if char!="&":
			newstring=str(newstring)+str(char)
	return(str(newstring))

if __name__=="__main__":
	with open("logFile" + '.pkl', 'rb') as f:
		loggedData = pickle.load(f)
	file=open("file.kml","w")
	file.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"\n xmlns:gx="http://www.google.com/kml/ext/2.2">\n\n<Folder>\n')
	for key, value in loggedData.items():
		name=None
		try:
			name=value["essid"]
		except KeyError:
			name="unknown"
		file.write('<Placemark>\n<name>'+check(name)+'</name>\n<description>\n')
		for key2,value2 in value.items():
			file.write(check(key2)+": "+check(value2)+'\n')
		file.write('</description>\n<gx:balloonVisibility>1</gx:balloonVisibility>\n<Point>\n<coordinates>'+str(value["position"][1])+','+str(value["position"][0])+'</coordinates>\n</Point>\n</Placemark>\n')
	file.write("</Folder>\n\n</kml>")
	file.close()


