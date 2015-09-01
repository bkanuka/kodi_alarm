import sys
import time
from multiprocessing import Process, Pipe

class AlarmNB:
    def __init__(self, harmony_ip, harmony_port, email, password, kodi_ip, kodi_port):

        def worker_func(conn):
            from harmony_control import Harmony
            from kodi_control import Kodi
            from amp_control import Amp

            harmony = Harmony(harmony_ip, harmony_port, email, password)
            amp = Amp(harmony_ip, harmony_port, email, password)
            kodi = Kodi(kodi_ip, kodi_port)

            amp_client = None
            raise_vol = False

            try:
                while True:
                    command, args = conn.recv()

                    if command == "start_kodi":
                        harmony.start_kodi(args)

                    elif command == "set_vol":
                        amp.set_vol(args)

                    elif command == "kodi_play":
                        kodi.play(**args)

                    elif command == "start_rise":
                        interval = args
                        raise_vol = True
                        
                    elif command == "stop_rise":
                        if amp_client:
                            amp_client.disconnect(send_close=True)
                            amp_client = None  
                        raise_vol = False
                        
                    elif command == "close":
                        conn.close()
                        break


                    if raise_vol:
                        if not amp_client:
                            amp_client = amp.get_client()

                        while True:
                            amp.volume_up(amp_client)
                            start_polling = time.time()
                            while (time.time() - start_polling) < interval:
                                if conn.poll():
                                    break
                                time.sleep(0.5)
                            if conn.poll():
                                break

            except (EOFError, KeyboardInterrupt):
                pass

            finally:
                if amp_client:
                    amp_client.disconnect(send_close=True)

        worker_conn1, worker_conn2 = Pipe()
        self.worker = Process(target=worker_func, args=(worker_conn2,))
        self.worker.start()
        self.worker_conn = worker_conn1

    def start_kodi(self, wait=True):
        self.worker_conn.send(("start_kodi", wait))

    def set_volume(self, vol):
        self.worker_conn.send(("set_vol", vol))

    def kodi_play(self, playlist="Nikta", shuffle=True):
        self.worker_conn.send(("kodi_play", {"playlist": playlist, "shuffle": shuffle}))

    def start_rise(self, interval):
        self.worker_conn.send(("start_rise", interval))

    def start(self):
        self.start_kodi()
        self.set_volume(55)
        self.kodi_play()
        self.start_rise(20)

    def stop_rise(self):
        self.worker_conn.send(("stop_rise", None))

    def close(self):
        self.worker_conn.send(("stop_rise", None))
        self.worker_conn.send(("close", None))
        self.worker_conn.close()
        self.worker.join()
