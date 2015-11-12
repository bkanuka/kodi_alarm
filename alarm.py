import sys
import time
import random
import requests
import zmq
from  multiprocessing import Process

class Job:
    def __init__(self, name, interval=5, maxitter=float('inf')):
        self.name = name
        self.interval = interval
        self.maxitter = maxitter

    def start(self):
        print "Starting Job: " + self.name

    def run(self):
        print "Running Job: " + self.name

    def stop(self):
        print "Stopping Job: " + self.name


def broker(jobs, us_port=5557, ds_port=5558):

    us_context = zmq.Context()
    us_socket = us_context.socket(zmq.PAIR)
    us_socket.connect("tcp://localhost:%s" % us_port)
    print "Broker upstream port: ", us_port

    ds_context = zmq.Context()
    ds_socket = ds_context.socket(zmq.PUB)
    ds_socket.bind("tcp://*:%s" % ds_port)
    print "Broker downstream port: ", ds_port

    run = False
    procs = []

    while True:
        msg = us_socket.recv()

        if msg == "Start":
            if not run or not any([p.is_alive() for p in procs]):
                procs = [Process(target=client, args=(j,)) for j in jobs]
                [p.start() for p in procs]
                run = True
                us_socket.send_json(True)
            else:
                us_socket.send_json(False)

        if msg == "Stop":
            if not run:
                us_socket.send_json(False)
            else:
                ds_socket.send("Stop")
                us_socket.send_json(True)
                time.sleep(20)

                for p in procs:
                    if p.is_alive():
                        print "ERROR: TERMINATING PROCESS"
                        p.terminate()

                run = False

def client(job, us_port=5558):
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_sub.setsockopt(zmq.SUBSCRIBE, '')
    socket_sub.connect("tcp://localhost:%s" % us_port)
    print "Connected to broker with port %s" % us_port

    # Startup Things
    job.start()

    run = True
    i = 0
    while run and i < job.maxitter:
        print "Waiting for message"
        message_waiting = socket_sub.poll(timeout=job.interval*1000)
        print "Received/Timeout"
        if message_waiting:
            message = socket_sub.recv()
            if message == "Stop":
                print "Recieved stop command, client will stop recieving messages"
                run = False
                break
            else:
                print "Received: " + message

        # Do things
        job.run()
        i = i + 1

    # Stop things
    job.stop()



if __name__ == "__main__":
    from jobs import *
    startkodi = StartKodi()
    ampvolume = AmpVolume()

    jobs = [startkodi, ampvolume]

    Process(target=broker, args=(jobs,)).start()
