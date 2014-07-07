#!bin/python
import subprocess, OSC, threading
import time 

pdrestart = False


def killaudiogames():
	p= subprocess.Popen(['killall','-9', 'pd-extended'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	#b= subprocess.Popen(['killall','-9', 'blender'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return p

def launcSnd():
    a= subprocess.Popen(['wmctrl','-s 0'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    p= subprocess.Popen(['pasuspender','pd-extended', '/home/husk/pd/planetQ/audiogames/2.1/src/soundengine/main.pd'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p


def launcBlender():
	p= subprocess.Popen(['wmctrl','-s 1'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	#p= subprocess.Popen(['/home/carlos/blender-2.63a-linux-glibc27-i686/blender','/home/carlos/audiogames/2.1/src/game2.blend'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	p= subprocess.Popen(['gnome-terminal','-e','sh blender.sh'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return p

def launcTracker():
	p= subprocess.Popen(['pd-extended','-noaudio', '/home/husk/pd/planetQ/audiogames/2.1/src/tracking/tracker-norte.pd'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	time.sleep(4)
	a= subprocess.Popen(['wmctrl','-s 1'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return p

def launcRouter():
	p= subprocess.Popen(['pd-extended','-noaudio', '/home/husk/pd/planetQ/audiogames/2.1/src/tracking/routerOSC.pd'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return p

# define a message-handler function for the server to call.
def restartpd_handler(addr, tags, stuff, source):
    if  int(stuff[0]) == 1:
      global pdrestart
      pdrestart = True
    print "---"

def OSCserver():

  receive_address = '127.0.0.1', 9999
  s = OSC.OSCServer(receive_address) # basic
  s.addDefaultHandlers()
  s.addMsgHandler("/pdrestart", restartpd_handler) # adding our function
  # Start OSCServer
  print "\nStarting OSCServer. Use ctrl-C to quit."
  st = threading.Thread( target = s.serve_forever )
  st.start()
  return s,st

def main(server,st):
  global pdrestart
  k=killaudiogames()
  s=launcSnd()
  r=launcRouter()
  t=launcTracker()
  time.sleep(3)
  #b=launcBlender()
  try :
      while 1 :
          if pdrestart == True:
              print "restart"
              t.kill()
              o= subprocess.Popen(['wmctrl','-s 0'], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
              time.sleep(0.5)
              pdrestart = False
              t= launcTracker()
          time.sleep(0.5)

  except KeyboardInterrupt :
      print "\nClosing OSCServer."
      server.close()
      killaudiogames()
      print "Waiting for Server-thread to finish"
      st.join() ##!!!

if __name__ == "__main__" :
  s,st=OSCserver()
  main(s,st)
