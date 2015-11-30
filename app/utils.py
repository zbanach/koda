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
