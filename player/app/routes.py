from flask import render_template, redirect
from app import app
from config import app_config, radio_stations, playlists
import subprocess
import re
import time
import logging
from os.path import join, exists

STATE_PLAYLIST = 'PLAYLIST'
STATE_STOPPED = 'STOPPED'
STATE_RADIO = 'RADIO'

logging.basicConfig(level=logging.DEBUG,
                    filename=app_config['logfile'],
                    filemode='a',
                    format='%(asctime)s - %(message)s')


class Util:
    def __init__(self):
        pass

    @staticmethod
    def saturate_percent(percent):
        if percent > 100:
            return 100
        if percent < 0:
            return 0

        return percent


class System:
    def __init__(self):
        pass

    @staticmethod
    def run_system_method(method, arguments):
        return System.system_call(method, arguments, subprocess.call)

    @staticmethod
    def call_system_method(method, arguments):
        return System.system_call(method, arguments, subprocess.check_output)

    @staticmethod
    def system_call(method, arguments, call_type):
        assert isinstance(method, str)
        assert isinstance(arguments, list)

        cmd = app_config['system_path'] + method + '.sh'
        return call_type([cmd] + arguments)


class State:
    def __init__(self):
        self.state = STATE_STOPPED
        self.radio_id = None
        self.playlist_id = None
        self.source_songs = []

    def set_music_stopped(self):
        self.state = STATE_STOPPED
        self.radio_id = None
        self.playlist_id = None

    def set_radio_running(self, radio_id):
        self.state = STATE_RADIO
        self.radio_id = radio_id
        self.playlist_id = None

    def set_playlist_running(self, playlist_id):
        self.state = STATE_PLAYLIST
        self.radio_id = None
        self.playlist_id = playlist_id

    def get_state(self):
        return self.state

    def as_json(self):
        if self.state == STATE_RADIO:
            text = radio_stations[self.radio_id][0]
        elif self.state == STATE_PLAYLIST:
            text = playlists[self.playlist_id][0]
        elif self.state == STATE_STOPPED:
            text = '-'
        else:
            logging.error("unrecognized state {}".format(self.state))
            text = '? unrecognized state ?'

        return {'source': text}


class SystemState:
    def __init__(self):
        pass

    def get_current_song(self, state):
        x = {
            STATE_STOPPED: lambda: '-',
            STATE_RADIO: self.get_current_radio_song,
            STATE_PLAYLIST: self.get_current_source_song,
        }
        return x[state]()

    @staticmethod
    def get_current_source_song():
        max_tries = 10
        wait_time_sec = 0.15
        for t in xrange(max_tries):
            result = System.call_system_method('get_current_source_song', [])
            if len(result) > 0:
                logging.debug("get_current_source_song: song: {}".format(result))
                return SystemState.trim_filepath_to_filename_with_last_last_dir(result)
            time.sleep(wait_time_sec)

        logging.debug("get_current_source_song: no song found")
        return '-'

    @staticmethod
    def trim_filepath_to_filename_with_last_last_dir(filepath):
        parts = filepath.split('/')
        return parts[-2] + ' / ' + parts[-1]

    @staticmethod
    def get_current_radio_song():
        return System.call_system_method('get_current_radio_song', [])

    @staticmethod
    def set_volume(percent):
        percent_str = '{}%'.format(Util.saturate_percent(percent))
        return System.call_system_method('set_volume', [percent_str])

    @staticmethod
    def get_volume():
        percent = System.call_system_method('get_volume', [])
        percent = re.sub('\%', '', percent)
        return int(percent)

    def as_json(self, state):
        return {'volume': self.get_volume(), 'song_name': self.get_current_song(state)}


class Player:
    def __init__(self):
        self.state = State()
        self.system_state = SystemState()

    def stop_music(self):
        logging.debug("stop_music()")
        self.state.set_music_stopped()
        self.call_stop_music()

    def run_radio(self, radio_id):
        logging.debug("run_radio({})".format(radio_id))
        self.state.set_radio_running(radio_id)
        self.call_stop_music()
        self.call_run_radio(radio_id)

    def run_playlist(self, playlist_id):
        logging.debug("run_playlist({})".format(playlist_id))
        self.state.set_playlist_running(playlist_id)
        self.call_stop_music()
        self.call_run_playlist(playlist_id)

    def decrement_volume(self):
        volume = self.system_state.get_volume() - 5
        logging.debug("decrement_volume() -> set_volume({})".format(volume))
        self.system_state.set_volume(volume)

    def increment_volume(self):
        volume = self.system_state.get_volume() + 5
        logging.debug("increment_volume() -> set_volume({})".format(volume))
        self.system_state.set_volume(volume)

    def get_state(self):
        app_state = self.state.as_json()
        sys_state = self.system_state.as_json(self.state.get_state())
        result = app_state.copy()
        result.update(sys_state)
        return result

    @staticmethod
    def call_run_playlist(playlist_id):
        # todo assure thte path exists
        subdirectory = playlists[playlist_id][1]
        directory = join(app_config['music_path'], subdirectory)

        if not exists(directory):
            logging.error("{} does not exist!".format(directory))
            return None

        return System.run_system_method('run_directory', [directory])

    @staticmethod
    def call_run_radio(radio_id):
        return System.run_system_method('run_radio', [radio_stations[radio_id][1]])

    @staticmethod
    def call_stop_music():
        return System.run_system_method('stop_music', [])


player = Player()


@app.route('/')
def index():
    templateData = get_index_arguments()
    return render_template('index.html', **templateData)


@app.route('/run_playlist/<int:playlist_id>', methods=['POST'])
def run_playlist(playlist_id):
    player.run_playlist(playlist_id)
    return redirect('/')


@app.route('/run_radio/<int:radio_id>', methods=['POST'])
def run_radio(radio_id):
    player.run_radio(radio_id)
    return redirect('/')


@app.route('/stop_music/', methods=['POST'])
def stop_music():
    player.stop_music()
    return redirect('/')


@app.route('/volume_up/', methods=['POST'])
def volume_up():
    player.increment_volume()
    return redirect('/')


@app.route('/volume_down/', methods=['POST'])
def volume_down():
    player.decrement_volume()
    return redirect('/')


def get_index_arguments():
    state = player.get_state()
    state.update({'title': 'My home player'})
    state.update({'radio_stations': radio_stations})
    state.update({'playlists': playlists})
    return state
