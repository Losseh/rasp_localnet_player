import logging

from states import STATE_STOPPED, STATE_RADIO, STATE_PLAYLIST


class State:
    def __init__(self, radio_stations, playlists):
        # constants
        self.radio_stations = radio_stations
        self.playlists = playlists

        # variables
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
            text = self.radio_stations[self.radio_id][0]
        elif self.state == STATE_PLAYLIST:
            text = self.playlists[self.playlist_id][0]
        elif self.state == STATE_STOPPED:
            text = '-'
        else:
            logging.error("unrecognized state {}".format(self.state))
            text = '? unrecognized state ?'

        return {'source': text}
