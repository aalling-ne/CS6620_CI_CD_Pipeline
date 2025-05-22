import pipeline as pl
import pytest

def test_zero_zero():
    assert(pl.add_then_power(0, 0) == 1)

def test_two_four():
    assert(pl.add_then_power(2,4) == 1296)

def test_string_input():
    with pytest.raises(TypeError):
        pl.add_then_power(1,"two")