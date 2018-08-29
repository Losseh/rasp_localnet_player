import os
import platform

class Config(object):
  SECRET_KEY='you will never guess'

app_config = {}
sys_path = os.path.dirname(os.path.abspath(__file__)) + '/system/'
sys_path += ('raspberry/' if (platform.node() == 'AdrianPi') else 'stub/')
app_config['system_path'] = sys_path

app_config['min_vol'] = -10000
app_config['max_vol'] = 400
