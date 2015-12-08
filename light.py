#!/usr/bin/env python

"""Light control

Usage:
  light.py on [<room>]
  light.py off [<room>]
  light.py up [<room>]
  light.py down [<room>]
  light.py set <level> [<room>]
  light.py get [<room>]
  light.py dim [<room>]
  light.py undim [<room>]
  light.py toggle [<room>]

"""

import requests

class Light:
    def __init__(self, idx):
        self.idx = idx
        self.prev_level = None

    def _send_request(self, params):
        BASE_URL = 'http://ha.home.bkanuka.com/json.htm'
        req = requests.get(BASE_URL, params=params)
        try:
            r = req.json()
        except ValueError:
            r = None
        return r

    def get_level(self):
        params = {"type": "devices",
                "rid": self.idx}
        json = self._send_request(params)
        if not json:
            return None
        result = json["result"][0]
        if result["Data"] == "Off":
            return 0
        level = int(result["Level"])
        return level

    def set_level(self, level):
        level = min(level, 100)
        level = max(0, level)
        params = {"type": "command",
                "param": "switchlight",
                "idx": self.idx,
                "switchcmd": "Set Level",
                "level": level}
        json = self._send_request(params)
        return json

    def toggle(self):
        params = {"type": "command",
                "param": "switchlight",
                "idx": self.idx,
                "switchcmd": "Toggle"}
        json = self._send_request(params)
        return json

    def on(self):
        params = {"type": "command",
                "param": "switchlight",
                "idx": self.idx,
                "switchcmd": "On"}
        json = self._send_request(params)
        return json

    def off(self):
        params = {"type": "command",
                "param": "switchlight",
                "idx": self.idx,
                "switchcmd": "Off"}
        json = self._send_request(params)
        return json

    def up(self):
        level = self.get_level()
        if not level:
            return None
        json = self.set_level(level + 5)
        return json

    def down(self):
        level = self.get_level()
        if not level:
            return None
        json = self.set_level(level - 5)
        return json

    def dim(self):
        level = self.get_level()
        if not level:
            return None
        if level > 5:
            self.prev_level = level
            json = self.set_level(5)
            return json

    def undim(self):
        level = self.get_level()
        if not level:
            return None
        print level
        print self.prev_level
        if (level > 0) and (level <= 5) and (self.prev_level):
            json = self.set_level(self.prev_level)
            return json


if __name__ == "__main__":

    from docopt import docopt

    rooms = {
            'family': {
                'idx': 1
                },
            'bedroom': {
                'idx': 2
                }
            }

    args = docopt(__doc__)

    if not args['<room>']:
        args['<room>'] = 'family'

    room = args['<room>']
    idx = rooms[room]['idx']

    light = Light(idx)

    if args['set']:
        light.set_level(int(args['<level>']))

    elif args['get']:
        print light.get_level()

    elif args['on']:
        light.on()

    elif args['off']:
        light.off()

    elif args['up']:
        light.up()

    elif args['down']:
        light.down()

    elif args['dim']:
        light.dim()

    elif args['undim']:
        light.undim()

    elif args['toggle']:
        light.toggle()

    else:
        light.toggle()

