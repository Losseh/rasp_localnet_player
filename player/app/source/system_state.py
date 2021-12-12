import re
import time

from states import STATE_STOPPED, STATE_RADIO, STATE_PLAYLIST


class SystemState:
    def __init__(self, system):
        self.system = system

    def get_current_song(self, state):
        x = {
            STATE_STOPPED: lambda: '-',
            STATE_RADIO: self.get_current_radio_song,
            STATE_PLAYLIST: self.get_current_source_song,
        }
        return x[state]()

    def get_current_source_song(self):
        max_tries = 10
        wait_time_sec = 0.15
        for t in xrange(max_tries):
            result = self.system.call_system_method('get_current_source_song', [])
            if len(result) > 0:
                # logging.debug("get_current_source_song: song: {}".format(result))
                return self.trim_filepath_to_filename_with_last_last_dir(result)
            time.sleep(wait_time_sec)

        # logging.debug("get_current_source_song: no song found")
        return '-'

    @staticmethod
    def trim_filepath_to_filename_with_last_last_dir(filepath):
        parts = filepath.split('/')
        return parts[-2] + ' / ' + parts[-1]

    def get_current_radio_song(self):
        return self.system.call_system_method('get_current_radio_song', [])

    def set_volume(self, percent):
        percent_str = '{}%'.format(Util.saturate_percent(percent))
        return self.system.call_system_method('set_volume', [percent_str])

    def get_volume(self):
        percent = self.system.call_system_method('get_volume', [])
        percent = re.sub('%', '', percent)
        return int(percent)

    def as_json(self, state):
        return {
            'volume': self.get_volume(),
            'song_name': self.get_current_song(state),
        }


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
