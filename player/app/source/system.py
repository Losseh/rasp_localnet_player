import subprocess


class System:
    def __init__(self, app_config):
        self.app_config = app_config

    def run_system_method(self, method, arguments):
        return self.system_call(method, arguments, subprocess.call)

    def call_system_method(self, method, arguments):
        return self.system_call(method, arguments, subprocess.check_output)

    def system_call(self, method, arguments, call_type):
        assert isinstance(method, str)
        assert isinstance(arguments, list)

        cmd = self.app_config['system_path'] + method + '.sh'
        return call_type([cmd] + arguments)
