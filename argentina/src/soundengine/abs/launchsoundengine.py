from xml.dom.minidom import parseString
import xml.etree.ElementTree as etree
import sys,os
import shutil
import subprocess

def readconf(fil):
    tracker_N = {}
    tracker_S = {}
    data = fil.read()
    fil.close()
    dom = parseString(data)
    lang = dom.getElementsByTagName('language')[0].toxml()
    kin = dom.getElementsByTagName('number')[0].toxml()
    kinects = kin.replace('<number>','').replace('</number>','')
    language = lang.replace('<language>','').replace('</language>','')
    Name = dom.getElementsByTagName('Name')
    ips = dom.getElementsByTagName('ip')
    aj = dom.getElementsByTagName('ajuste')[0].toxml()
    ports = dom.getElementsByTagName('puerto')
    ori =aj.replace('<ajuste>','').replace('</ajuste>','')
    for n in Name:
        em = n.toxml().replace('<Name>','').replace('</Name>','')
        if em == "Norte":
            tracker_N['ip']=str(ips[0].toxml().replace('<ip>','').replace('</ip>',''))
            tracker_N['port']=str(ports[0].toxml().replace('<puerto>','').replace('</puerto>', ''))
    
        if em == "Sur": 
            tracker_S['ip']=str(ips[1].toxml().replace('<ip>','').replace('</ip>',''))
            tracker_S['port']=str(ports[1].toxml().replace('<puerto>','').replace('</puerto>', ''))
    conf = language, kinects, ori, tracker_N, tracker_S
    return conf


file = open('../../data/audiogames.xml','r')
conf=readconf(file)
languaje, kinects, ori_adj, tracker_N, tracker_S = conf

if kinects == '1':
  shutil.copy2('binaural1_una.pd','binaural1.pd')
  shutil.copy2('../../tracking/getUserPresence1.pd','../../tracking/getUserPresence.pd')
else:
  shutil.copy2('binaural1_due.pd','binaural1.pd')
  shutil.copy2('../../tracking/getUserPresence2.pd','../../tracking/getUserPresence.pd')
command = ("pasuspender sh soundengine.sh")
subprocess.call(command,shell=True)


