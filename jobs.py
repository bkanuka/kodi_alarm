import sys
import time
import requests
from alarm import Job
from nadamp import Amp
from kodi_control import Kodi

#print 'init'

#print 'starting kodi'
#harmony.start_kodi(wait=True)

#print 'setting volume'
#amp.set_vol(60)


#class Job:
#    def __init__(self, name, interval=5, maxitter=float('inf')):
#        self.name = name
#        self.interval = interval
#        self.maxitter = maxitter
#
#    def start(self):
#        print "Starting Job: " + self.name
#
#    def run(self):
#        print "Running Job: " + self.name
#
#    def stop(self):
#        print "Stopping Job: " + self.name


class StartKodi(Job):
    def __init__(self):
        Job.__init__(self, 'StartKodi', maxitter=0)

    def start(self):
        url = 'http://ha.home.bkanuka.com/json.htm'
        payload = {'type': 'command', 
                'param': 'switchlight',
                'switchcmd': 'On',
                'idx': 5}

        r = requests.get(url, params=payload)
        print "StartKodi: " + r.text

        print "StartKodi: sleeping"
        time.sleep(15)

        print 'playing'
        kodi = Kodi('192.168.1.11', 8080)
        kodi.play(playlist='Nikta', shuffle=True)


class AmpVolume(Job):
    def __init__(self):
        Job.__init__(self, 'AmpVolume', interval=10, maxitter=5)
        print "AmpVolume: connecting"
        self.amp = Amp('HarmonyHub', 5222, 'bkanuka@gmail.com', 'lookout')

    def start(self):
        print "AmpVolume: sleeping"
        time.sleep(10)
        print "AmpVolume: setting vol"
        self.amp.set_vol(50)
        print "AmpVolume: get client"
        self.client = self.amp.get_client()

    def run(self):
        print "AmpVolume: vol up"
        self.amp.volume_up(self.client)

    def stop(self):
        print "AmpVolume: disconnecting"
        self.client.disconnect(wait=True, send_close=True)
        time.sleep(2)
        print "AmpVolume: setting vol"
        self.amp.set_vol(55)
