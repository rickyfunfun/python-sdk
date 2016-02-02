# coding: utf-8

import os

from StringIO import StringIO
import cStringIO
from nose.tools import with_setup
from nose.tools import assert_raises
from nose.tools import raises

import requests

import leancloud
from leancloud import File
from leancloud import ACL

__author__ = 'asaka'


def setup_func():
    leancloud.init(
        os.environ['APP_ID'],
        master_key=os.environ['MASTER_KEY']
    )


def test_basic():
    s = StringIO('blah blah blah')
    s1 = cStringIO.StringIO()
    s1.write('blah blah blah')
    f1 = File('Blah', s, 'text/plain')
    f2 = File('Blah', s1)
    f3 = File('Blah', open('tests/test_file.txt', 'r'))
    for f in (f1, f2, f3):
        assert f.name == 'Blah'
        assert f._metadata['size'] == 14
        assert f.size == 14
        assert f._type == 'text/plain'


def test_create_with_url():
    f = File.create_with_url('xxx', 'http://i1.wp.com/leancloud.cn/images/static/default-avatar.png', meta_data={})
    assert f.url == 'http://i1.wp.com/leancloud.cn/images/static/default-avatar.png'


def test_create_without_data():
    f = File.create_without_data(123)
    assert f.id == 123


def test_acl():
    acl = ACL()
    f = File('Blah', buffer('xxx'))
    assert_raises(TypeError, f.set_acl, 'a')
    f.set_acl(acl)
    assert f.get_acl() == acl


@with_setup(setup_func)
def test_save():
    f = File('Blah', buffer('xxx'))
    f.save()
    assert f.id


@with_setup(setup_func)
def test_save_external():
    f = File.create_with_url('lenna.jpg', 'http://i1.wp.com/leancloud.cn/images/static/default-avatar.png')
    f.save()
    assert f.id


@raises(ValueError)
def test_thumbnail_url_erorr():
    f = File.create_with_url('xx', False)
    f.get_thumbnail_url(100, 100)


@raises(ValueError)
def test_thumbnail_size_erorr():
    r = requests.get('http://i1.wp.com/leancloud.cn/images/static/default-avatar.png')
    b = buffer(r.content)
    f = File('Lenna2.jpg', b)
    f.save()
    assert f.id

    f.get_thumbnail_url(-1, -1)
    f.get_thumbnail_url(1, 1, quality=110)


@with_setup(setup_func)
def test_thumbnail():
    r = requests.get('http://i1.wp.com/leancloud.cn/images/static/default-avatar.png')
    b = buffer(r.content)
    f = File('Lenna2.jpg', b)
    f.save()
    assert f.id

    url = f.get_thumbnail_url(100, 100)
    assert url.endswith('?imageView/2/w/100/h/100/q/100/format/png')


@with_setup(setup_func)
def test_destroy():
    r = requests.get('http://i1.wp.com/leancloud.cn/images/static/default-avatar.png')
    b = buffer(r.content)
    f = File('Lenna2.jpg', b)
    f.save()
    assert f.id
    f.destroy()


@with_setup(setup_func)
def test_fetch():
    r = requests.get('http://i1.wp.com/leancloud.cn/images/static/default-avatar.png')
    b = buffer(r.content)
    f = File('Lenna2.jpg', b)
    f.metadata['foo'] = 'bar'
    f.save()
    fetched = File.create_without_data(f.id)
    fetched.fetch()
    assert fetched.id == f.id
    assert fetched.metadata == f.metadata
    assert fetched.name == f.name
    assert fetched.url == f.url
    assert fetched.size == f.size
    assert fetched.url == f.url
    f.destroy()
