import os


def read_directories(path):
    return [x[1] for x in os.walk(path)][0]


def read_tree(path):
    return [x for x in os.walk(path)]
    for subpath in os.walk(path):
        for filename in subpath[2]:
            result.append(os.path.join(subpath[0], filename))
    return result
