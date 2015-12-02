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


def write_binary(stream, data):
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
        while integer:
            bools.append(integer & 1)
            integer = integer >> 1
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
            stream.write(True)
        stream.write(False)
