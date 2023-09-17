#!/usr/bin/env python3

from unittest import mock
import foo

@mock.patch('foo.lolz')
def test_my_thing(mocked_lolz):
    mocked_lolz.return_value = 5
    res = foo.lolz()
    assert res == 5

def test_without_mock():
    res = foo.lolz()
    assert res == 88



