from ..app.codec import ExpGolombCodec
from utils import make_bitstream

import pytest


class TestDirectEncoding:
    
    @pytest.fixture
    def codec(self):
        return ExpGolombCodec(True)

    def test_encoding_single_symbols(self, codec):
        assert codec.encode([0]) == make_bitstream('1')
        assert codec.encode([1]) == make_bitstream('010')
        assert codec.encode([2]) == make_bitstream('011')
        assert codec.encode([3]) == make_bitstream('00100')
        assert codec.encode([4]) == make_bitstream('00101')
        assert codec.encode([5]) == make_bitstream('00110')
        assert codec.encode([6]) == make_bitstream('00111')

    def test_encoding_sequence(self, codec):
        seq = [3, 1, 0, 0, 1, 2, 4]
        expected = make_bitstream('001000101101001100101')
        assert codec.encode(seq) == expected

        
class TestDirectDecoding:

    @pytest.fixture
    def codec(self):
        return ExpGolombCodec(True)

    def test_decoding_single_symbols(self, codec):
        assert codec.decode(make_bitstream('1')) == [0]
        assert codec.decode(make_bitstream('010')) == [1]
        assert codec.decode(make_bitstream('011')) == [2]
        assert codec.decode(make_bitstream('00100')) == [3]
        assert codec.decode(make_bitstream('00101')) == [4]
        assert codec.decode(make_bitstream('00110')) == [5]
        assert codec.decode(make_bitstream('00111')) == [6]

    def test_decoding_sequence(self, codec):
        stream = make_bitstream('001111100101101000110011')
        expected = [6, 0, 0, 4, 0, 1, 5, 2]
        assert codec.decode(stream) == expected


class TestIndirectEncoding:

    @pytest.fixture
    def codec(self):
        return ExpGolombCodec()

    def test_encoding_sequence(self, codec):
        seq = [0, 3, 1, 0, 2, 0, 2, 0, 3, 0, 0, 2]
        header = '0'*13 + '100'+'0010'+'00'+'10'+'11'+'01'
        code_words = '1'+'011'+'00100'+'1'+'010'+'1'+'010'+'1'+'011'+'1'+'1'+'010'
        expected = make_bitstream(header + code_words)
        assert codec.encode(seq) == expected


class TestIndirectDecoding:

    @pytest.fixture
    def codec(self):
        return ExpGolombCodec()

    def test_decoding_sequence(self, codec):
        header = '0'*13 + '100'+'0010'+'00'+'10'+'11'+'01'
        code_words = '1'+'011'+'00100'+'1'+'010'+'1'+'010'+'1'+'011'+'1'+'1'+'010'
        stream = make_bitstream(header + code_words)
        expected = [0, 3, 1, 0, 2, 0, 2, 0, 3, 0, 0, 2]
        assert codec.decode(stream) == expected
