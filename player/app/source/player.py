import logging
from os.path import exists, join

from state import State
from system import System
from system_state import SystemState
from directory_reader import read_directories


class Player:
    def __init__(self, radio_stations, app_config):
        self.radio_stations = radio_stations
        self.app_config = app_config

        # todo: to powinno byc rozszerzone o cale drzewo, a nie tylko foldery
        self.playlists = self.get_playlists()

        self.state = State(radio_stations, self.playlists)
        self.system = System(app_config)
        self.system_state = SystemState(self.system)

    def stop_music(self):
        # logging.debug("stop_music()")
        self.state.set_music_stopped()
        self.call_stop_music()

    def run_radio(self, radio_id):
        # logging.debug("run_radio({})".format(radio_id))
        self.state.set_radio_running(radio_id)
        self.call_stop_music()
        self.call_run_radio(radio_id)

    def run_playlist(self, playlist_id):
        # logging.debug("run_playlist({})".format(playlist_id))
        self.state.set_playlist_running(playlist_id)
        self.call_stop_music()
        self.call_run_playlist(playlist_id)

    def decrement_volume(self):
        volume = self.system_state.get_volume() - 5
        # logging.debug("decrement_volume() -> set_volume({})".format(volume))
        self.system_state.set_volume(volume)

    def increment_volume(self):
        volume = self.system_state.get_volume() + 5
        # logging.debug("increment_volume() -> set_volume({})".format(volume))
        self.system_state.set_volume(volume)

    def get_playlists(self):
        return read_directories(self.app_config['music_path'])

    def get_state(self):
        app_state = self.state.as_json()
        sys_state = self.system_state.as_json(self.state.get_state())
        result = app_state.copy()
        result.update(sys_state)
        result.update({'playlists': self.playlists})
        return result

    # todo: przerobic na run_path, arg=path:string
    def call_run_playlist(self, playlist_id):
        subdirectory = self.playlists[playlist_id]
        directory = join(self.app_config['music_path'], subdirectory)

        if not exists(directory):
            logging.error("{} does not exist!".format(directory))
            return None

        return self.system.run_system_method('run_directory', [directory])

    def call_run_radio(self, radio_id):
        return self.system.run_system_method('run_radio', [self.radio_stations[radio_id][1]])

    def call_stop_music(self):
        return self.system.run_system_method('stop_music', [])