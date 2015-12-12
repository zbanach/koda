# coding=utf-8
from math import log
import PIL.Image as Img
import matplotlib.pyplot as plt

def histogram(samples):
    """
    Zwraca histogram danego ciągu próbek w postaci słownika.
    """
    hist = {}
    for sample in samples:
        hist[sample] = hist[sample] + 1 if sample in hist else 1
    return hist


def entropy(source):
    """
    Oblicza entropię danych źródłowych, przyjmując że są one kodowane binarnie.
    """    
    alphabet_hist = histogram(source)
    source_len = len(source)
    entropy = 0
    for symbol, occurrences in alphabet_hist.iteritems():
        probability = occurrences / float(source_len)
        entropy -= probability * log(probability, 2)
    return entropy


def write_binary(stream, data, num_bits=0):
    """
    Zapisuje do strumienia bitowego (BitStream) liczbę naturalną lub ciąg liczb, 
    kodując je binarnie (NKB).
    """
    if isinstance(data, list):
        for integer in data:
            write_integer_to_stream(stream, integer)
    else:
        integer = int(data)
        if integer < 0:
            raise ValueError("Nie można zapisać do strumienia ujemnej wartości")
        bools = []
        bits_used = 0
        while integer:
            bools.append(integer & 1)
            integer = integer >> 1
            bits_used += 1
        for i in range(bits_used, num_bits):
            bools.append(False)
        bools.reverse()
        stream.write(bools, bool)


def write_unary(stream, data):
    """
    Zapisuje do strumienia bitowego (BitStream) liczbę naturalną lub ciąg liczb,
    kodując je przy pomocy kodu unarnego.
    """
    if isinstance(data, list):
        for integer in data:
            write_unary(stream, integer)
    else:
        integer = int(data)
        if integer < 0:
            raise ValueError("Nie można zapisać do strumienia ujemnej wartości")
        for i in range(integer):
            stream.write(False)
        stream.write(True)


def read_unary(stream):
    """
    Odczytuje ze strumienia bitowego (BitStream) liczbę naturalną zakodowaną unarnie.
    """
    number = 0
    while stream.read(bool) == False:
        number += 1
    return number


def read_binary(stream, num_bits):
    """
    Odczytuje ze strumienia bitowego (BitStream) liczbę naturalną zakodowaną binarnie
    na podanej liczbie bitów.
    """
    number = 0
    for i in range(num_bits):
        number = number << 1 | stream.read(bool)
    return number

def read_image(filename):
    """
    Wczytuje obrazek z podanej lokalizacji i zwraca tablicę z wartościami pixeli.

    Zakłada się, że obrazek jest w skali szarości, dlatego pobierana jest wartość
    kanału R.
    """
    try:
        img = Img.open(filename)
        return list(img.getdata(0))
    except IOError:
        raise IOError("Nie można wczytać pliku '{}'".format(filename))

def differential_encoding(data, first_value=128):
    """
    Różnicowe kodowanie ciągu.
    """
    return [data[idx - 1] - val if idx > 0 else first_value - val for idx, val in enumerate(data)]

def differential_decoding(data, first_value=128):
    """
    Dekodowanie ciągu zakodowanego różnicowo.
    """
    new_data = [first_value - data[0]]
    for idx, val in enumerate(data[1:], start=1):
        new_data += [new_data[idx - 1] - val]
    return new_data

def scale_to_positive(data):
    """
    Przeskalowanie ciągu liczb ujemno-dodatnich do wartości dodatnich.
    """
    return [(2*abs(val)) - 1 if val < 0 else 2*val for val in data]

def scale_to_nonpositive(data):
    """
    Przeskalowanie ciągu liczb dodatnich do wartości ujemno-dodatnich.
    """
    return [val/2 if val%2 == 0 else -1*(val + 1)/2 for val in data]

def show_histogram(data, name=''):
    """
    Wyświetlenie histogramu dla ciągu danych.
    """
    plt.hist(data)
    plt.xlabel(name)
    plt.show()

def normalize_to_byte(samples):
    return [round(s) if 0 <= s <= 255 else (0 if s < 0 else 255) for s in samples]