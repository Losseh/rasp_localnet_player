from flask import render_template, redirect
from app import app
from config import app_config, radio_stations
import subprocess
import re
import time
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# root_logger = logging.getLogger("default_logger")
# root_logger.setLevel(logging.DEBUG)
#
# debug_logger = logging.StreamHandler(sys.stdout)
# debug_logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# debug_logger.setFormatter(formatter)
# root_logger.addHandler(debug_logger)


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
        self.state = "STOPPED"
        self.radio_id = None
        self.source_songs = []

    def set_music_stopped(self):
        self.state = "STOPPED"
        self.radio_id = None

    def set_radio_running(self, radio_id):
        self.state = "RADIO"
        self.radio_id = radio_id

    def set_source1_running(self):
        self.state = "SOURCE1"
        self.radio_id = None

    def get_state(self):
        return self.state

    def as_json(self):
        texts = {
            'STOPPED': '-',
            'SOURCE1': 'Pendrive'
        }

        if self.state == "RADIO":
            text = radio_stations[self.radio_id][0]
        else:
            text = texts[self.get_state()]

        return {'source': text}


class SystemState:
    def __init__(self):
        pass

    def get_current_song(self, state):
        x = {
            'STOPPED': lambda: '-',
            'RADIO': self.get_current_radio_song,
            'SOURCE1': self.get_current_source_song
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
        # todo should assure that percent is in correct format
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

    def run_source1(self):
        logging.debug("run_source()")
        self.state.set_source1_running()
        self.call_stop_music()
        self.call_run_source1()

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
    def call_run_source1():
        return System.run_system_method('run_directory', ['/media/source1'])

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


@app.route('/run_radio/<int:radio_id>', methods=['POST'])
def run_radio(radio_id):
    player.run_radio(radio_id)
    return redirect('/')


@app.route('/run_source1/', methods=['POST'])
def run_source1():
    player.run_source1()
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
    return state
