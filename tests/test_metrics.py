from benchmark import f1_score

def test_f1_perfect():
    assert f1_score(tp=10, fp=0, fn=0) == 1.0

def test_f1_zero_when_no_predictions():
    assert f1_score(tp=0, fp=0, fn=5) == 0.0

def test_f1_half():
    # precision=0.5, recall=0.5 -> f1=0.5
    assert abs(f1_score(tp=5, fp=5, fn=5) - 0.5) < 1e-9
