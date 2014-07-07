from xml.dom.minidom import parseString
file = open('sndobjects.xml','r')
data = file.read()
file.close()
dom = parseString(data)
so={}
snd_objs=dom.childNodes[0].childNodes
for s in snd_objs:
	if s.nodeType == 1:
		idsnd=s.getElementsByTagName("id")[0].childNodes[0].data
		pc=s.getElementsByTagName("puntoscomer")[0].childNodes[0].data
		pch=s.getElementsByTagName("puntoschocar")[0].childNodes[0].data
		rol=s.getElementsByTagName("rol")[0].childNodes[0].data
		bpm=s.getElementsByTagName("bpm")[0].childNodes[0].data
		color=s.getElementsByTagName("color")[0].childNodes[0].data
		octava=s.getElementsByTagName("octava")[0].childNodes[0].data
		nota=s.getElementsByTagName("nota")[0].childNodes[0].data
		so[idsnd]=pc, pch, rol, bpm, color, octava, nota

print so
