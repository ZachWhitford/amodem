import os
from cStringIO import StringIO
import numpy as np

import send
import recv
import common

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-12s %(message)s')

class Args(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def run(size, chan):
    tx_data = os.urandom(size)
    tx_audio = StringIO()
    send.main(Args(silence_start=1, silence_stop=1, input=StringIO(tx_data), output=tx_audio))

    data = tx_audio.getvalue()
    data = common.loads(data)
    data = chan(data)
    data = common.dumps(data * 1j)
    rx_audio = StringIO(data)

    rx_data = StringIO()
    recv.main(Args(skip=100, input=rx_audio, output=rx_data))
    rx_data = rx_data.getvalue()

    assert rx_data == tx_data

def test_small():
    run(1024, lambda x: x)

def test_large():
    run(54321, lambda x: x)

def test_attenuation():
    run(5120, lambda x: x * 0.1)

def test_low_noise():
    r = np.random.RandomState(seed=0)
    run(5120, lambda x: x + r.normal(size=len(x), scale=0.0001))

def test_medium_noise():
    r = np.random.RandomState(seed=0)
    run(5120, lambda x: x + r.normal(size=len(x), scale=0.001))
