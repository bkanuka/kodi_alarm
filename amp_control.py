import sys
import time
import RPIO
from harmony import auth
from harmony import client as harmony_client

class Amp:
    def __init__(self, harmony_ip, harmony_port, email, password):
        self.harmony_ip = harmony_ip
        self.harmony_port = harmony_port
        self.email = email
        self.password = password

        client = self.get_client()
        config = client.get_config()
        client.disconnect(send_close=True)

        dev = [ dev for dev in config['device'] if dev['label'] == u'NAD Amp' ][0]
        self.amp_id = dev['id']
        
        RPIO.setup(16, RPIO.IN)
        RPIO.setup(20, RPIO.IN)
        RPIO.setup(21, RPIO.IN)

        self.volmap = {
                (False, True, True): -120,
                (True, False, True): -100,
                (False, False, True): -80,
                (True, True, False): -60,
                (False, True, False): -40,
                (True, False, False): -20,
                (False, False, False): 0,
                }

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
        return (RPIO.input(16), RPIO.input(20), RPIO.input(21))

    def get_vol(self):
        gpio_val = self.get_gpio_values()
        db = self.volmap[gpio_val]
        vol = self.db_to_vol(db)
        return vol

    def set_vol(self, x):
        if x < 0 or x > 100:
            raise ValueError('Volume must be between 0 and 100')

        client = self.get_client()

        while self.get_vol() > x:
            self.volume_down(client)
        v = self.get_vol()
        u = 0.0
        while u + v < x:
            self.volume_up(client)
            u = u + 16.5/4.8

        client.disconnect(send_close=True)

    def volume_up(self, client):
        client.send_command(self.amp_id, "VolumeUp")

    def volume_down(self, client):
        client.send_command(self.amp_id, "VolumeDown")
