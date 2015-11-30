from ..app.utils import entropy, histogram
import math

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
