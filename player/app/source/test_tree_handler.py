from tree_handler import open_details, close_details


def test_change_details_open():
    tree = get_full_tree()
    paths = [('path', 'd')]
    expected = [('path', 'd'), ('path/dir1', 'd'), ('path/dir2', 'd'), ('path/file0.mp3', 'f')]
    actual = open_details(tree, paths, 'path')
    assert actual == expected


def test_change_details_close():
    paths = [('path', 'd'), ('path/dir1', 'd'), ('path/dir2', 'd')]
    expected = [('path', 'd')]
    actual = close_details(paths, 'path')
    assert actual == expected


def get_full_tree():
    return [
        ('path', ['dir1', 'dir2'], ['file0.mp3']),
        ('path/dir1', ['subdir1'], ['file1.mp3']),
        ('path/dir1/subdir1', [], ['file2.mp3']),
        ('path/dir2', [], ['file3.mp3'])
    ]
