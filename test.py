import sys
import time
from harmony_control import HarmonyNB
#from kodi_control import Kodi
#from amp_control import Amp

EMAIL='bkanuka@gmail.com'
PASSWORD='lookout'
HARMONY_IP='HarmonyHub'
HARMONY_PORT=5222
KODI_IP='kodi.home.bkanuka.com'
KODI_PORT=8080

harmony=HarmonyNB(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
#amp = Amp(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
#kodi = Kodi(KODI_IP, KODI_PORT)
harmony.start_kodi()
print "RETURNED!"
harmony.close()
