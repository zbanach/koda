# coding=utf-8
from codec import ExpGolombCodec
from utils import entropy, read_image, differential_encoding, scale_to_positive, show_histogram
from os.path import dirname, join, pardir, abspath
from os import listdir

def main():
    IMG_PATH = abspath(join(dirname(__file__), pardir, 'images'))
    source = [1, 2, 3, 0, 0, 4, 5, 0, 2, 6, 0, 7, 8, 0, 1, 0, 2, 2, 3, 9, 0, 0, 1, 2]
    #source = [255, 255, 255, 255, 255, 254]
    print "Ciąg wejściowy:   ", source

    print "\n1. Kodowanie pośrednie (ze słownikiem)"
    codec = ExpGolombCodec()
    encoded = codec.encode(source)
    print "Dane zakodowane:  ", encoded
    print codec.statistics
    s = codec.statistics
    print s.alphabet
    print s.histogram
    decoded = codec.decode(encoded)
    print "Dane zdekodowane: ", decoded
    print codec.statistics

    print "\n2. Kodowane bezpośrednie (bez słownika)"
    codec = ExpGolombCodec(direct=True)
    encoded = codec.encode(source)
    print "Dane zakodowane:  ", encoded
    decoded = codec.decode(encoded)
    print "Dane zdekodowane: ", decoded
    print codec.statistics

    print "\nInne statystyki:"
    s = codec.statistics
    print "Alfabet źródłowy: ", s.alphabet
    print "Histogram: ", s.histogram
    print "Długość ciągu źródłowego: ", s.source_length
    print "Rozmiar słowa źródłowego: ", s.symbol_size
    print "Rozmiar danych źródłowych [b]: ", s.source_size
    print "Rozmiar danych zakodowanych [b]: ", s.compressed_size

    print "\nKODOWANIE OBRAZÓW"
    images = listdir(IMG_PATH)
    for idx, image in enumerate(images, start=1):
        print "\n{}. Obraz {}".format(idx, image)
        data = read_image(join(IMG_PATH, image))
        diffed = differential_encoding(data)
        show_histogram(diffed, image)
        scaled = scale_to_positive(diffed)
        for direct in (True, False):
            codec = ExpGolombCodec(direct)
            codec.encode(scaled)
            stat = codec.statistics
            if direct:
                print "Długość ciągu źródłowego: ", stat.source_length
                print "Rozmiar słowa źródłowego: ", stat.symbol_size
                print "Rozmiar danych źródłowych [b]: ", stat.source_size
            print '\nKodowanie bez słownika' if direct else '\nKodowanie ze słownikiem'
            print stat
            print "Rozmiar danych zakodowanych [b]: ", stat.compressed_size

if __name__ == '__main__':
    main()
    
