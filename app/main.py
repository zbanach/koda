# coding=utf-8
import numpy
import sys
from codec import ExpGolombCodec
from utils import entropy, read_image, differential_encoding, scale_to_positive, show_histogram, normalize_to_byte
from os.path import dirname, join, pardir, abspath
from os import listdir


def main():
    show_hist = True if '-h' in sys.argv else False
    exec_all = True if all([op not in sys.argv for op in ['-1', '-2', '-3']]) else False
    if '-1' in sys.argv or exec_all:
        test_encoding_and_decoding()

    if '-2' in sys.argv or exec_all:
        test_for_sample_data(show_hist)

    if '-3' in sys.argv or exec_all:
        test_for_images(show_hist)


def test_encoding_and_decoding():
    print "1. TEST KODOWANIA I DEKODOWANIA\n"
    source = [1, 2, 3, 0, 0, 4, 5, 0, 2, 6, 0, 7, 8, 0, 1, 0, 2, 2, 3, 9, 0, 0, 1, 2]
    print "   Ciąg wejściowy:   ", source

    print "\n   1.1. Kodowanie pośrednie (ze słownikiem)"
    codec = ExpGolombCodec()
    encoded = codec.encode(source)
    print "        Dane zakodowane:  ", encoded
    print "        - Statystyki"
    print "        -- Stopień kompresji: %.2f" % codec.statistics.compression_ratio
    print "        -- Entropia źródła:   %.2f" % codec.statistics.entropy
    print "        -- Średnia dł. słowa: %.2f" % codec.statistics.mean_code_word_length
    decoded = codec.decode(encoded)
    print "        Dane zdekodowane: ", decoded


    print "\n    1.2. Kodowane bezpośrednie (bez słownika)"
    codec = ExpGolombCodec(direct=True)
    encoded = codec.encode(source)
    print "        Dane zakodowane:  ", encoded
    print "        - Statystyki"
    print "        -- Stopień kompresji: %.2f" % codec.statistics.compression_ratio
    print "        -- Entropia źródła:   %.2f" % codec.statistics.entropy
    print "        -- Średnia dł. słowa: %.2f" % codec.statistics.mean_code_word_length
    decoded = codec.decode(encoded)
    print "        Dane zdekodowane: ", decoded

    print "\n=======================================================================\n"



def test_for_sample_data(show_hist=False):
    print "2. TEST KODOWANIA SZTUCZNYCH CIĄGÓW DANYCH\n"
    numpy.random.seed(37)

    print "   2.1. Rozkład jednostajny\n"

    for i, size_kb in enumerate([1, 128, 1024]):
        print "     %s. %dKB" % (chr(ord('a') + i), size_kb)
        uniform_samples = normalize_to_byte(numpy.random.uniform(0., 256., size_kb*1024))
        if show_hist:
            show_histogram(uniform_samples)
        encode_and_print_stats(uniform_samples, 8)

    print "   2.2. Rozkład normalny\n"
    for i, size_kb in enumerate([1, 128, 1024]):
        print "     %s. %dKB" % (chr(ord('a') + i), size_kb)
        normal_samples = normalize_to_byte(numpy.random.normal(128., 16., 1024))
        if show_hist:
            show_histogram(normal_samples)
        encode_and_print_stats(normal_samples, 8)

    print "   2.3. Rozkład Laplace'a\n"
    for i, size_kb in enumerate([1, 128, 1024]):
        print "     %s. %dKB" % (chr(ord('a') + i), size_kb)
        laplace_samples = normalize_to_byte(numpy.random.laplace(128., 16., 1024))
        if show_hist:
            show_histogram(laplace_samples)
        encode_and_print_stats(laplace_samples, 8)

    print "\n=======================================================================\n"


def test_for_images(show_hist=False):
    IMG_PATH = abspath(join(dirname(__file__), pardir, 'images'))
    print "3. TEST KODOWANIA OBRAZÓW\n"
    images = listdir(IMG_PATH)

    for idx, image in enumerate(images, start=1):
        print "   3.%d. %s\n" % (idx, image)
        data = read_image(join(IMG_PATH, image))
        diffed = differential_encoding(data)
        if show_hist:
            show_histogram(diffed, image)
        scaled = scale_to_positive(diffed)
        encode_and_print_stats(scaled, 8)

    print "\n=======================================================================\n"


def encode_and_print_stats(source, indent):
    codec = ExpGolombCodec(direct=True)
    codec.encode(source)
    stat = codec.statistics

    tab = ' ' * indent
    print "%sEntropia źródła:                %5.2f" % (tab, stat.entropy)
    print "%sRozmiar danych źródłowych [KB]: %5.1f" % (tab, stat.source_size/1024./8)
    print
    print "%s+-- Kodowanie bezpośrednie ----------+" % tab
    print "%s| Rozmiar po kompresji [KB]:    %5.1f |" % (tab, stat.compressed_size/1024./8)
    print "%s| Stopień kompresji:            %5.2f |" % (tab, stat.compression_ratio)
    print "%s| Długość słowa kodowego:       %5.2f |" % (tab, stat.mean_code_word_length)
    print "%s+------------------------------------+" % tab

    codec = ExpGolombCodec(direct=False)
    codec.encode(source)
    stat = codec.statistics
    print "%s+-- Kodowanie pośrednie -------------+" % tab
    print "%s| Rozmiar po kompresji [KB]:    %5.1f |" % (tab, stat.compressed_size/1024./8)
    print "%s| Stopień kompresji:            %5.2f |" % (tab, stat.compression_ratio)
    print "%s| Długość słowa kodowego:       %5.2f |" % (tab, stat.mean_code_word_length)
    print "%s+------------------------------------+" % tab
    print



if __name__ == '__main__':
    main()
