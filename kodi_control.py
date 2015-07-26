from xbmcjson import XBMC

class Kodi:
    def __init__(self, ip, port):
        self.kodi_url = 'http://{}:{}/jsonrpc'.format(ip, port)
        kodi = XBMC(self.kodi_url, '', '')
        kodi.JSONRPC.Ping()

    def play(self, playlist='Nikta', shuffle=True):
        kodi = XBMC(self.kodi_url, '', '')

        playlist = 'special://profile/playlists/music/{}.m3u'.format(playlist)

        kodi.Playlist.Clear({"playlistid": 0})

        kodi.Playlist.Add({
                    "playlistid": 0,
                    "item": {"directory": playlist}
                    })

        kodi.Player.Open({
                    "item": {"playlistid": 0},
                    "options": {"shuffled": shuffle}
                    })
