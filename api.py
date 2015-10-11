from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Ping(Resource):
    def get(self):
        return "PONG!"

api.add_resource(Ping, '/alarm/ping')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
