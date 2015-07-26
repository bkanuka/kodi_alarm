import time
from harmony import auth
from harmony import client as harmony_client

class Harmony:
    def __init__(self, harmony_ip, harmony_port, email, password):
        self.harmony_ip = harmony_ip
        self.harmony_port = harmony_port
        self.email = email
        self.password = password

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

    def start_kodi(self, wait=True):
        client = self.get_client()

        current_activity = client.get_current_activity()
        print "Current Activity:", current_activity

        config = client.get_config()
        activity = [ act for act in config['activity'] if act['label'] == u'XBMC' ][0]
        activity_id = int(activity['id'])
        print "Activity Id:", activity_id

        start = False
        if current_activity != activity_id:
            print "Starting Kodi"
            client.start_activity(activity_id)
            start = True

        client.disconnect(send_close=True)

        if start and wait:
            time.sleep(20)
