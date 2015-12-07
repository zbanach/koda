# coding=utf-8
from utils import write_unary, write_binary, read_unary, read_binary, entropy, histogram

import math
from bitstream import BitStream


class ExpGolombCodec:
    """Koder/dekoder danych, wykorzystujący wykładniczy kod Golomba.

    W wykładniczym kodzie Golomba, alfabet symboli dzielony jest na przedziały zmiennej
    długości w taki sposób, że q-ty przedział zawiera 2^q symboli. Słowo kodowe jest 
    wynikiem konkatenacji numeru przedziału zakodowanego unarnie oraz odległości od 
    początku przedziału, zakodowanej binarnie na q bitach.

    Kodek może pracować w dwóch trybach:
    1) bezpośrednim (direct=True) - symbole alfabetu wejściowego kodowane są bezpośrednio
       przy pomocy kodu Golomba. Wyjściem kodera i wejściem dekodera jest ciąg bitowy 
       składający się wyłącznie z zakodowanych symboli.
    2) pośrednim (direct=False) - symbole alfabetu źródłowego są porządkowane według 
       nierosnącego prawdopodobieństwa, a kodowany jest ich numer porządkowy. Do zakodowanego
       ciągu dołączany jest nagłówek, zawierający uporządkowaną listę symboli (książka kodów).
    """

    def __init__(self, direct=False):
        """Tworzy i inicjalizuje nową instancję kodera/dekodera.

        Argumenty:
            direct (bool): tryb pracy kodera (True - bezpośredni, False - pośredni)
        """        
        self._direct = direct
        self._stats = Statistics()
        self._hist = None

    def encode(self, source):
        """Koduje wejściowy ciąg danych przy pomocy wykładniczego kodu Golomba.

        Argumenty:
            source (List[int]): ciąg liczb naturalnych do zakodowania

        Zwraca:
            BitStream: strumień bitowy zawierający ciąg słów kodowych oraz opcjonalnie
                nagłówek (przy pośrednim trybie pracy kodera).
        """
        stream = BitStream()
        self._source = source
        self._hist = histogram(source)
        # Utworzenie i zapisanie w nagłówku książki kodów (jeżeli wybrano tryb pośredni)
        if not self._direct:
            self._codebook = self._make_codebook(stream)
        header_len = len(stream)
        # Kodowanie danych źródłowych
        for word in source:
            self._encode_word(word, stream)
        # Obliczenie statystyk
        self._stream_len = len(stream)
        self._stream_data_len = len(stream) - header_len
        self._stats = Statistics(self)
        return stream

    def decode(self, stream):
        """Dekoduje dane zakodowane wcześniej przy pomocy kodera.

        Argumenty:
            stream (BitStream): strumień bitowy zawierający ciąg słów kodowych
                oraz opcjonalnie nagłówek (przy pośrednim trybie pracy kodera).

        Zwraca:
            List[int]: ciąg odkodowanych liczb naturalnych
        """
        self._source = []
        self._stream_len = len(stream)
        # Odczyt nagłówka z książką kodów (jeżeli wybrano tryb pośredni)
        if not self._direct:
            self._codebook = self._read_codebook(stream)
        self._stream_data_len = len(stream)
        # Dekodowanie danych
        while stream:
            word = self._decode_word(stream)
            self._source.append(word)
        # Obliczenie statystyk
        self._stats = Statistics(self)
        return self._source

    @property
    def statistics(self):
        return self._stats

    def _make_codebook(self, stream):
        alphabet = self._hist.keys()
        ordered_alphabet = sorted(alphabet, key=self._hist.get, reverse=True)
        codebook = {symbol: code for code, symbol in enumerate(ordered_alphabet)}

        # Zapis książki kodów do strumienia
        symbol_size = int(math.ceil(math.log(max(alphabet) or 1, 2)))
        write_binary(stream, len(alphabet), num_bits=16)
        write_binary(stream, symbol_size, num_bits=4)
        for symbol in ordered_alphabet:
            write_binary(stream, symbol, num_bits=symbol_size)
        return codebook

    def _encode_word(self, word, stream):
        symbol = word if self._direct else self._codebook[word]
        q = int(math.floor(math.log(symbol + 1, 2)))
        r = symbol + 1 - math.pow(2, q)
        write_unary(stream, q)
        write_binary(stream, r, num_bits=q)

    def _read_codebook(self, stream):
        number_of_symbols = read_binary(stream, 16)
        symbol_size = read_binary(stream, 4)
        return {i: read_binary(stream, symbol_size) for i in range(number_of_symbols)}

    def _decode_word(self, stream):
        q = read_unary(stream)
        r = read_binary(stream, q)
        symbol = int(math.pow(2, q) + r - 1)
        return symbol if self._direct else self._codebook[symbol]


class Statistics:        
    def __init__(self, codec=None):
        if codec:
            self._source_len = len(codec._source)
            self._entropy = entropy(codec._source)
            self._hist = codec._hist if codec._hist else histogram(codec._source)
            self._symbol_size = int(math.ceil(math.log(max(self._hist.keys()) or 1, 2)))
            self._cr = float(self._source_len) * self._symbol_size / codec._stream_len
            self._mean_code_len = float(codec._stream_data_len) / self._source_len
            self._source_size = self._symbol_size * self._source_len
            self._stream_size = codec._stream_len
        else:
            self._source_len = 0
            self._entropy = 0
            self._hist = {}
            self._cr = 0
            self._mean_code_len = 0
            self._symbol_len = 0
            self._source_size = 0
            self._stream_size = 0
        
    def __str__(self):
        return "- Statystyki\n" \
               "--- Stopień kompresji:\t%.2f\n" \
               "--- Entropia źródła:\t%.2f\n" \
               "--- Średnia dł. słowa:\t%.2f" % (self._cr, self._entropy, self._mean_code_len)

    @property
    def histogram(self):
        """Zwraca histogram symboli alfabetu źródłowego w postaci słownika."""
        return self._hist

    @property
    def alphabet(self):
        """Zwraca listę symboli alfabetu źródłowego, uporządkowaną wg nierosnącego p-ństwa."""
        return sorted(self._hist.keys(), key=self._hist.get, reverse=True)
    
    @property
    def entropy(self):
        """Zwraca wartość entropii danych źródłowych."""
        return self._entropy

    @property
    def compression_ratio(self):
        """Zwraca wartość współczynnika kompresji danych."""
        return self._cr

    @property
    def mean_code_word_length(self):
        """Zwraca średnią długość słowa kodowego."""
        return self._mean_code_len

    @property
    def source_length(self):
        """Zwraca długość ciągu danych źródłowych (liczbę słów)."""
        return self._source_len

    @property
    def symbol_size(self):
        """Zwraca min. liczbę bitów potrzebną do zapisania symboli alfabetu źródłowego w NKB."""
        return self._symbol_size

    @property
    def source_size(self):
        """Zwraca całkowity rozmiar danych źródłowych."""
        return self._source_size

    @property
    def compressed_size(self):
        """Zwraca całkowity rozmiar zakodowanych danych."""
        return self._stream_size
