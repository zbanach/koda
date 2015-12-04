# coding=utf-8
from utils import write_unary, write_binary, read_unary, read_binary, entropy

import math
from bitstream import BitStream


class ExpGolombCodec:

    def __init__(self):
        self.statistics = None
    
    def encode(self, source):
        stream = BitStream()
        for symbol in source:
            self._encode_symbol(symbol, stream)
        self.statistics = Statistics(source, stream)
        return stream
        
    def decode(self, stream):
        out = []
        while stream:
            out.append(self._decode_symbol(stream))
        #self.statistics = Statistics(out, stream)
        return out
            
    def _encode_symbol(self, symbol, stream):
        q = int(math.floor(math.log(symbol + 1, 2)))
        r = symbol + 1 - math.pow(2, q)
        write_unary(stream, q)
        write_binary(stream, r, num_bits=q)

    def _decode_symbol(self, stream):
        q = read_unary(stream)
        r = read_binary(stream, q)
        return int(math.pow(2, q) + r - 1)


class Statistics:
    def __init__(self, uncompressed, compressed):
        bits = math.ceil(math.log(max(uncompressed), 2)) if max(uncompressed) != 0 else 1
        self.cr = bits*len(uncompressed) / len(compressed) if len(compressed) > 0 else 0
        self.entropy = entropy(uncompressed)
        self.mean_codeword = len(compressed) / len(uncompressed) if len(uncompressed) > 0 else 0
        
    def __str__(self):
        return "Stopień kompresji:\t\t%.2f\n" \
               "Entropia źródła:\t\t%.2f\n" \
               "Średnia dł. słowa:\t\t%.2f" % (self.cr, self.entropy, self.mean_codeword)
