from pprint import pprint

from directory_reader import read_directories, read_tree


def test_read_directories():
    expected = {'dir1', 'dir2', 'dir with space'}

    actual = read_directories('./test_resources')

    assert all((element in expected) for element in actual)


def test_read_tree():
    expected = {'dir1', 'dir2', 'dir with space'}

    actual = read_tree('./test_resources')

    pprint(actual)
    assert all((element in expected) for element in actual)
