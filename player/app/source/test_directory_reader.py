from directory_reader import read_directories


def test_read_directories():
    expected = {'dir1', 'dir2', 'dir with space'}

    actual = read_directories('./test_resources')

    assert all((element in expected) for element in actual)
