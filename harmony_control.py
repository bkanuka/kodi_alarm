import time
from harmony import auth
from harmony import client as harmony_client
from multiprocessing import Process, Pipe

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
        try:
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

        finally:
            client.disconnect(send_close=True)

        if start and wait:
            time.sleep(20)

class HarmonyNB:
    def __init__(self, harmony_ip, harmony_port, email, password):
        conn1, conn2 = Pipe()

        def worker_function(conn):
            harmony = Harmony(harmony_ip, harmony_port, email, password)
            while True:
                try:
                    command = conn.recv()
                    if command == "start_kodi_wait":
                        harmony.start_kodi(wait=True)
                    elif command == "start_kodi_nowait":
                        harmony.start_kodi(wait=False)
                    elif command == "close":
                        conn.close()
                        break
                except EOFError:
                    break

        self.worker = Process(target=worker_function, args=(conn2,))
        self.worker.start()

        self.conn = conn1

    def start_kodi(self, wait=True):
        if wait:
            self.conn.send("start_kodi_wait")
        else:
            self.conn.send("start_kodi_nowait")

    def close(self):
        self.conn.send("close")
        self.conn.close()
        self.worker.join()

