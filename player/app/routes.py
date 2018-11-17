from flask import Flask, render_template, redirect
from app import app
from config import app_config
import datetime
import subprocess
import re
import time

class Util: 
  @staticmethod
  def saturate_percent(percent):
    if (percent > 100):
      return 100
    if (percent < 0):
      return 0

    return percent


class System:
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
    self.source_songs = []

  def set_music_stopped(self):
    self.state = "STOPPED"
  
  def set_radio_running(self):
    self.state = "RADIO"

  def set_source1_running(self):
    self.state = "SOURCE1"

  def get_state(self):
    return self.state

  def as_json(self):
    x = {'STOPPED': '-', 'RADIO': 'Radio paradise', 'SOURCE1': 'Pendrive'}
    return {'source': x[self.get_state()]}

class SystemState:
  def get_current_song(self, state):
    x = {'STOPPED': lambda: '-', 'RADIO': self.get_current_radio_song, 'SOURCE1': self.get_current_source_song}
    return x[state]()
  
  def get_current_source_song(self):
    max_tries = 10
    wait_time_sec = 0.15
    for t in xrange(max_tries):
      result = System.call_system_method('get_current_source_song', [])
      if len(result) > 0:
        return result
      time.sleep(wait_time_sec)

    return '-'
  
  def get_current_radio_song(self):
    return System.call_system_method('get_current_radio_song', [])

  def set_volume(self, percent):
    #todo should assure that percent is in correct format
    percent_str = '{}%'.format(Util.saturate_percent(percent))
    return System.call_system_method('set_volume', [percent_str])

  def get_volume(self):
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
    self.state.set_music_stopped()
    self.call_stop_music()

  def run_radio(self):
    self.state.set_radio_running()
    self.call_stop_music()
    self.call_run_radio()

  def run_source1(self):
    self.state.set_source1_running()
    self.call_stop_music()
    self.call_run_source1()

  def decrement_volume(self):
    self.system_state.set_volume(self.system_state.get_volume() - 5)

  def increment_volume(self):
    self.system_state.set_volume(self.system_state.get_volume() + 5)

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
  def call_run_radio():
    return System.run_system_method('run_radio', [])

  @staticmethod
  def call_stop_music():
    return System.run_system_method('stop_music', [])

player = Player()


@app.route('/')
def index():
  templateData = get_index_arguments()
  return render_template('index.html', **templateData)

@app.route('/run_radio/', methods=['POST'])
def run_radio():
  player.run_radio()
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
  return {
    'title': 'My home player',
    'volume': state['volume'],
    'music_state': state['source'],
    'song_name': state['song_name']
  }

