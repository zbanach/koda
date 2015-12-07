#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..app.codec import ExpGolombCodec
from ..app.utils import entropy, read_image, differential_encoding, differential_decoding, scale_to_positive, scale_to_nonpositive, show_histogram
from os.path import dirname

def test_images():
    IMG_PATH = './images/'

    print "\nTest kodowania obrazów"
    pictures = ['airplane_bw.png', 'area_bw.png', 'lenna_bw.png', 'pepper_bw.png']
    for idx, picture in enumerate(pictures, start=1):
        print "\n{}. Obraz {}".format(idx,picture)
        data = read_image(IMG_PATH+picture)
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
