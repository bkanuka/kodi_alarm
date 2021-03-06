import sys
import time
import RPIO
RPIO.setwarnings(False)

from harmony import auth
from harmony import client as harmony_client

class Amp:
    def __init__(self, harmony_ip, harmony_port, email, password):
        self.harmony_ip = harmony_ip
        self.harmony_port = harmony_port
        self.email = email
        self.password = password

        self.amp_id = None

        RPIO.setup(19, RPIO.OUT, initial=RPIO.HIGH)
        RPIO.setup(5, RPIO.IN)
        RPIO.setup(6, RPIO.IN)
        RPIO.setup(13, RPIO.IN)

        self.volmap = {
                (False, True, True): -120,
                (True, False, True): -100,
                (False, False, True): -80,
                (True, True, False): -60,
                (False, True, False): -40,
                (True, False, False): -20,
                (False, False, False): 0,
                }

    def get_amp_id(self):
        try:
            client = self.get_client()
            config = client.get_config()
        finally:
            client.disconnect(send_close=True)

        dev = [ dev for dev in config['device'] if dev['label'] == u'NAD Amp' ][0]
        self.amp_id = dev['id']

    def get_client(self):
        token = auth.login(self.email, self.password)
        if not token:
            sys.exit('Could not get token from Logitech server.')

        session_token = auth.swap_auth_token(
            self.harmony_ip, self.harmony_port, token)
        if not session_token:
            sys.exit('Could not swap login token for session token.')

        client = harmony_client.create_and_connect_client(
            self.harmony_ip, self.harmony_port, session_token)
        return client

    def db_to_vol(self, x):
        return (16.5/20) * x + 99

    def vol_to_db(self, x):
        return (20/16.5) * x - 120

    def get_gpio_values(self):
        return (RPIO.input(5), RPIO.input(6), RPIO.input(13))

    def get_vol(self):
        gpio_val = self.get_gpio_values()
        db = self.volmap[gpio_val]
        vol = self.db_to_vol(db)
        return vol

    def set_vol(self, x):
        if x < 0 or x > 100:
            raise ValueError('Volume must be between 0 and 100')

        try:
            client = self.get_client()

            if self.get_vol() == 0:
                self.volume_up(client)
                self.volume_up(client)

            if self.get_vol() == 0:
                raise AssertionError('Pressed VolumeUp and no change. Is the Amp on?')

            count = 0
            orig_max_vol = self.get_vol()
            while self.get_vol() == orig_max_vol:
                self.volume_down(client)
                count = count + 1
                if count > 10:
                    raise AssertionError('Pressed VolumeDown and no change. Is the Amp on?')

            while self.get_vol() > x:
                self.volume_down(client)

            vol = self.get_vol()
            while vol < x:
                self.volume_up(client)
                vol = vol + 16.5/4.9

        finally:
            client.disconnect(send_close=True)

    def volume_up(self, client):
        if not self.amp_id:
            self.get_amp_id()

        client.send_command(self.amp_id, "VolumeUp")

    def volume_down(self, client):
        if not self.amp_id:
            self.get_amp_id()

        client.send_command(self.amp_id, "VolumeDown")

if __name__ == "__main__":

    EMAIL='bkanuka@gmail.com'
    PASSWORD='lookout'
    HARMONY_IP='HarmonyHub'
    HARMONY_PORT=5222
    KODI_IP='kodi.home.bkanuka.com'
    KODI_PORT=8080

    amp = Amp(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
    print amp.get_gpio_values()
    #print amp.get_vol()
