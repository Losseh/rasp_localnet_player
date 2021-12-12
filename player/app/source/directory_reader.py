import os


def read_directories(path):
    return [x[1] for x in os.walk(path)][0]
