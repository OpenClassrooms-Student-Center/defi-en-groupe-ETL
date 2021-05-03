import pytest
from etl.load import load


def test_load_not_list():
    with pytest.raises(TypeError):
        load(1234)


def test_load_empty_list():
    with pytest.raises(AttributeError):
        load([])


def test_load_invalid_data():
    with pytest.raises(TypeError):
        load([1234])
