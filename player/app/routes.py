from flask import Flask, render_template, redirect
from app import app
from config import app_config
import datetime
import subprocess
import re

class State:
  def __init__(self):
    self.radio_running = False
    self.source1 = False

state = State()


@app.route('/')
def index():
  set_volume(100)
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

def call_run_source1():
  return subprocess.call([app_config['system_path'] + 'run_directory.sh', '/media/source1'])

def call_run_radio():
  return subprocess.call([app_config['system_path'] + 'run_radio.sh'])

def call_stop_music():
  return subprocess.call([app_config['system_path'] + 'stop_music.sh'])

def get_index_arguments():
  return {
    'title': 'My home player',
    'music_state': get_music_state(),
  }

def get_music_state():
  if (state.radio_running):
    return 'Radio paradise is running'
  if (state.source1):
    return 'Source1 is running'
  else:
    return 'Music is off'

def set_volume(percent):
  print 'set ' + str(percent) + '%'
  cmd = app_config['system_path'] + 'set_volume.sh'
  amixer = percent_to_amixer(percent)
  ret_val = subprocess.call([cmd, amixer])
  return ret_val

def percent_to_amixer(percent):
  return str(int(percent * (app_config['max_vol'] - app_config['min_vol']) / 100 + app_config['min_vol']))

def saturate_percent(percent):
  if (percent > 100):
    return 100
  if (percent < 0):
    return 0

  return percent
