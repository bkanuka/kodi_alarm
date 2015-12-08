from flask import Flask
from flask_restful import Resource, Api
import zmq

app = Flask(__name__)
api = Api(app)

ds_port = 5557
ds_context = zmq.Context()
ds_socket = ds_context.socket(zmq.PAIR)
ds_socket.bind("tcp://*:%s" % ds_port)

class Start(Resource):
    def get(self):
        ds_socket.send("Start")
        msg = ds_socket.recv_json()
        return msg

api.add_resource(Start, '/alarm/start')

class Stop(Resource):
    def get(self):
        ds_socket.send("Stop")
        msg = ds_socket.recv_json()
        return msg

api.add_resource(Stop, '/alarm/stop')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5554, debug=True, use_reloader=False)
