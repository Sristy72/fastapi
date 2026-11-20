from wsgiref import validate

import pytest


def test_equal_or_not_equal():
    assert 3 == 3


def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)



