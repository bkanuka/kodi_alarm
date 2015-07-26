import time
from harmony import auth
from harmony import client as harmony_client

class Harmony:
    def __init__(self, harmony_ip, harmony_port, email, password):
        self.client = self.get_client(harmony_ip, harmony_port, email, password)
        self.config = self.client.get_config()

    def get_client(self, harmony_ip, harmony_port, email, password):
        token = auth.login(email, password)
        if not token:
            sys.exit('Could not get token from Logitech server.')

        session_token = auth.swap_auth_token(
            harmony_ip, harmony_port, token)
        if not session_token:
            sys.exit('Could not swap login token for session token.')

        client = harmony_client.create_and_connect_client(
            harmony_ip, harmony_port, session_token)
        return client

    def close(self):
        self.client.disconnect(send_close=True)

    def start_kodi(self, wait=True):
        activity = [ act for act in self.config['activity'] if act['label'] == u'XBMC' ][0]
        activity_id = activity['id']
        self.client.start_activity(activity_id)
        if wait:
            time.sleep(20)

    def volume_up(self):
        dev = [ dev for dev in self.config['device'] if dev['label'] == u'NAD Amp' ][0]
        dev_id = dev['id']
        self.client.send_command(dev_id, "VolumeUp")

    def volume_down(self):
        dev = [ dev for dev in self.config['device'] if dev['label'] == u'NAD Amp' ][0]
        dev_id = dev['id']
        self.client.send_command(dev_id, "VolumeDown")
