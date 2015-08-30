import sys
import time
from harmony_control import Harmony
from kodi_control import Kodi
from amp_control import Amp

EMAIL='bkanuka@gmail.com'
PASSWORD='lookout'
HARMONY_IP='HarmonyHub'
HARMONY_PORT=5222
KODI_IP='kodi.home.bkanuka.com'
KODI_PORT=8080

print 'init'
harmony=Harmony(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
amp = Amp(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
kodi = Kodi(KODI_IP, KODI_PORT)


vol = int(sys.argv[1])
print 'setting volume to {}'.format(vol)
amp.set_vol(vol)
