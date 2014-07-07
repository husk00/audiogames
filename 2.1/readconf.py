from xml.dom.minidom import parseString
tracker_N={}
tracker_S={}
file = open('audiogames.xml','r')
data = file.read()
file.close()
dom = parseString(data)
lang = dom.getElementsByTagName('language')[0].toxml()
kin= dom.getElementsByTagName('number')[0].toxml()
kinects=kin.replace('<number>','').replace('</number>','')
language=lang.replace('<language>','').replace('</language>','')


Name= dom.getElementsByTagName('Name')
ips= dom.getElementsByTagName('ip')
aj= dom.getElementsByTagName('ajuste')[0].toxml()
ports= dom.getElementsByTagName('puerto')
ori=aj.replace('<ajuste>','').replace('</ajuste>','')
for n in Name:
	em=  n.toxml().replace('<Name>','').replace('</Name>','')
	if em == "Norte":
		tracker_N['ip']=str(ips[0].toxml().replace('<ip>','').replace('</ip>',''))
		tracker_N['port']=str(ports[0].toxml().replace('<puerto>','').replace('</puerto>', ''))

	if em == "Sur":
		tracker_S['ip']=str(ips[1].toxml().replace('<ip>','').replace('</ip>',''))
		tracker_S['port']=str(ports[1].toxml().replace('<puerto>','').replace('</puerto>', ''))



print language, kinects, ori,tracker_N, tracker_S
