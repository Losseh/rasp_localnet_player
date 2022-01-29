import os
import platform


class Config(object):
    SECRET_KEY = 'you will never guess'


app_config = {
    'min_vol': -10000,
    'max_vol': 400
}

current_path = os.path.dirname(os.path.abspath(__file__))
if platform.node() == 'AdrianPi':
    app_config['system_path'] = current_path + '/system/raspberry/'
    app_config['logfile'] = '/home/pi/rasp_localnet_player/player_log'
    app_config['music_path'] = '/media/source1/muzyczka'
else:
    app_config['system_path'] = current_path + '/system/stub/'
    app_config['logfile'] = '/tmp/player_log'
    app_config['music_path'] = current_path + '/source/test_resources/'

# human readable name; stream address
radio_stations = [
    ("Nowy Swiat [PL]", "http://stream.rcs.revma.com/ypqt40u0x1zuv"),
    ("357 [PL]", "http://stream.rcs.revma.com/an1ugyygzk8uv"),
    ("Antyradio [PL]", "http://an.cdn.eurozet.pl/ant-waw.mp3"),
    ("Antyradio classics [PL]", "https://n-4-2.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5 -cache 128"),
    ("Trojka [PL]", "http://stream3.polskieradio.pl:8904/listen.pls"),
    ("Radio paradise [ENG]", "http://stream-uk1.radioparadise.com/mp3-192"),
    ("BBC Radio 4 [ENG]", "http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/sbr_low/ak/bbc_radio_fourfm.m3u8")
]
