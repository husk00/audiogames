# Game.py
import sys
import bge
from xml.dom.minidom import parseString
import xml.etree.ElementTree as etree
import GameLogic as gl
from OSC import OSCClient, OSCMessage, OSCBundle

gl.send_to = ('localhost', 7777 )

time = 0.0
time_since_last_frame = 0.0

# PARA AÑADIR AL XML ####################################################3
bpm_base = 90.0
bpm_bonus = 90              # bpm que aumenta con el bonus
bonus_duration = 2000       # tiempo que dura el bonus
out_cnt = bonus_duration*1  

timewithoutplayer = 1200

inicializado = False
user_presence = False
start = False

pdrestart = False


snd_objs = {}

def readconf(file):
    tracker_N = {}
    tracker_S = {}
    data = file.read()
    file.close()
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

def readlevels(file):
    level={}
    tmp=[]
    tmp2=[]
    tree = etree.parse(file)
    root = tree.getroot()
    for child in tree.iter():
        for c in child:
            if c.tag != "level":
                if c.tag == "id":
                    tmp=[]
                    tmp2=[]
                    i=c.text
                else:
                    tmp.append(c.text)
                    if len(tmp)==2:
                        tupla=tmp[0],tmp[1]
                        tmp2.append(tupla)
                        tmp=[]
                level[i]=tmp2
                        
    return level

def readsndobjs(file):
    
    data = file.read()
    file.close()
    dom = parseString(data)
    so={}
    snd_objs=dom.childNodes[0].childNodes
    for s in snd_objs:
    	if s.nodeType == 1:
    		idsnd=int(s.getElementsByTagName("id")[0].childNodes[0].data)
    		pc=int(s.getElementsByTagName("puntoscomer")[0].childNodes[0].data)
    		pch=int(s.getElementsByTagName("puntoschocar")[0].childNodes[0].data)
    		rol=s.getElementsByTagName("rol")[0].childNodes[0].data.upper()
    		bpm=float(s.getElementsByTagName("bpm")[0].childNodes[0].data)
    		color=s.getElementsByTagName("color")[0].childNodes[0].data.upper()
    		octava=int(s.getElementsByTagName("octava")[0].childNodes[0].data)
    		nota=int(s.getElementsByTagName("nota")[0].childNodes[0].data)
    		alcance=int(s.getElementsByTagName("alcance")[0].childNodes[0].data)
    		so[idsnd]=pc, pch, rol, bpm, color, octava, nota, alcance
    return so

def sendOSCgame():
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/game"
        msg.setAddress(address)
        msg.append(currentlevel)
        client.sendto(msg, gl.send_to)
        print('Send message example =', msg, "to ", gl.send_to)
        return

def sendOSCnextlevel():
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/nextlevel"
        msg.setAddress(address)
        msg.append(currentlevel)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
def init():
    
    # set default current level
    global currentlevel
    currentlevel = 1
    global inicializado
    if inicializado == False:
        sendOSCgame()
        inicializado = True
    global pdrestart
    if pdrestart == True:
        print("UHHHIIHJIJIJKJJK")
        pdrestart = False

    
        
    # Tell the python interpreter to look in my lib folder for python scripts
    sys.path.append(bge.logic.expandPath("//lib"))
    sys.path.append(bge.logic.expandPath("//data"))   # seems not to work with file open??
    
    #  if you use bpy module you cannot use blenderplayer #path = bpy.data.filepath.rpartition("/")[0]+"/data/"
    path = "/home/husk/pd/planetQ/audiogames/argentina/src/data/"
    
    # read configuration file
    file = open(path+'audiogames.xml','r')
    conf = readconf(file)
    #print(conf)
    global languaje, kinects, ori_adj, tracker_N, tracker_S
    languaje, kinects, ori_adj, tracker_N, tracker_S = conf  # {'ip': '192.168.106.6', 'port': '7711'}
    
    # read levels configuration file
    file = open(path+'levels.xml','r')
    global ll
    ll = readlevels(file)
    #print(ll)
    
    # read soundobjects configuration file
    file = open(path+'sndobjects.xml','r')
    global snd_objs
    snd_objs = readsndobjs(file)
    #print(snd_objs)
    
    # A good place to enable mouse visibility
    bge.render.showMouse(False)

    keyboard = bge.logic.keyboard.events
    events = bge.events
    
    if keyboard[events.SPACEKEY] or user_presence == True:  ######################################################################################
        # go to the default starting scene
        sendOSCnextlevel()
        bge.logic.getCurrentScene().replace('interlevel')
        
    

def main():
    # A good place to put any code that needs to be called each frame
    # In this case, its only going to update the time attribute of my Game module
    global time, time_since_last_frame
    time_since_last_frame = time - bge.logic.getCurrentController().owner['time']
    time = bge.logic.getCurrentController().owner['time']
    
    keyboard = bge.logic.keyboard.events
    events = bge.events

    # change cameras
    JUST_RELEASED = bge.logic.KX_INPUT_JUST_RELEASED

    if keyboard[bge.events.CKEY] == JUST_RELEASED:
        scene = bge.logic.getCurrentScene()
        cam = scene.active_camera
        if cam.name == 'Camera.cenital':
            scene.active_camera = scene.objects["Camera.2"]
        else:
            scene.active_camera = scene.objects["Camera.cenital"]
    

    if keyboard[events.LKEY] == JUST_RELEASED:
        global currentlevel, ll
        currentlevel += 1
        if currentlevel > len(ll):
            currentlevel = 1
            print("YOU WIN---------")
            bge.logic.getCurrentScene().replace('youwin')
        else:
            print("level-up----------------------------", currentlevel)
            bge.logic.getCurrentScene().replace('interlevel')
    
    scn = bge.logic.getCurrentScene()
    luz = scn.objects["luz-general"]
    if keyboard[events.OKEY] == JUST_RELEASED:      
        luz.energy = 0.0
        
    if keyboard[events.IKEY] == JUST_RELEASED: 
        luz.energy = 0.2
           
                    
                    
                     