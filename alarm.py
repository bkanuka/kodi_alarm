import sys
import time
import random
import requests
import zmq
from  multiprocessing import Process

#print 'init'

#print 'starting kodi'
#harmony.start_kodi(wait=True)

#print 'setting volume'
#amp.set_vol(60)

#print 'playing'
#kodi = Kodi(KODI_IP, KODI_PORT)
#kodi.play(playlist='Nikta', shuffle=True)

def broker(ds_port="5558"):
    ds_context = zmq.Context()
    ds_socket = ds_context.socket(zmq.PUB)
    ds_socket.bind("tcp://192.168.1.10:%s" % ds_port)
    print "Broker server on port: ", ds_port
    i = 0
    while True:
        msg = str(i)
        print "Publishing: " + msg
        ds_socket.send(msg)
        time.sleep(1)
        i = i + 1

    ds_socket.send("Exit")
         

def client(port_sub):
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect("tcp://192.168.1.10:%s" % port_sub)
    print "Connected to broker with port %s" % port_sub
    # Initialize poll set
    #poller = zmq.Poller()
    #poller.register(socket_sub, zmq.POLLIN)

    run = True
    while run:
        print "Waiting for message"
        print socket_sub.closed
        message = socket_sub.recv()
        #message = socket_sub.poll(timeout=5*1000)
        print "Received"
        print message
        if message:

            message = socket_sub.recv()
        #socks = poller.poll(timeout=5*1000)
        #print socks
        #if socks:
        #    socks = dict(socks)

        #if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            #string = socket_sub.recv()
            #topic, messagedata = string.split()
            print "Processing ... ", message
            if message == "Exit": 
                print "Recieved exit command, client will stop recieving messages"
                run = False
                break
            else:
                print "Received: " + message
        
    print "Exiting"

        

if __name__ == "__main__":
    # Now we can run a few servers 
    ds_port = "9999"
    Process(target=broker, args=(ds_port,)).start()
    time.sleep(1)
    Process(target=client, args=(ds_port,)).start()
