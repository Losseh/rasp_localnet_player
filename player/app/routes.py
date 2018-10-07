from flask import Flask, render_template, redirect
from app import app
from config import app_config
import datetime
import subprocess
import re
import time

class State:
  def __init__(self):
    self.radio_running = False
    self.source1 = False

state = State()


@app.route('/')
def index():
  templateData = get_index_arguments()
  return render_template('index.html', **templateData)

@app.route('/run_radio/', methods=['POST'])
def run_radio():
  call_stop_music()
  call_run_radio()
  state.radio_running = True
  state.source1 = False
  return redirect('/')

@app.route('/run_source1/', methods=['POST'])
def run_source1():
  call_stop_music()
  call_run_source1()
  state.radio_running = False
  state.source1 = True
  return redirect('/')

@app.route('/stop_music/', methods=['POST'])
def stop_radio():
  call_stop_music()
  state.radio_running = False
  state.source1 = False
  return redirect('/')

@app.route('/volume_up/', methods=['POST'])
def volume_up():
  set_volume(saturate_percent(get_volume() + 5))
  return redirect('/')

@app.route('/volume_down/', methods=['POST'])
def volume_down():
  set_volume(saturate_percent(get_volume() - 5))
  return redirect('/')
 
def call_run_source1():
  return subprocess.call([app_config['system_path'] + 'run_directory.sh', '/media/source1'])

def call_run_radio():
  return subprocess.call([app_config['system_path'] + 'run_radio.sh'])

def call_stop_music():
  return subprocess.call([app_config['system_path'] + 'stop_music.sh'])

def get_index_arguments():
  music_state = get_music_state()
  return {
    'title': 'My home player',
    'volume': get_volume(),
    'music_state': music_state['source'],
    'song_name': music_state['song_name']
  }

def get_music_state():
  if (state.radio_running):
    return {
      'song_name': get_current_radio_song(),
      'source': 'Radio paradise'
    } 
  if (state.source1):
    return {
      'song_name': get_current_source_song(),
      'source': 'Pendrive'
    }
  else:
    return {
      'song_name': '-',
      'source': '-'
    }

def get_current_source_song():
  max_tries = 10
  wait_time_sec = 0.15
  for t in xrange(max_tries):
    result = call_system_method('get_current_source_song', [])
    print result
    if len(result) > 0:
      return result
    time.sleep(wait_time_sec)

  return '-'
  
def get_current_radio_song():
  return call_system_method('get_current_radio_song', [])

def get_volume():
  percent = call_system_method('get_volume', [])
  print percent
  percent = re.sub('\%', '', percent)
  return int(percent)

def set_volume(percent):
  #todo should assure that percent is in correct format
  percent_str = '{}%'.format(saturate_percent(percent))
  print 'set {}%'.format(percent_str)
  return call_system_method('set_volume', [percent_str])

def call_system_method(method, arguments):
  assert isinstance(method, str)
  assert isinstance(arguments, list)

  cmd = app_config['system_path'] + method + '.sh'
  result = subprocess.check_output([cmd] + arguments)
  return result


def saturate_percent(percent):
  if (percent > 100):
    return 100
  if (percent < 0):
    return 0

  return percent
