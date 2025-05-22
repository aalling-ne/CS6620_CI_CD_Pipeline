import pipeline as pl

def test_zero_zero():
    assert(pl.add_then_power(0, 0) == 0)

def test_two_four():
    assert(pl.add_then_power(2,4) == 1296)