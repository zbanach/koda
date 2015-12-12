from ..app.utils import entropy, histogram, write_binary, write_unary, read_binary, read_unary, normalize_to_byte
from utils import make_bitstream

from bitstream import BitStream, ReadError
import bitstream
import math
import pytest


def test_histogram():
    assert histogram([]) == {}
    assert histogram([1]) == {1: 1}
    assert histogram([1, 1]) == {1: 2}
    assert histogram([1, 2, 3, 1, 4, 4, 1]) == {1: 3, 2: 1, 3: 1, 4: 2}
    assert histogram([1 if i % 2 == 0 else 2 for i in range(200)]) == \
        {1: 100, 2: 100}

    
def test_entropy():
    assert entropy([]) == 0
    assert entropy([1]) == 0
    assert entropy([1 for i in range(200)]) == 0
    assert entropy([1, 2]) == 1
    assert entropy([1 if i % 2 == 0 else 2 for i in range(200)]) == 1
    assert entropy([1, 2, 3, 4]) == 2
    assert entropy([i for i in range(8)]) == 3
    assert entropy([i for i in range(32)]) == 5
    assert abs(entropy([1, 2, 3]) - -math.log(1/3.0, 2)) < 0.001
    assert abs(entropy([i for i in range(100)]) - -math.log(1/100.0, 2)) < 0.001


def test_normalize_to_byte():
    assert normalize_to_byte(range(256)) == range(256)
    assert normalize_to_byte([-1, 0, 1]) == [0, 0, 1]
    assert normalize_to_byte([240, 255, 256, 257]) == [240, 255, 255, 255]
    assert normalize_to_byte([5, 7, -3, -1, 0, 8, 270, 265, 255]) == [5, 7, 0, 0, 0, 8, 255, 255, 255]


class TestBitStreamBinaryWriter:
    @pytest.fixture
    def stream(self):
        bitstream.register(int, writer=write_binary)
        return BitStream()
    
    def test_writer(self, stream):
        assert stream == BitStream()
        stream.write(0)
        assert stream == BitStream()
        stream.write(1)
        assert stream == make_bitstream('1')
        stream.write(2)
        assert stream == make_bitstream('110')
        stream.write(3)
        assert stream == make_bitstream('11011')

    def test_writer2(self, stream):
        stream.write(19)
        assert stream == make_bitstream('10011')

    def test_writer_for_negative_numbers(self, stream):
        with pytest.raises(ValueError):
            stream.write(-1)


class TestBitStreamUnaryWriter:
    
    @pytest.fixture
    def stream(self):
        return BitStream()
    
    def test_writer(self, stream):
        assert stream == BitStream()
        write_unary(stream, 0)
        assert stream == make_bitstream('1')
        write_unary(stream, 1)
        assert stream == make_bitstream('101')
        write_unary(stream, 2)
        assert stream == make_bitstream('101001')

    def test_writer2(self, stream):
        write_unary(stream, 5)
        assert stream == make_bitstream('000001')


class TestBitStreamBinaryReader:
    
    def test_reader(self):
        assert 0 == read_binary(make_bitstream('0'), 1)
        assert 1 == read_binary(make_bitstream('1'), 1)
        assert 2 == read_binary(make_bitstream('10'), 2)
        assert 5 == read_binary(make_bitstream('101'), 3)
        assert 16 == read_binary(make_bitstream('10000000'), 5)

    def test_reader_sequence(self):
        bs = make_bitstream('100100110')
        assert 4 == read_binary(bs, 3)
        assert 2 == read_binary(bs, 2)
        assert 0 == read_binary(bs, 1)
        assert 6 == read_binary(bs, 3)
        
    def test_reader_underflow(self):
        with pytest.raises(ReadError):
            read_binary(make_bitstream('1'), 2)


class TestBitStreamUnaryReader:

    def test_reader(self):
        assert 0 == read_unary(make_bitstream('1'))
        assert 1 == read_unary(make_bitstream('01'))
        assert 15 == read_unary(BitStream([False for i in range(15)] + [True]))

    def test_reader_sequence(self):
        bs = make_bitstream('0011010001')
        assert 2 == read_unary(bs)
        assert 0 == read_unary(bs)
        assert 1 == read_unary(bs)
        assert 3 == read_unary(bs)
