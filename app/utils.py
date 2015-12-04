# coding=utf-8
from math import log

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
