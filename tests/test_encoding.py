#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..app.codec import ExpGolombCodec
from ..app.utils import entropy, read_image, differential_encoding, differential_decoding, scale_to_positive, scale_to_nonpositive, show_histogram
from os.path import dirname, join, pardir, abspath
from os import listdir

def test_images():
    IMG_PATH = abspath(join(dirname(__file__), pardir, 'images'))

    print "\nTest kodowania obrazów"
    images = listdir(IMG_PATH)
    for idx, image in enumerate(images, start=1):
        print "\n{}. Obraz {}".format(idx, image)
        data = read_image(join(IMG_PATH, image))
        diffed = differential_encoding(data)
        scaled = scale_to_positive(diffed)
        decoded = None
        for direct in (True, False):
            codec = ExpGolombCodec(direct)
            encoded = codec.encode(scaled)
            decoded = codec.decode(encoded)
            assert decoded == scaled
        descaled = scale_to_nonpositive(decoded)
        assert descaled == diffed
        dediffed = differential_decoding(descaled)
        assert dediffed == data
        print "Obraz wejściowy jednakowy ze zdekodowanym."

if __name__ == '__main__':
    test_images()
