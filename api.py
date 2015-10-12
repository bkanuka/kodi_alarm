from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Start(Resource):
    def get(self):

        EMAIL='bkanuka@gmail.com'
        PASSWORD='lookout'
        HARMONY_IP='HarmonyHub'
        HARMONY_PORT=5222
        KODI_IP='kodi.home.bkanuka.com'
        KODI_PORT=8080

        print 'init'
        harmony=Harmony(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
        amp = Amp(HARMONY_IP, HARMONY_PORT, EMAIL, PASSWORD)
        kodi = Kodi(KODI_IP, KODI_PORT)


        print 'starting kodi'
        harmony.start_kodi(wait=True)

        print 'setting volume'
        amp.set_vol(55)

        print 'playing'
        kodi.play(playlist='Nikta', shuffle=True)

        return True

api.add_resource(Alarm, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
