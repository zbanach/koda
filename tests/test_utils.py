from ..app.utils import entropy, histogram, write_binary, write_unary

from bitstream import BitStream
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
        assert stream == BitStream(True)
        stream.write(2)
        assert stream == BitStream([True, True, False])
        stream.write(3)
        assert stream == BitStream([True, True, False, True, True])

    def test_writer2(self, stream):
        stream.write(19)
        assert stream == BitStream([True, False, False, True, True])

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
        assert stream == BitStream([False])
        write_unary(stream, 1)
        assert stream == BitStream([False, True, False])
        write_unary(stream, 2)
        assert stream == BitStream([False, True, False, True, True, False])

    def test_writer2(self, stream):
        write_unary(stream, 5)
        assert stream == BitStream([True, True, True, True, True, False])
