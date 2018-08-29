from flask import Flask, render_template, redirect
from app import app
from config import app_config
import datetime
import subprocess
import re

@app.route('/')
def index():
  templateData = get_index_arguments()
  return render_template('index.html', **templateData)

@app.route('/volume_up/', methods=['POST'])
def volume_up():
  set_volume(saturate_percent(get_volume() + 5))
  return redirect('/')

@app.route('/volume_down/', methods=['POST'])
def volume_down():
  set_volume(saturate_percent(get_volume() - 5))
  return redirect('/')

def get_index_arguments():
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")
  volume = get_volume()
  templateData = {
    'title' : 'HELLO!',
    'time': timeString,
    'volume': volume
  }
  return templateData

def set_volume(percent):
  print 'set ' + str(percent) + '%'
  cmd = app_config['system_path'] + 'set_volume.sh'
  amixer = percent_to_amixer(percent)
  ret_val = subprocess.call([cmd, amixer])
  return ret_val

def get_volume():
  cmd = app_config['system_path'] + 'get_volume.sh'
  percent = subprocess.check_output([cmd])
  percent = re.sub('\%', '', percent)
  return int(percent)

#def amixer_to_percent(amixer):
#  return int((100. * (int(amixer) - app_config['min_vol'])) / (app_config['max_vol'] - app_config['min_vol']))

def percent_to_amixer(percent):
  return str(int(percent * (app_config['max_vol'] - app_config['min_vol']) / 100 + app_config['min_vol']))

def saturate_percent(percent):
  if (percent > 100):
    return 100
  if (percent < 0):
    return 0

  return percent
