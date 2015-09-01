from flask import Flask
from flask_restful import Resource, Api
from alarm import AlarmNB
import requests

app = Flask(__name__)
api = Api(app)

EMAIL='bkanuka@gmail.com'
PASSWORD='lookout'
HARMONY_IP='HarmonyHub'
HARMONY_PORT=5222
KODI_IP='kodi.home.bkanuka.com'
KODI_PORT=8080

alarm = AlarmNB(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD, KODI_IP, KODI_PORT)

class Ping(Resource):
    def get(self):
        return "PONG!"

api.add_resource(Ping, '/alarm/ping')

class Start(Resource):
    def get(self):
        alarm.start_kodi(wait=False)
        alarm.set_volume(40)
        alarm.kodi_play(playlist="Nikta", shuffle=True)
        alarm.start_rise(60)

        return True

api.add_resource(Start, '/alarm/start')

class Stop(Resource):
    def get(self):
        message = {"id":1,
        "jsonrpc":"2.0", 
        "method":"GUI.ShowNotification", 
        "params": {
            "title": "Alarm",
            "message": "Stopping Alarm"}
        }

        r = requests.post("http://192.168.1.11:8080/jsonrpc", json=message)

        alarm.stop_rise()
        alarm.set_volume(45)
        alarm.close()
        return True

api.add_resource(Stop, '/alarm/stop')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
