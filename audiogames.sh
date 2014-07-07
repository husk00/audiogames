#!/bin/bash

killall -9 pd-extended

cd 2.1/src/soundengine/abs
gnome-terminal -e 'python launchsoundengine.py' &
cd ../../tracking
sleep 2
gnome-terminal -e echo "ag" | sudo pd-extended -noaudio tracker-norte.pd &
sleep 2
gnome-terminal -e 'pd-extended routerOSC.pd'

sleep 5
wmctrl -s 1
sleep 2
gnome-terminal -e 'sh /home/carlos/audiogames/blender.sh'








