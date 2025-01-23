from metadatavalidator import __author__, __version__


def test_version():
    assert __version__


def test_author():
    assert __author__