# -*- coding:utf8 -*-

import base64
import hashlib
import os

import requests

from . import consts


def cal_b64md5(data):
    """

    :param data: cal md5 checksum for this piece data

    Usage::

        >>> cal_b64md5(io.BytesIO(b"hello world"))
        XrY7u+Ae7tCTyyK7j1rNww==

    """
    if data is None:
        return None
    md5sum = hashlib.md5()
    if hasattr(data, "read") and hasattr(data, "seek"):
        # file-like object or IO-like object
        data_piece = data.read(consts.MD5_CHUNK_SIZE)
        while data_piece:
            md5sum.update(to_bytes(data_piece))
            data_piece = data.read(consts.MD5_CHUNK_SIZE)
        data.seek(0, os.SEEK_SET)
    else:
        md5sum.update(to_bytes(data))
    return to_str(base64.b64encode(md5sum.digest()))


def to_bytes(some_str, encoding="utf8"):
    if isinstance(some_str, requests.compat.str):
        some_bytes = some_str.encode(encoding)
    else:
        some_bytes = some_str
    return some_bytes


def to_str(some_bytes, encoding="utf8"):
    if isinstance(some_bytes, requests.compat.bytes):
        some_str = some_bytes.decode(encoding)
    else:
        some_str = some_bytes
    return some_str


def percent_quote(query):
    return requests.compat.quote(to_bytes(query), consts.PERCENT_SAFE)


def percent_encode(params_tuple, sort=False):
    if sort:
        params = sorted(params_tuple, key=lambda x: x[0])
    else:
        params = list(params_tuple)

    encoded = "&".join([
        "{0}={1}".format(percent_quote(opt), percent_quote(val))
        for opt, val in params
        if val is not None
    ])
    return encoded
