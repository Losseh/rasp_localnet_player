import os
import platform


class Config(object):
    SECRET_KEY = 'you will never guess'


app_config = {}
sys_path = os.path.dirname(os.path.abspath(__file__)) + '/system/'
sys_path += ('raspberry/' if (platform.node() == 'AdrianPi') else 'stub/')
app_config['system_path'] = sys_path
app_config['logfile'] = '/home/pi/player_log'
app_config['music_path'] = '/media/source1/muzyczka'

app_config['min_vol'] = -10000
app_config['max_vol'] = 400

# human readable name; stream address
radio_stations = [
    ("Nowy Swiat [PL]", "http://stream.rcs.revma.com/ypqt40u0x1zuv"),
    ("357 [PL]", "https://stream.rcs.revma.com/an1ugyygzk8uv"),
    ("Antyradio [PL]", "http://ant-waw-01.cdn.eurozet.pl:8602/listen.pls"),
    ("Antyradio classics [PL]", "http://antgre-01.cdn.eurozet.pl:8002/listen.pls"),
    ("Trojka [PL]", "http://stream3.polskieradio.pl:8904/listen.pls"),
    ("Radio paradise [ENG]", "http://stream-uk1.radioparadise.com/mp3-192"),
    ("BBC Radio 4 [ENG]", "http://www.listenlive.eu/bbcradio4.m3u"),
    ("MDR Kultur [DE]", "http://avw.mdr.de/streams/284310-0_aac_high.m3u"),
    ("SWR2 Archivradio [DE]", "http://mp3-live.swr.de/swr2raka01_m.m3u"),
    ("RTVA Canal Flamenco [ES]", "http://canalflamenco.rtva.stream.flumotion.com/rtva/canalflamenco.mp3.m3u")
]

# human readable name; subdirectory
playlists = [
    ('Rasp - Chillout', 'chill'),
    ("Rasp - Live", 'live')
]

