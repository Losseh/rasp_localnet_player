import os


def open_details(full_tree, paths, selected_path):
    details = find_details(full_tree, selected_path)
    result = []
    for path in paths:
        result.append(path)
        if path[0] == selected_path:
            for subdir in details[1]:
                result.append((os.path.join(selected_path, subdir), 'd'))
            for subfile in details[2]:
                result.append((os.path.join(selected_path, subfile), 'f'))

    return result


def close_details(paths, selected_path):
    result = []
    for path in paths:
        if not str.startswith(path[0], selected_path) or path[0] == selected_path:
            result.append(path)

    return result


def find_details(full_tree, path):
    for details in full_tree:
        if details[0] == path:
            return details

    return None, [], []
