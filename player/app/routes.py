from flask import render_template, redirect
from config import app_config, radio_stations
import logging

from player.app import app
from player.app.source.player import Player

logging.basicConfig(level=logging.DEBUG,
                    filename=app_config['logfile'],
                    filemode='a',
                    format='%(asctime)s - %(message)s')


player = Player(radio_stations, app_config)


@app.route('/', methods=['GET'])
def index():
    template_data = get_index_arguments()
    return render_template('index.html', **template_data)


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
    return state
